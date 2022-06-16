<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="servicesUsed"
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
                                'recovery_time',
                                'spending',
                                'criticality',
                            ]"
                            :filters="filterGlobal"
                        >
                            <template #header>
                                <b-row class="justify-content-between">
                                    <b-col sm="4">
                                        <b-button
                                            title="Crear servicio"
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
                                </b-row>
                            </template>
                            <Column field="name" header="Nombre"></Column>
                            <Column
                                field="recovery_time"
                                header="Tiempo de recuperación"
                            ></Column>
                            <Column field="spending" header="Gasto">
                                <template #body="slotProps">
                                    {{ slotProps.data.spending }}$
                                </template>
                            </Column>
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
                                        title="Detalle del servicio"
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
                                        title="Editar servicio"
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
                                        title="Eliminar servicio"
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
                                No hay servicios encontrados.
                            </template>
                        </DataTable>
                    </div>
                    <!-- /.card-body -->
                </div>
                <!-- /.card -->
            </div>
            <!-- /.col -->
        </div>
        <div class="row"></div>

        <!--
            Modal del detalle  
        -->
        <b-modal
            id="modal-detail"
            title="Detalle del servicio"
            ref="modal"
            size="lg"
            centered
        >
            <h3 class="text-center font-weight-bold">
                {{ serviceDetail.name }}
            </h3>
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <strong>Costo: </strong>{{ serviceDetail.spending }}
                </li>
                <li class="list-group-item">
                    <strong>Tiempo de recuperación: </strong
                    >{{ serviceDetail.recovery_time }}
                </li>
                <li class="list-group-item">
                    <div v-if="!serviceDetail.scale_max_value">
                        <strong>Criticidad: </strong
                        >{{ serviceDetail.criticality }}
                    </div>
                    <div v-if="serviceDetail.scale_max_value">
                        <strong>Criticidad: </strong
                        >{{ serviceDetail.criticality }}/{{
                            serviceDetail.scale_max_value
                        }}
                    </div>
                </li>
            </ul>
            <h4 class="mt-5 text-center font-weight-bold">
                Servicios de la organización usados por el servicio contratado
            </h4>
            <b-list-group-item
                class="mt-2 flex-column align-items-start"
                v-for="item in serviceDetail._services_offered"
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
                v-if="!serviceDetail._services_offered.length"
            >
                No existen servicios de la organización asociados a este
                servicio contratado
            </h3>

            <h4 class="mt-5 text-center font-weight-bold">
                Riesgos del servicios de la organización
            </h4>
            <b-list-group-item
                class="mt-2 flex-column align-items-start"
                v-for="item in serviceDetail._risks"
                :key="item.key"
            >
                <h5 class="mb-1">{{ item.name }}</h5>
                <p class="mb-1">Descripción: {{ item.description }}</p>
            </b-list-group-item>
            <h3
                class="mt-3 text-center"
                v-if="!serviceDetail._services_offered.length"
            >
                No existen riesgos asociados a este servicio contratado
            </h3>

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
            title="Crear servicio"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-form-group
                    label="Ingrese el título del servicio"
                    invalid-feedback="Este campo es obligatorio"
                    :state="serviceState.name"
                >
                    <b-form-input
                        v-model="service.name"
                        :state="serviceState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-row align-v="center">
                    <b-col>
                        <b-form-group
                            label="Tiempo de recuperación"
                            invalid-feedback="Este campo es obligatorio"
                        >
                            <b-row cols="1" cols-sm="3" cols-md="3" cols-lg="3">
                                <b-col>
                                    <b-form-group label="Días">
                                        <b-form-input
                                            type="number"
                                            v-model.number="duration.days"
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
                            label="Ingrese el costo (en dólares)"
                            invalid-feedback="El costo no puede ser negativa ni cero"
                            :state="serviceState.spending"
                        >
                            <b-form-input
                                type="number"
                                v-model.number="service.spending"
                                :state="serviceState.spending"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-form-group label="Ingrese la criticidad">
                    <b-form-spinbutton
                        v-model.number="service.criticality"
                        :min="scaleView.scale_min_value"
                        :max="scaleView.scale_max_value"
                    ></b-form-spinbutton>
                </b-form-group>
                <b-row>
                    <b-col>
                        <p class="mb-1">
                            <strong
                                >Escala a utilizar para la criticidad: </strong
                            >{{ scaleView.scale_name }}
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
                        Crear servicio
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear  
        -->
        <b-modal
            id="modal-confirm-create"
            title="Confirmar crear servicio"
            centered
        >
            <h4>¿Está seguro de crear este servicio?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createService"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de editar  
        -->
        <b-modal
            id="modal-update"
            title="Editar servicio"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-form-group
                    label="Ingrese el título del servicio"
                    invalid-feedback="Este campo es obligatorio"
                    :state="serviceState.name"
                >
                    <b-form-input
                        v-model="service.name"
                        :state="serviceState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-row align-v="center">
                    <b-col>
                        <b-form-group
                            label="Tiempo de recuperación"
                            invalid-feedback="Este campo es obligatorio"
                        >
                            <b-row cols="1" cols-sm="3" cols-md="3" cols-lg="3">
                                <b-col>
                                    <b-form-group label="Días">
                                        <b-form-input
                                            type="number"
                                            v-model.number="duration.days"
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
                            label="Ingrese el costo (en dólares)"
                            invalid-feedback="El costo no puede ser negativa ni cero"
                            :state="serviceState.spending"
                        >
                            <b-form-input
                                type="number"
                                v-model.number="service.spending"
                                :state="serviceState.spending"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-form-group label="Ingrese la criticidad">
                    <b-form-spinbutton
                        v-model.number="service.criticality"
                        :min="scaleView.scale_min_value"
                        :max="scaleView.scale_max_value"
                    ></b-form-spinbutton>
                </b-form-group>
                <b-row>
                    <b-col>
                        <p class="mb-1">
                            <strong
                                >Escala a utilizar para la criticidad: </strong
                            >{{ scaleView.scale_name }}
                        </p>
                    </b-col>
                </b-row>
            </form>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitUpdate"
                    >
                        Editar servicio
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar editar  
        -->
        <b-modal
            id="modal-confirm-update"
            title="Confirmar editar servicio"
            centered
        >
            <h4>¿Está seguro de editar este servicio?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="updateService"
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
            title="Confirmar eliminar servicio"
            centered
        >
            <h4>¿Está seguro de eliminar este servicio?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteService"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de asociar servicios de la organización con servicios contratado  
        -->
        <b-modal
            id="modal-associate-services"
            title="Asociar servicios de la organización con servicios contratados"
            ref="modal"
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
                ¿Está seguro de asociar estos servicios de la organización al
                servicio
                <strong>{{ serviceName }}</strong
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
            ref="modal"
            size="lg"
            centered
        >
            <!--multiselect
                v-model="selectedRisks"
                placeholder="Buscar riesgos"
                label="name"
                track-by="id"
                :options="risks"
                :multiple="true"
            ></multiselect-->
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
                ¿Está seguro de asociar estos riesgos al servicio
                <strong>{{ serviceName }}</strong
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
    name: "ServicesUsed",
    components: {
        Multiselect,
    },
    data: () => ({
        loading: false,
        filterGlobal: {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        },

        // Variables para manejar los modales
        show_modal_create: false,

        servicesUsed: [],
        serviceDetail: {
            name: "",
            spending: 0,
            recovery_time: "",
            criticality: 0,
            scale_name: "",
            scale_min_value: 0,
            scale_max_value: 0,
            _services_offered: [],
            _risks: [],
        },
        serviceId: 0,
        serviceName: "",

        service: {
            name: "",
            spending: 0,
            recovery_time: "",
            criticality: 0,
            scale: 0,
        },
        serviceState: {
            name: null,
            spending: null,
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

        // Lista de servicios de la organización para realizar la asociación
        servicesOffered: [],
        selectedServicesOffered: [],
        // Lista de riesgos para realizar la asociación
        risks: [],
        selectedRisks: [],
        crisisScenarioRisks: [],
    }),
    mounted() {
        this.getServicesUsed();
        this.getScaleView();
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
                icon: "ti-check",
                horizontalAlign: "right",
                verticalAlign: "top",
                type: "danger",
            });
        },
        async getScaleView() {
            axios
                .get(`${SERVER_ADDRESS}/api/config/scales/view/`, {
                    params: { name: "Servicios Contratados" },
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
                    this.service.criticality = res.data[0].scale_min_value;
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(err.response.data);
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

        async getServicesUsed() {
            this.loading = true;
            this.servicesUsed = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/services/used/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for (var i = 0; i < res.data.length; i++) {
                        //Convertimos en texto la duración
                        res.data[i].recovery_time = getRecoveryTimeText(
                            res.data[i].recovery_time
                        );
                        this.servicesUsed.push(res.data[i]);
                    }
                    this.loading = false;

                    // Mientras tanto vamos cargando la lista de servicios de la organización y riesgos
                    this.getServicesOffered();
                    this.getRisks();
                    this.getCrisisScenarioRisks();
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(err.response.data);
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

        /**
         * Validar formularios
         */
        checkFormValidity() {
            let valid = true;
            if (!this.service.name) {
                this.serviceState.name = false;
                valid = false;
            }
            if (this.service.spending <= 0) {
                this.serviceState.spending = false;
                valid = false;
            }
            return valid;
        },
        resetModal() {
            this.service.name = "";
            this.serviceState.name = null;
            this.service.spending = 0;
            this.serviceState.spending = null;
            this.service.criticality = this.scaleView.scale_min_value;

            this.duration.days = 0;
            this.duration.hours = 0;
            this.duration.minutes = 0;
        },

        /**
         * Detail
         */
        async show_modal_detail(id) {
            this.serviceDetail = {
                name: "",
                spending: 0,
                recovery_time: "",
                criticality: 0,
                scale_name: "",
                scale_min_value: 0,
                scale_max_value: 0,
                _services_offered: [],
            };

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/service/used/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.serviceDetail = res.data;

                    this.$nextTick(() => {
                        this.$bvModal.show("modal-detail");
                    });
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(err.response.data);
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
         * Create
         */
        handleSubmitCreate() {
            // Inicializamos variables de estados
            this.serviceState.name = null;
            this.serviceState.spending = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create");
            });
        },
        async createService() {
            this.service.recovery_time = setRecoveryTime(this.duration);
            this.service.scale = this.scaleView.scale;

            axios
                .post(
                    `${SERVER_ADDRESS}/api/phase2/services/used/`,
                    this.service,
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
                        "¡El servicio ha sido creado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    this.getServicesUsed();
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(err.response.data);
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
         * Update
         */
        handleSubmitUpdate() {
            // Inicializamos variables de estados
            this.serviceState.name = null;
            this.serviceState.spending = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-update");
            });
        },

        /**
         * Update
         */
        handleSubmitUpdate() {
            // Inicializamos variables de estados
            this.serviceState.name = null;
            this.serviceState.spending = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-update");
            });
        },
        show_modal_update(id) {
            this.serviceId = id;

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase2/service/used/${this.serviceId}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.service = res.data;
                    this.duration = getRecoveryTime(res.data.recovery_time);
                    this.$nextTick(() => {
                        this.$bvModal.show("modal-update");
                    });
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(err.response.data);
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
        async updateService() {
            this.service.recovery_time = setRecoveryTime(this.duration);
            this.service.scale = this.scaleView.scale;

            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/service/used/${this.serviceId}/`,
                    this.service,
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
                        "¡El servicio ha sido actualizado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });

                    this.getServicesUsed();
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(err.response.data);
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
         * Delete
         */
        show_modal_delete(id) {
            this.serviceId = id;

            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
        async deleteService() {
            axios
                .delete(
                    `${SERVER_ADDRESS}/api/phase2/service/used/${this.serviceId}/`,
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
                        "¡El servicio ha sido eliminado exitosamente!"
                    );
                    this.getServicesUsed();

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-delete");
                    });
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(err.response.data);
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
         * Associate services offered
         */
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
                            this.errorMessage(err.response.data);
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
            this.serviceId = id;
            this.serviceName = name;
            this.selectedServicesOffered = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/service/used/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
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
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(err.response.data);
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
            //Es necesario que el array de IDs tenga este nombre
            let ids = {
                services_offered: servicesIds,
            };

            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/service/used/${this.serviceId}/`,
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
                        "¡Los servicios de la organización fueron asociados al servicio contratado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-associate-services");
                        this.$bvModal.hide("modal-associate-services");
                    });
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(err.response.data);
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
                            this.errorMessage(err.response.data);
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
                            this.errorMessage(err.response.data);
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
            this.serviceId = id;
            this.serviceName = name;
            this.selectedRisks = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/service/used/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
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
                            this.errorMessage(err.response.data);
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
            console.log("riesgos seleccionados");
            console.log(this.selectedRisks);
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
                    `${SERVER_ADDRESS}/api/phase2/service/used/${this.serviceId}/`,
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
                            this.errorMessage(err.response.data);
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
    },
};
</script>
<style lang="scss">
</style>
