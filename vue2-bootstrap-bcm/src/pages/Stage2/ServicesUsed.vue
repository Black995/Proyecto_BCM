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

        services: [],
        serviceId: 0,

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
                    params: { name: "Servicios Usados" },
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
            this.services = [];

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
                        this.services.push(res.data[i]);
                    }
                    this.loading = false;
                })
                .catch((err) => {
                    console.log(err);
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
         * Create
         */

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
        show_modal_update(id) {},

        /**
         * Delete
         */
        show_modal_delete(id) {
            this.serviceId = id;

            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
    },
};
</script>
<style lang="scss">
</style>
