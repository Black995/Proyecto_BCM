<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="activities"
                            responsiveLayout="scroll"
                            :paginator="true"
                            :rows="10"
                            :rowsPerPageOptions="[10, 20]"
                            :resizableColumns="true"
                            :autoLayout="true"
                            :responsive="true"
                            :reorderableColumns="true"
                            :loading="loading"
                            :globalFilterFields="[
                                'name',
                                'cost',
                                'recovery_time',
                                'criticality',
                            ]"
                            :filters="filterGlobal"
                        >
                            <template #header>
                                <b-row class="justify-content-between">
                                    <b-col sm="4">
                                        <b-button
                                            title="Crear actividad de negocio"
                                            variant="success"
                                            @click="show_modal_create = true"
                                        >
                                            <font-awesome-icon
                                                icon="fa-solid fa-plus"
                                            />
                                        </b-button>
                                    </b-col>
                                    <b-col sm="4">
                                        <span class="p-input-icon-left">
                                            <i class="pi pi-search" />

                                            <InputText
                                                v-model="
                                                    filterGlobal['global'].value
                                                "
                                                placeholder="Buscar..."
                                            />
                                        </span>
                                    </b-col>
                                    <b-col sm="1">
                                        <b-button
                                            title="Descargar"
                                            variant="warning"
                                            @click="" 
                                        >
                                        <font-awesome-icon icon="fa-solid fa-file-pdf" />
                                        </b-button>
                                    </b-col>
                                </b-row>
                            </template>
                            <Column field="name" header="Nombre"></Column>

                            <Column field="cost" header="Costo">
                                <template #body="slotProps">
                                    <div v-if="slotProps.data.cost > 0">
                                        {{ slotProps.data.cost }}$
                                    </div>
                                </template>
                            </Column>
                            <Column
                                field="recovery_time"
                                header="Tiempo de recuperación"
                            ></Column>
                            <Column field="criticality" header="Criticidad">
                                <template #body="slotProps">
                                    <div v-if="!slotProps.data.scale_max_value">
                                        {{ slotProps.data.criticality }}
                                    </div>
                                    <div v-if="slotProps.data.scale_max_value">
                                        {{ slotProps.data.criticality }}/{{
                                            slotProps.data.scale_max_value
                                        }}
                                    </div>
                                </template>
                            </Column>
                            <Column field="id" header="Opciones">
                                <template #body="slotProps">
                                    <b-button
                                        title="Detalle de la actividad"
                                        pill
                                        variant="info"
                                        @click="
                                            show_modal_detail(slotProps.data.id)
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-search"
                                        />
                                    </b-button>
                                    <b-button
                                        title="Editar actividad de la organización"
                                        pill
                                        variant="warning"
                                        @click="
                                            show_modal_update(slotProps.data.id)
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-pen-to-square"
                                        />
                                    </b-button>
                                    <b-button
                                        title="Eliminar actividad"
                                        pill
                                        variant="danger"
                                        @click="
                                            show_modal_delete(slotProps.data.id)
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-trash"
                                        />
                                    </b-button>
                                </template>
                            </Column>
                            <Column field="id_2" header="Asociar servicios">
                                <template #body="slotProps">
                                    <div class="text-center">
                                        <b-button
                                            pill
                                            title="Asociar servicios de la organización"
                                            variant="primary"
                                            @click="
                                                show_modal_association_services(
                                                    slotProps.data.id,
                                                    slotProps.data.name
                                                )
                                            "
                                        >
                                            <font-awesome-icon
                                                icon="fa-solid fa-computer"
                                            />
                                        </b-button>
                                    </div>
                                </template>
                            </Column>
                            <Column field="id_3" header="Asociar riesgos">
                                <template #body="slotProps">
                                    <div class="text-center">
                                        <b-button
                                            pill
                                            title="Asociar riesgos"
                                            variant="primary"
                                            @click="
                                                show_modal_association_risks(
                                                    slotProps.data.id,
                                                    slotProps.data.name
                                                )
                                            "
                                        >
                                            <font-awesome-icon
                                                icon="fa-solid fa-chart-line"
                                            />
                                        </b-button>
                                    </div>
                                </template>
                            </Column>
                            <template #empty>
                                No hay actividades encontradas.
                            </template>
                        </DataTable>
                    </div>
                </div>
            </div>
        </div>
        <div class="row"></div>

        <!--
            Modal del detalle  
        -->

        <b-modal
            id="modal-detail"
            title="Detalle de la actividad"
            ref="modal"
            size="lg"
            centered
        >
            <h3 class="text-center font-weight-bold">
                {{ activityDetail.name }}
            </h3>
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <strong>Descripción: </strong>
                    {{ activityDetail.description }}
                </li>
                <li v-if="activityDetail.cost" class="list-group-item">
                    <strong>Costo: </strong> {{ activityDetail.cost }}
                </li>
                <li v-if="!activityDetail.cost" class="list-group-item">
                    <strong>Costo: </strong> no aplica
                </li>
                <li class="list-group-item">
                    <strong>Tiempo de recuperación: </strong>
                    {{ activityDetail.recovery_time }}
                </li>
                <li class="list-group-item">
                    <div v-if="!activityDetail.scale_max_value">
                        <strong>Criticidad: </strong>
                        {{ activityDetail.criticality }}
                    </div>
                    <div v-if="activityDetail.scale_max_value">
                        <strong>Criticidad: </strong>
                        {{ activityDetail.criticality }}/{{
                            activityDetail.scale_max_value
                        }}
                    </div>
                </li>
            </ul>
            <h4 class="mt-5 text-center font-weight-bold">
                Servicios de la organización que dependen de esta actividad
            </h4>
            <b-list-group-item
                class="mt2 flex-column align-items-start"
                v-for="item in activityDetail._services_offered"
                :key="item.key"
            >
                <h5 class="mb-1">{{ item.name }}</h5>
                <div class="mb-1 d-flex w-100 justify-content-between">
                    <div>Area: {{ item.area_name }}</div>
                    <div>Tipo: {{ item.type_name }}</div>
                    <div v-if="!item.scale_max_value">
                        Criticidad: {{ item.criticality }}
                    </div>
                    <div v-if="item.scale_max_value">
                        Criticidad: {{ item.criticality }}/{{
                            item.scale_max_value
                        }}
                    </div>
                </div>
            </b-list-group-item>
            <h3
                class="mt-3 text-center"
                v-if="!activityDetail._services_offered.length"
            >
                No existen servicios de la organización asociados a esta
                actividad
            </h3>
            <h4 class="mt-5 text-center font-weight-bold">
                Riesgos asociados a la actividad de la organización
            </h4>
            <b-list-group-item
                class="mt-2 flex-column align-items-start"
                v-for="item in activityDetail._risks"
                :key="item.key"
            >
                <h5 class="mb-1">{{ item.name }}</h5>
                <p class="mb-1">Descripción: {{ item.description }}</p>
            </b-list-group-item>
            <h3 class="mt-3 text-center" v-if="!activityDetail._risks.length">
                No existen riesgos asociados a esta actividad
            </h3>
            <!--h4 class="mt-5 text-center font-weight-bold">
                Sedes donde se realiza la actividad de la organización
            </h4>
            <b-list-group-item
                class="mt-2 flex-column align-items-start"
                v-for="item in activityDetail._headquarters"
                :key="item.key"
            >
                <h5 class="mb-1">{{ item.name }}</h5>
                <p class="mb-1">Ubicación: {{ item.location_name }}</p>
            </b-list-group-item>
            <h3
                class="mt-3 text-center"
                v-if="!activityDetail._headquarters.length"
            >
                Esta actividad no esta asociada a ninguna sede
            </h3-->
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="info"
                        class="float-right"
                        @click="$bvModal.hide('modal-detail')"
                    >
                        Cerrar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de crear  
        -->
        <b-modal
            v-model="show_modal_create"
            id="modal-create"
            title="Crear activida del negocio"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-form-group
                    label="Ingrese el nombre de la actividad"
                    invalid-feedback="Este campo es obligatorio"
                    :state="activityState.name"
                >
                    <b-form-input
                        v-model="activity.name"
                        :state="activityState.name"
                        required
                    >
                    </b-form-input>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción de la actividad"
                    invalid-feedback="Este campo es obligatorio"
                    :state="activityState.description"
                >
                    <b-form-textarea
                        v-model="activity.description"
                        :state="activityState.description"
                        required
                        rows="3"
                    ></b-form-textarea>
                </b-form-group>
                <b-row align-v="center">
                    <b-col>
                        <b-form-group
                            label="Tiempo de recuperación"
                            invalid-feedback="Este campo es obligatorio"
                        >
                            <b-row cols="1" cols-sm="3" cols-lg="3">
                                <b-col>
                                    <b-form-group label="Días">
                                        <b-form-input
                                            type="number"
                                            v-model="duration.days"
                                        ></b-form-input>
                                    </b-form-group>
                                </b-col>
                                <b-col>
                                    <b-form-group label="Horas">
                                        <b-form-select
                                            v-model="duration.hours"
                                            :options="hours"
                                            label="Horas"
                                        ></b-form-select>
                                    </b-form-group>
                                </b-col>
                                <b-col>
                                    <b-form-group label="Minutos">
                                        <b-form-select
                                            v-model="duration.minutes"
                                            :options="minutes"
                                            label="Minutos"
                                        ></b-form-select>
                                    </b-form-group>
                                </b-col>
                            </b-row>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese el costo (en dolares)"
                            invalid-feedback="El costo no puede ser negativo"
                        >
                            <b-form-input
                                type="number"
                                v-model.number="activity.cost"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-form-group
                    label="Ingrese la criticidad"
                    invalid-feedback="El valor de la criticidad está fuera de la escala actual"
                    :state="activityState.criticality"
                >
                    <b-form-spinbutton
                        v-model.number="activity.criticality"
                        :min="scaleView.scale_min_value"
                        :max="scaleView.scale_max_value"
                        :state="activityState.criticality"
                    ></b-form-spinbutton>
                </b-form-group>
                <b-row>
                    <b-col>
                        <p class="mb-1">
                            <strong>
                                Escala a utilizar pasa la criticidad:
                            </strong>
                            {{ scaleView.scale_name }}
                        </p>
                    </b-col>
                </b-row>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitCreate"
                    >
                        Crear actividad de la organización
                    </b-button>
                </div>
            </template>
        </b-modal>
        <!--
            Modal de confirmar crear  
        -->
        <b-modal
            id="modal-confirm-create"
            title="Confirmar crear actividad de la organización"
            centered
        >
            <h4>¿Está seguro de crear esta actividad?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createActivity"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <b-modal
            id="modal-update"
            title="Editar actividad de la organización"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-form-group
                    label="Ingrese el nombre de la actividad"
                    invalid-feedback="Este campo es obligatorio"
                    :state="activityState.name"
                >
                    <b-form-input
                        v-model="activity.name"
                        :state="activityState.name"
                        required
                    >
                    </b-form-input>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción de la actividad"
                    invalid-feedback="Este campo es obligatorio"
                    :state="activityState.description"
                >
                    <b-form-textarea
                        v-model="activity.description"
                        :state="activityState.description"
                        required
                        rows="3"
                    ></b-form-textarea>
                </b-form-group>
                <b-row align-v="center">
                    <b-col>
                        <b-form-group
                            label="Tiempo de recuperación"
                            invalid-feedback="Este campo es obligatorio"
                        >
                            <b-row cols="1" cols-sm="3" cols-lg="3">
                                <b-col>
                                    <b-form-group label="Días">
                                        <b-form-input
                                            type="number"
                                            v-model="duration.days"
                                        ></b-form-input>
                                    </b-form-group>
                                </b-col>
                                <b-col>
                                    <b-form-group label="Horas">
                                        <b-form-select
                                            v-model="duration.hours"
                                            :options="hours"
                                            label="Horas"
                                        ></b-form-select>
                                    </b-form-group>
                                </b-col>
                                <b-col>
                                    <b-form-group label="Minutos">
                                        <b-form-select
                                            v-model="duration.minutes"
                                            :options="minutes"
                                            label="Minutos"
                                        ></b-form-select>
                                    </b-form-group>
                                </b-col>
                            </b-row>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese el costo (en dolares)"
                            invalid-feedback="El costo no puede ser negativo"
                        >
                            <b-form-input
                                type="number"
                                v-model.number="activity.cost"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-form-group
                    label="Ingrese la criticidad"
                    invalid-feedback="El valor de la criticidad está fuera de la escala actual"
                    :state="activityState.criticality"
                >
                    <b-form-spinbutton
                        v-model.number="activity.criticality"
                        :min="scaleView.scale_min_value"
                        :max="scaleView.scale_max_value"
                        :state="activityState.criticality"
                    ></b-form-spinbutton>
                </b-form-group>
                <b-row>
                    <b-col>
                        <p class="mb-1">
                            <strong>
                                Escala a utilizar pasa la criticidad:
                            </strong>
                            {{ scaleView.scale_name }}
                        </p>
                    </b-col>
                </b-row>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitUpdate"
                    >
                        Editar actividad
                    </b-button>
                </div>
            </template>
        </b-modal>

        <b-modal
            id="modal-confirm-update"
            title="Confirmar crear actividad de la organización"
            centered
        >
            <h4>¿Está seguro de editar esta actividad?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="updateActivity"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar eliminar  
        -->
        <b-modal
            id="modal-confirm-delete"
            title="Confirmar Elminar actividad"
            centered
        >
            <h4>¿Está seguro de eliminar este servicio?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteActivity"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de asociar servicios de la organización con actividades de la organización 
        -->
        <b-modal
            id="modal-associate-services"
            title="Asociar servicios de la organización con la actividad"
            size="lg"
            centered
        >
            <multiselect
                v-model="selectedServicesOffered"
                placeholder="Buscar servicios de la organización"
                label="name"
                track-by="id"
                :options="servicesOffered"
                :multiple="true"
            ></multiselect>

            <b-list-group v-if="selectedServicesOffered.length" class="mt-3">
                <b-list-group-item
                    href="#"
                    class="flex-column align-items-start"
                    v-for="item in selectedServicesOffered"
                    :key="item.key"
                >
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">{{ item.name }}</h5>
                        <!--small class="text-muted">3 days ago</small-->
                    </div>
                    <div class="mb-1 d-flex w-100 justify-content-between">
                        <div>Area: {{ item.area_name }}</div>
                        <div>Tipo: {{ item.type_name }}</div>
                        <div v-if="!item.scale_max_value">
                            Criticidad: {{ item.criticality }}
                        </div>
                        <div v-if="item.scale_max_value">
                            Criticidad: {{ item.criticality }}/{{
                                item.scale_max_value
                            }}
                        </div>
                    </div>
                </b-list-group-item>
            </b-list-group>

            <h3 class="mt-3 text-center" v-if="!selectedServicesOffered.length">
                No existen servicios de la organización asociados a este
                servicio contratado
            </h3>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="primary"
                        class="float-right"
                        @click="show_modal_confirm_association_services"
                    >
                        Asociar servicios de la organización
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar asociar servicios  
        -->
        <b-modal
            id="modal-confirm-associate-services"
            title="Confirmar asociar servicios de la organización"
            centered
        >
            <h4>
                ¿Está seguro de asociar estos servicios de la organización a la
                actividad
                <strong>{{ activityName }}</strong
                >?
            </h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="primary"
                        class="float-right"
                        @click="associateServices"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>
        <!--
            Modal de asociar riesgos con servicios contratados
        -->
        <b-modal
            id="modal-associate-risks"
            title="Asociar riesgos con servicios contratados"
            size="lg"
            centered
        >
            <multiselect
                v-model="selectedRisks"
                placeholder="Buscar riesgos"
                label="name"
                track-by="id"
                :options="crisisScenarioRisks"
                :multiple="true"
                group-label="name"
                group-values="_risks"
                :group-select="true"
            ></multiselect>

            <b-list-group v-if="selectedRisks.length" class="mt-3">
                <b-list-group-item
                    href="#"
                    class="flex-column align-items-start"
                    v-for="item in selectedRisks"
                    :key="item.key"
                >
                    <h5 class="mb-1">{{ item.name }}</h5>
                    <p class="mb-1">Descripción: {{ item.description }}</p>
                </b-list-group-item>
            </b-list-group>

            <h3 class="mt-3 text-center" v-if="!selectedRisks.length">
                No existen riesgos asociados a este servicio contratado
            </h3>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="primary"
                        class="float-right"
                        @click="show_modal_confirm_association_risks"
                    >
                        Asociar riesgos
                    </b-button>
                </div>
            </template>
        </b-modal>
        <!--
            Modal de confirmar asociar riesgos  
        -->
        <b-modal
            id="modal-confirm-associate-risks"
            title="Confirmar asociar riesgos"
            centered
        >
            <h4>
                ¿Está seguro de asociar estos riesgos a la actividad
                <strong>{{ activityName }}</strong
                >?
            </h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="primary"
                        class="float-right"
                        @click="associateRisks"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>
    </div>
