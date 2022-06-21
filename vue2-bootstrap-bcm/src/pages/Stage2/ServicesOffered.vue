<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="services"
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
                                'type_name',
                                'recovery_time',
                                'profit',
                                'criticality',
                                'area_name',
                            ]"
                            :filters="filterGlobal"
                        >
                            <template #header>
                                <b-row class="justify-content-between">
                                    <b-col sm="4">
                                        <b-button
                                            title="Crear servicio de la organización"
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
                            <Column field="type_name" header="Tipo"></Column>
                            <Column
                                field="recovery_time"
                                header="Tiempo de recuperación"
                            ></Column>
                            <Column field="profit" header="Ganancia">
                                <template #body="slotProps">
                                    {{ slotProps.data.profit }}$
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
                            <Column field="area_name" header="Area"></Column>
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
                                        title="Editar servicio de la organización"
                                        pill
                                        variant="warning"
                                        @click="
                                            show_modal_update(
                                                slotProps.data.id,
                                                slotProps.data.type_name
                                            )
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-pen-to-square"
                                        />
                                    </b-button>
                                    <b-button
                                        title="Eliminar servicio de la organización"
                                        pill
                                        variant="danger"
                                        @click="
                                            show_modal_delete(
                                                slotProps.data.id,
                                                slotProps.data.type_name
                                            )
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-trash"
                                        />
                                    </b-button>
                                </template>
                            </Column>
                            <Column field="id_2" header="Asociar personal">
                                <template #body="slotProps">
                                    <div class="text-center">
                                        <b-button
                                            pill
                                            title="Asociar personal de la organización encargado"
                                            variant="primary"
                                            @click="
                                                show_modal_association_staffs(
                                                    slotProps.data.id,
                                                    slotProps.data.name
                                                )
                                            "
                                        >
                                            <font-awesome-icon
                                                icon="fa-solid fa-users"
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
            title="Detalle del servicio de la organización"
            ref="modal"
            size="lg"
            centered
        >
            <h3 class="text-center font-weight-bold">
                {{ serviceDetail.name }}
            </h3>
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <strong>Tipo: </strong>{{ serviceDetail.type_name }}
                </li>
                <li class="list-group-item">
                    <strong>Ganancia promedio: </strong
                    >{{ serviceDetail.profit }}$
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
                <li class="list-group-item">
                    <strong>Area: </strong>{{ serviceDetail.area_name }}
                </li>
            </ul>
            <h4 class="mt-5 text-center font-weight-bold">
                Personal de la organización encargado en el servicio
            </h4>
            <b-list-group-item
                class="mt-2 flex-column align-items-start"
                v-for="item in serviceDetail._staffs"
                :key="item.key"
            >
                <div class="d-flex w-100 justify-content-between">
                    <h5 class="mb-1">{{ item.names }} {{ item.surnames }}</h5>
                    <small class="text-muted"
                        >Número de staff: {{ item.staff_number }}
                    </small>
                </div>
                <div class="mb-1 d-flex w-100 justify-content-between">
                    <div>Area: {{ item.area_name }}</div>
                    <div>Cargo: {{ item.position_name }}</div>
                    <div>Sede: {{ item.headquarter_name }}</div>
                </div>
            </b-list-group-item>
            <h3 class="mt-3 text-center" v-if="!serviceDetail._staffs.length">
                No existe personal de la organización encargado en este servicio
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
            title="Crear servicio de la organización"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-form-group
                    label="Ingrese el título del servicio de la organización"
                    invalid-feedback="Este campo es obligatorio"
                    :state="serviceState.name"
                >
                    <b-form-input
                        v-model="service.name"
                        :state="serviceState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Seleccione el tipo"
                            invalid-feedback="Este campo es obligatorio"
                            :state="serviceState.type"
                        >
                            <b-form-select
                                v-model="service.type"
                                :options="types"
                                value-field="value"
                                text-field="name"
                                :state="serviceState.type"
                                required
                            ></b-form-select>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese la ganacia (en dólares)"
                            invalid-feedback="La ganancia no puede ser negativa ni cero"
                            :state="serviceState.profit"
                        >
                            <b-form-input
                                type="number"
                                v-model.number="service.profit"
                                :state="serviceState.profit"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
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
                            label="Seleccione el área asociada a este servicio de la organización"
                            invalid-feedback="Este campo es obligatorio"
                            :state="serviceState.area"
                        >
                            <b-form-select
                                v-model="service.area"
                                :options="areas"
                                value-field="id"
                                text-field="name"
                                :state="serviceState.area"
                                required
                            ></b-form-select>
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
                        Crear servicio de la organización
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear  
        -->
        <b-modal
            id="modal-confirm-create"
            title="Confirmar crear servicio de la organización"
            centered
        >
            <h4>¿Está seguro de crear este {{ type }} ofrecido?</h4>
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
            title="Editar servicio de la organización"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-form-group
                    label="Ingrese el título del servicio de la organización"
                    invalid-feedback="Este campo es obligatorio"
                    :state="serviceState.name"
                >
                    <b-form-input
                        v-model="service.name"
                        :state="serviceState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Seleccione el tipo"
                            invalid-feedback="Este campo es obligatorio"
                            :state="serviceState.type"
                        >
                            <b-form-select
                                v-model="service.type"
                                :options="types"
                                value-field="value"
                                text-field="name"
                                :state="serviceState.type"
                                required
                            ></b-form-select>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese la ganacia (en dólares)"
                            invalid-feedback="La ganancia no puede ser negativa ni cero"
                            :state="serviceState.profit"
                        >
                            <b-form-input
                                type="number"
                                v-model.number="service.profit"
                                :state="serviceState.profit"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
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
                            label="Seleccione el área asociada a este servicio de la organización"
                            invalid-feedback="Este campo es obligatorio"
                            :state="serviceState.area"
                        >
                            <b-form-select
                                v-model="service.area"
                                :options="areas"
                                value-field="id"
                                text-field="name"
                                :state="serviceState.area"
                                required
                            ></b-form-select>
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
            title="Confirmar editar servicio de la organización"
            centered
        >
            <h4>¿Está seguro de editar este {{ type }} ofrecido?</h4>
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
            title="Confirmar eliminar servicio de la organización"
            centered
        >
            <h4>¿Está seguro de eliminar este {{ type }} ofrecido?</h4>
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
            Modal de asociar staff de la organización con servicios de la organización  
        -->
        <b-modal
            id="modal-associate-staffs"
            title="Personal de la organización encargado de los servicios de la organización"
            ref="modal"
            size="lg"
            centered
        >
            <multiselect
                v-model="selectedStaffs"
                placeholder="Buscar personal de la organización"
                label="names"
                track-by="id"
                :options="staffs"
                :multiple="true"
            ></multiselect>

            <b-list-group v-if="selectedStaffs.length" class="mt-3">
                <b-list-group-item
                    href="#"
                    class="flex-column align-items-start"
                    v-for="item in selectedStaffs"
                    :key="item.key"
                >
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">
                            {{ item.names }}
                        </h5>
                        <small class="text-muted"
                            >Número de staff: {{ item.staff_number }}</small
                        >
                    </div>
                    <div class="mb-1 d-flex w-100 justify-content-between">
                        <div>Area: {{ item.area_name }}</div>
                        <div>Cargo: {{ item.position_name }}</div>
                        <div>Sede: {{ item.headquarter_name }}</div>
                    </div>
                </b-list-group-item>
            </b-list-group>

            <h3 class="mt-3 text-center" v-if="!selectedStaffs.length">
                No existe personal de la organización encargado e este servicio
                de la organización
            </h3>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="primary"
                        class="float-right"
                        @click="show_modal_confirm_association_staffs"
                    >
                        Asociar personal de la organización
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar asociar servicios  
        -->
        <b-modal
            id="modal-confirm-associate-staffs"
            title="Confirmar personal de la organización"
            centered
        >
            <h4>
                ¿Está seguro de asociar este personal de la organización al
                servicio
                <strong>{{ serviceName }}</strong
                >?
            </h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="primary"
                        class="float-right"
                        @click="associateStaffs"
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
    name: "ServicesOffered",
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

        services: [],
        serviceDetail: {
            name: "",
            type_name: "",
            profit: 0,
            recovery_time: "",
            criticality: 0,
            area_name: "",
            scale_name: "",
            scale_min_value: 0,
            scale_max_value: 0,
            _staffs: [],
        },
        serviceId: 0,
        serviceName: "",
        type: "",

        service: {
            name: "",
            type: 0,
            profit: 0,
            recovery_time: "",
            criticality: 0,
            area: 0,
            scale: 0,
        },
        serviceState: {
            name: null,
            type: null,
            profit: null,
            area: null,
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
        areas: [],
        types: [
            {
                value: 1,
                name: "Producto",
            },
            {
                value: 2,
                name: "Servicio",
            },
            {
                value: 3,
                name: "Proceso",
            },
        ],
        // Variable en la que se maneja la escala de la vista
        scaleView: {
            id: 0,
            name: "",
            scale: 0,
            scale_name: "",
            scale_min_value: 0,
            scale_max_value: 0,
        },

        // Lista de staffs de la organización para realizar la asociación
        staffs: [],
        selectedStaffs: [],
    }),
    mounted() {
        this.getServicesOffered();
        this.getAreas();
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
        async getAreas() {
            this.areas = [];
            axios
                .get(`${SERVER_ADDRESS}/api/config/areas/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.areas = res.data;
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
        async getScaleView() {
            axios
                .get(`${SERVER_ADDRESS}/api/config/scales/view/`, {
                    params: { name: "Servicios Ofrecidos" },
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
            this.loading = true;
            this.services = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/services/offered/`, {
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
                        this.services.push(res.data[i]);
                    }
                    this.loading = false;

                    // Mientras tanto vamos cargando el staff
                    this.getStaffs();
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

        /**
         * Validar formularios
         */
        checkFormValidity() {
            let valid = true;
            if (!this.service.name) {
                this.serviceState.name = false;
                valid = false;
            }
            if (this.service.area == 0) {
                this.serviceState.area = false;
                valid = false;
            }
            if (this.service.type == 0) {
                this.serviceState.type = false;
                valid = false;
            }
            if (this.service.profit <= 0) {
                this.serviceState.profit = false;
                valid = false;
            }
            return valid;
        },
        resetModal() {
            this.service.name = "";
            this.serviceState.name = null;
            this.service.type = 0;
            this.serviceState.type = null;
            this.service.profit = 0;
            this.serviceState.profit = null;
            this.service.area = 0;
            this.serviceState.area = null;
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
                type_name: "",
                profit: 0,
                recovery_time: "",
                criticality: 0,
                area_name: "",
                scale_name: "",
                scale_min_value: 0,
                scale_max_value: 0,
                _staffs: [],
            };

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/service/offered/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.serviceDetail = res.data;
                    this.serviceDetail.recovery_time = getRecoveryTimeText(
                        this.serviceDetail.recovery_time
                    );

                    this.$nextTick(() => {
                        this.$bvModal.show("modal-detail");
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

        /**
         * Create
         */
        handleSubmitCreate() {
            // Inicializamos variables de estados
            this.serviceState.name = null;
            this.serviceState.type = null;
            this.serviceState.profit = null;
            this.serviceState.area = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            if (this.service.type == 1) this.type = "producto";
            else if (this.service.type == 2) this.type = "servicio";
            else this.type = "proceso";

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
                    `${SERVER_ADDRESS}/api/phase2/services/offered/`,
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
                    let successType = "";
                    if (this.service.type == 1) successType = "producto";
                    else if (this.service.type == 2) successType = "servicio";
                    else successType = "proceso";

                    this.successMessage(
                        "¡El " + successType + " ha sido creado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    this.getServicesOffered();
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
         * Update
         */
        handleSubmitUpdate() {
            // Inicializamos variables de estados
            this.serviceState.name = null;
            this.serviceState.type = null;
            this.serviceState.profit = null;
            this.serviceState.area = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            if (this.service.type == 1) this.type = "producto";
            else if (this.service.type == 2) this.type = "servicio";
            else this.type = "proceso";

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-update");
            });
        },
        show_modal_update(id, type_name) {
            this.serviceId = id;
            this.type = type_name;

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase2/service/offered/${this.serviceId}/`,
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
        async updateService() {
            this.service.recovery_time = setRecoveryTime(this.duration);
            this.service.scale = this.scaleView.scale;

            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/service/offered/${this.serviceId}/`,
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
                    let successType = "";
                    if (this.service.type == 1) successType = "producto";
                    else if (this.service.type == 2) successType = "servicio";
                    else successType = "proceso";

                    this.successMessage(
                        "¡El " +
                            successType +
                            " ha sido actualizado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });

                    // Cargamos de nuevo la tabla de escenario crítico
                    this.getServicesOffered();
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
         * Delete
         */
        show_modal_delete(id, type_name) {
            this.serviceId = id;
            this.type = type_name;

            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
        async deleteService() {
            axios
                .delete(
                    `${SERVER_ADDRESS}/api/phase2/service/offered/${this.serviceId}/`,
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
                        "¡El " +
                            toString(type) +
                            " ha sido eliminado exitosamente!"
                    );
                    this.getServicesOffered();

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

        /**
         * Associate staff
         */
        async getStaffs() {
            this.staffs = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/staffs/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for (let i = 0; i < res.data.length; i++) {
                        res.data[i].names =
                            res.data[i].names + " " + res.data[i].surnames;
                        this.staffs.push(res.data);
                    }
                    this.staffs = res.data;
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
        async show_modal_association_staffs(id, name) {
            this.serviceId = id;
            this.serviceName = name;
            this.selectedStaffs = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/service/offered/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for (let i = 0; i < res.data._staffs.length; i++) {
                        res.data._staffs[i].names =
                            res.data._staffs[i].names +
                            " " +
                            res.data._staffs[i].surnames;
                        this.selectedStaffs.push(res.data._staffs[i]);
                    }

                    this.$nextTick(() => {
                        this.$bvModal.show("modal-associate-staffs");
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
        show_modal_confirm_association_staffs() {
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-associate-staffs");
            });
        },
        async associateStaffs() {
            let staffsIds = [];
            for (let i = 0; i < this.selectedStaffs.length; i++) {
                staffsIds.push(this.selectedStaffs[i].id);
            }
            //Es necesario que el array de IDs tenga este nombre
            let ids = {
                staffs: staffsIds,
            };

            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/service/offered/${this.serviceId}/`,
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
                        this.$bvModal.hide("modal-confirm-associate-staffs");
                        this.$bvModal.hide("modal-associate-staffs");
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
    },
};
</script>
<style lang="scss">
</style>