</template>

<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import { FilterMatchMode } from "primevue/api";
import Multiselect from "vue-multiselect";
import NotificationTemplate from "../Notifications/NotificationTemplate";
import {
    getRecoveryTimeText,
    getRecoveryTime,
    setRecoveryTime,
} from "../../helpers/helpers";

export default {
    name: "BussinesActivities",
    components: {
        Multiselect,
    },
    data: () => ({
        loading: false,
        filterGlobal: {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        },

        show_modal_create: false,

        activities: [],
        activityId: 0,
        activityName: "",
        type: "",

        activity: {
            name: "",
            description: "",
            cost: 0,
            recovery_time: "",
            criticality: 0,
            scale: 0,
        },
        activityDetail: {
            name: "",
            description: "",
            cost: 0,
            recovery_time: "",
            criticality: 0,
            scale_name: "",
            scale_min_value: 0,
            scale_max_value: 0,
            _services_offered: [],
            _risks: [],
            _headquarters: [],
        },
        activityState: {
            name: null,
            description: null,
            criticality: null,
        },
        duration: {
            days: 0,
            hours: 0,
            minutes: 0,
        },
        hours: [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
            19, 20, 21, 22, 23,
        ],
        minutes: [0, 15, 30, 45],

        // Variable en la que se maneja la escala de la vista
        scaleView: {
            id: 0,
            name: "",
            scale: 0,
            scale_name: "",
            scale_min_value: 0,
            scale_max_value: 0,
        },

        servicesOffered: [],
        selectedServicesOffered: [],

        risks: [],
        selectedRisks: [],

        headquarters: [],
        selectedHeadquarters: [],

        crisisScenarioRisks: [],
    }),
    mounted() {
        this.getBussinesActivities();
        this.getScaleView();
        this.getServicesOffered();
        this.getRisks();
        this.getCrisisScenarioRisks();
    },
    methods: {
        successMessage(successText) {
            this.$notify({
                component: NotificationTemplate,
                title: successText,
                icon: "ti-check",
                horizontalAlign: "right",
                verticalAlign: "top",
                type: "success",
            });
        },
        errorMessage(errorText) {
            this.$notify({
                component: NotificationTemplate,
                title: errorText,
                icon: "ti-close",
                horizontalAlign: "right",
                verticalAlign: "top",
                type: "danger",
            });
        },
        async getBussinesActivities() {
            this.loading = true;
            this.activities = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/organizationActivities/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.activities = [];
                    for (var i = 0; i < res.data.length; i++) {
                        res.data[i].recovery_time = getRecoveryTimeText(
                            res.data[i].recovery_time
                        );
                        this.activities.push(res.data[i]);
                    }
                    this.loading = false;
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        /**
         * Filtros que se manejan en Prime Vue
         */
        clearFilter1() {
            this.initFilters1();
        },
        initFilters1() {
            this.filterGlobal = {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS },
            };
        },
        async getScaleView() {
            axios
                .get(`${SERVER_ADDRESS}/api/config/scales/view/`, {
                    params: { name: "Actividades de la Organización" },
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.scaleView = res.data[0];
                    this.scaleView.scale_min_value = parseInt(
                        this.scaleView.scale_min_value
                    );
                    this.scaleView.scale_max_value = parseInt(
                        this.scaleView.scale_max_value
                    );
                    this.activity.criticality = res.data[0].scale_min_value;
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        checkFormValidity() {
            let valid = true;
            if (!this.activity.name) {
                valid = false;
                this.activityState.name = false;
            }
            if (!this.activity.description) {
                valid = false;
                this.activityState.description = false;
            }
            // Los costos son opcionales
            if (this.activity.cost < 0) {
                valid = false;
                this.activityState.cost = false;
            }
            if (
                this.activity.criticality < this.scaleView.scale_min_value ||
                this.activity.criticality > this.scaleView.scale_max_value
            ) {
                this.activityState.criticality = false;
                valid = false;
            }
            return valid;
        },
        handleSubmitCreate() {
            this.activityState.name = null;
            this.activityState.description = null;
            this.activityState.criticality = null;

            if (!this.checkFormValidity()) {
                return;
            }

            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create");
            });
        },
        createActivity() {
            this.activity.recovery_time = setRecoveryTime(this.duration);
            this.activity.scale = this.scaleView.scale;

            axios
                .post(
                    `${SERVER_ADDRESS}/api/phase2/organizationActivities/`,
                    this.activity,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.successMessage(
                        "¡La actividad ha sido creada exitosamente!"
                    );

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    this.getBussinesActivities();
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        handleSubmitUpdate() {
            this.activityState.name = null;
            this.activityState.description = null;
            this.activityState.criticality = null;

            if (!this.checkFormValidity()) {
                return;
            }

            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-update");
            });
        },
        show_modal_update(id) {
            this.activityId = id;

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase2/organizationActivity/${this.activityId}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.activity = res.data;
                    this.duration = getRecoveryTime(res.data.recovery_time);
                    this.$nextTick(() => {
                        this.$bvModal.show("modal-update");
                    });
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        async updateActivity() {
            this.activity.recovery_time = setRecoveryTime(this.duration);
            this.activity.scale = this.scaleView.scale;
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/organizationActivity/${this.activityId}/`,
                    this.activity,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.successMessage(
                        "¡La actividad ha sido actualizada exitosamente!"
                    );

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });
                    this.getBussinesActivities();
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        async show_modal_detail(id) {
            this.activityDetail = {
                name: "",
                description: "",
                cost: 0,
                recovery_time: "",
                criticality: 0,
                scale_name: "",
                scale_min_value: 0,
                scale_max_value: 0,
                _services_offered: [],
                _risks: [],
                _headquarters: [],
            };
            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase2/organizationActivity/${id}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.activityDetail = res.data;
                    this.$bvModal.show("modal-detail");
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        async show_modal_delete(id) {
            this.activityId = id;
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
        async deleteActivity() {
            axios
                .delete(
                    `${SERVER_ADDRESS}/api/phase2/organizationActivity/${this.activityId}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.successMessage(
                        "¡La actividad ha sido eliminada exitosamente!"
                    );
                    this.getBussinesActivities();

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-delete");
                    });
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        async show_modal_association_services(id, name) {
            this.activityId = id;
            this.activityName = name;
            this.selectedServicesOffered = [];

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase2/organizationActivity/${id}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    for (
                        let i = 0;
                        i < res.data._services_offered.length;
                        i++
                    ) {
                        this.selectedServicesOffered.push(
                            res.data._services_offered[i]
                        );
                    }

                    this.$nextTick(() => {
                        this.$bvModal.show("modal-associate-services");
                    });
                });
        },
        show_modal_confirm_association_services() {
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-associate-services");
            });
        },
        async associateServices() {
            let servicesIds = [];
            for (let i = 0; i < this.selectedServicesOffered.length; i++) {
                servicesIds.push(this.selectedServicesOffered[i].id);
            }
            let ids = {
                services_offered: servicesIds,
            };
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/organizationActivity/${this.activityId}/`,
                    ids,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.successMessage(
                        "¡Los servicios fuero asociados a la actividad exitosamente!"
                    );

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-associate-services");
                        this.$bvModal.hide("modal-associate-services");
                    });
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        async getServicesOffered() {
            this.servicesOffered = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/services/offered/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.servicesOffered = res.data;
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        async getRisks() {
            this.risks = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase1/risks/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.risks = res.data;
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        async getCrisisScenarioRisks() {
            this.crisisScenarioRisks = [];

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase1/crisis_scenarios_list_risks/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    for (let i = 0; i < res.data.length; i++) {
                        res.data[i].name =
                            "Escenario crítico: " + res.data[i].name;
                        this.crisisScenarioRisks.push(res.data[i]);
                    }
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        async show_modal_association_risks(id, name) {
            this.activityId = id;
            this.activityName = name;
            this.selectedRisks = [];

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase2/organizationActivity/${id}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    for (let i = 0; i < res.data._risks.length; i++) {
                        this.selectedRisks.push(res.data._risks[i]);
                    }

                    this.$nextTick(() => {
                        this.$bvModal.show("modal-associate-risks");
                    });
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        show_modal_confirm_association_risks() {
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-associate-risks");
            });
        },
        async associateRisks() {
            let risksIds = [];
            for (let i = 0; i < this.selectedRisks.length; i++) {
                risksIds.push(this.selectedRisks[i].id);
            }
            //Es necesario que el array de IDs tenga este nombre
            let ids = {
                risks: risksIds,
            };

            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/organizationActivity/${this.activityId}/`,
                    ids,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡Los riesgos fueron asociados al servicio contratado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-associate-risks");
                        this.$bvModal.hide("modal-associate-risks");
                    });
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        async getHeadquarters() {
            this.headquarters = [];

            axios
                .get(`${SERVER_ADDRESS}/api/config/headquarters/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.headquarters = res.data;
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            for (let e in err.response.data) {
                                this.errorMessage(
                                    e + ": " + err.response.data[e]
                                );
                            }
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
        },
        resetModal() {
            this.activity.name = "";
            this.activityState.name = null;
            this.activity.description = "";
            this.activityState.description = null;
            this.activity.cost = 0;
            this.activity.recovery_time = "";
            this.activity.criticality = 0;
            this.activityState.criticality = null;
            this.activity.scale = 0;
        },
    },
};
</script>

<style lang="scss">
</style>