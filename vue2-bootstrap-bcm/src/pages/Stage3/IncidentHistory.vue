<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="incidents"
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
                                'start_date',
                                'end_date',
                                'description',
                                'crisis_scenario_name',
                            ]"
                            :filters="filterGlobal"
                        >
                            <template #header>
                                <b-row class="justify-content-between">
                                    <b-col sm="4">
                                        <b-button
                                            v-if="
                                                is_superuser == true ||
                                                permissions.includes(
                                                    'bcm_phase3.add_incidenthistory'
                                                )
                                            "
                                            title="Crear incidente"
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
                            <Column
                                field="start_date"
                                header="Fecha de inicio"
                            ></Column>
                            <Column
                                field="start_hour"
                                header="Hora de inicio"
                            ></Column>
                            <Column
                                field="end_date"
                                header="Fecha fin"
                            ></Column>
                            <Column field="end_hour" header="Hora fin"></Column>
                            <Column
                                field="crisis_scenario_name"
                                header="Nombre del escenario crítico"
                            ></Column>
                            <Column
                                field="description"
                                header="Descripción del incidente"
                            ></Column>
                            <Column field="id" header="Opciones">
                                <template #body="slotProps">
                                    <b-button
                                        v-if="
                                            is_superuser == true ||
                                            permissions.includes(
                                                'bcm_phase3.change_incidenthistory'
                                            )
                                        "
                                        title="Editar incidencia"
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
                                        v-if="
                                            is_superuser == true ||
                                            permissions.includes(
                                                'bcm_phase3.delete_incidenthistory'
                                            )
                                        "
                                        title="Eliminar incidencia"
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
                                No hay incidentes encontrados.
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
            Modal de crear  
        -->
        <b-modal
            v-model="show_modal_create"
            id="modal-create"
            title="Crear incidente"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-row align-v="center">
                    <b-col>
                        <b-form-group
                            label="Ingrese la fecha de inicio del incidente"
                            invalid-feedback="Este campo es obligatorio"
                            :state="incidentState.start_date"
                        >
                            <b-form-datepicker
                                v-model="startDateTime.date"
                                :state="incidentState.start_date"
                                locale="es"
                            ></b-form-datepicker>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese la hora de inicio del incidente"
                            invalid-feedback="Este campo es obligatorio"
                            :state="incidentState.start_date"
                        >
                            <b-form-timepicker
                                v-model="startDateTime.time"
                                :state="incidentState.start_time"
                                now-button
                                reset-button
                                locale="es"
                            ></b-form-timepicker>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row align-v="center">
                    <b-col>
                        <b-form-group
                            label="Ingrese la fecha fin del incidente"
                            invalid-feedback="Este campo es obligatorio"
                            :state="incidentState.end_date"
                        >
                            <b-form-datepicker
                                v-model="endDateTime.date"
                                :state="incidentState.end_date"
                                locale="es"
                            ></b-form-datepicker>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese la hora fin del incidente"
                            invalid-feedback="Este campo es obligatorio"
                            :state="incidentState.end_date"
                        >
                            <b-form-timepicker
                                v-model="endDateTime.time"
                                :state="incidentState.end_time"
                                now-button
                                reset-button
                                locale="es"
                            ></b-form-timepicker>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-form-group
                    label="Seleccione el escenario crítico que ocasionará la incidencia"
                    invalid-feedback="Este campo es obligatorio"
                    :state="incidentState.crisis_scenario"
                >
                    <b-form-select
                        v-model="incident.crisis_scenario"
                        :options="crisisScenarios"
                        value-field="id"
                        text-field="name"
                        :state="incidentState.crisis_scenario"
                        required
                    ></b-form-select>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción del incidente"
                    :state="incidentState.description"
                >
                    <b-form-textarea
                        v-model="incident.description"
                        :state="incidentState.description"
                        required
                        rows="3"
                    ></b-form-textarea>
                </b-form-group>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitCreate"
                    >
                        Crear incidente
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear  
        -->
        <b-modal
            id="modal-confirm-create"
            title="Confirmar crear incidencia"
            centered
        >
            <h4>¿Está seguro de crear esta incidencia?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createIncident"
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
            title="Editar incidente"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-row align-v="center">
                    <b-col>
                        <b-form-group
                            label="Ingrese la fecha de inicio del incidente"
                            invalid-feedback="Este campo es obligatorio"
                            :state="incidentState.start_date"
                        >
                            <b-form-datepicker
                                v-model="startDateTime.date"
                                :state="incidentState.start_date"
                                locale="es"
                            ></b-form-datepicker>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese la hora de inicio del incidente"
                            invalid-feedback="Este campo es obligatorio"
                            :state="incidentState.start_date"
                        >
                            <b-form-timepicker
                                v-model="startDateTime.time"
                                :state="incidentState.start_time"
                                now-button
                                reset-button
                                locale="es"
                            ></b-form-timepicker>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row align-v="center">
                    <b-col>
                        <b-form-group
                            label="Ingrese la fecha fin del incidente"
                            invalid-feedback="Este campo es obligatorio"
                            :state="incidentState.end_date"
                        >
                            <b-form-datepicker
                                v-model="endDateTime.date"
                                :state="incidentState.end_date"
                                locale="es"
                            ></b-form-datepicker>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese la hora fin del incidente"
                            invalid-feedback="Este campo es obligatorio"
                            :state="incidentState.end_date"
                        >
                            <b-form-timepicker
                                v-model="endDateTime.time"
                                :state="incidentState.end_time"
                                now-button
                                reset-button
                                locale="es"
                            ></b-form-timepicker>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-form-group
                    label="Seleccione el escenario crítico que ocasionará la incidencia"
                    invalid-feedback="Este campo es obligatorio"
                    :state="incidentState.crisis_scenario"
                >
                    <b-form-select
                        v-model="incident.crisis_scenario"
                        :options="crisisScenarios"
                        value-field="id"
                        text-field="name"
                        :state="incidentState.crisis_scenario"
                        required
                    ></b-form-select>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción del incidente"
                    :state="incidentState.description"
                >
                    <b-form-textarea
                        v-model="incident.description"
                        :state="incidentState.description"
                        required
                        rows="3"
                    ></b-form-textarea>
                </b-form-group>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitUpdate"
                    >
                        Editar incidente
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
            <h4>¿Está seguro de editar este incidente?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="updateIncident"
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
            title="Confirmar eliminar incidente"
            centered
        >
            <h4>¿Está seguro de eliminar este incidente?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteIncident"
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

export default {
    name: "IncidentHistory",
    components: {
        Multiselect,
    },
    data: () => ({
        loading: false,
        filterGlobal: {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        },
        permissions: [],
        is_superuser: false,

        // Variables para manejar los modales
        show_modal_create: false,

        incidents: [],
        incidentId: 0,

        incident: {
            start_date: "",
            end_date: "",
            description: "",
            crisis_scenario: 0,
        },
        incidentState: {
            start_date: null,
            start_time: null,
            end_date: null,
            end_time: null,
            description: null,
            crisis_scenario: null,
        },
        startDateTime: {
            date: "",
            time: "",
        },
        endDateTime: {
            date: "",
            time: "",
        },
        crisisScenarios: [],
    }),
    mounted() {
        this.getIncidents();
        this.permissions = JSON.parse(localStorage.getItem("permissions"));
        this.is_superuser = localStorage.getItem("is_superuser");
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
        async getIncidents() {
            this.loading = true;
            this.incidents = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase3/incident-histories/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for (var i = 0; i < res.data.length; i++) {
                        let end_date = "";
                        let end_hour = "";
                        if (res.data[i].end_date) {
                            end_date = res.data[i].end_date.slice(0, 10);
                            end_hour = res.data[i].end_date.slice(11, 16);
                        }
                        let inc = {
                            id: res.data[i].id,
                            start_date: res.data[i].start_date.slice(0, 10),
                            start_hour: res.data[i].start_date.slice(11, 16),
                            end_date: end_date,
                            end_hour: end_hour,
                            description: res.data[i].description,
                            crisis_scenario_name:
                                res.data[i].crisis_scenario_name,
                        };
                        this.incidents.push(inc);
                    }
                    this.loading = false;

                    this.getCrisisScenarios();
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
                value: null,
                matchMode: FilterMatchMode.CONTAINS,
            };
        },

        async getCrisisScenarios() {
            this.crisisScenarios = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase1/crisis_scenarios_list/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.crisisScenarios = res.data;
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
         * Validar formularios
         */
        checkFormValidity() {
            let valid = true;
            if (!this.startDateTime.date) {
                this.incidentState.start_date = false;
                valid = false;
            }
            if (!this.startDateTime.time) {
                this.incidentState.start_time = false;
                valid = false;
            }
            if (this.endDateTime.date && !this.endDateTime.time) {
                this.incidentState.end_time = false;
                valid = false;
            }
            if (!this.endDateTime.date && this.endDateTime.time) {
                this.incidentState.end_date = false;
                valid = false;
            }
            /*
            if (!this.endDateTime.date) {
                this.incidentState.end_date = false;
                valid = false;
            }
            if (!this.endDateTime.time) {
                this.incidentState.end_time = false;
                valid = false;
            }
            */
            if (!this.incident.crisis_scenario) {
                this.incidentState.crisis_scenario = false;
                valid = false;
            }
            return valid;
        },
        resetModal() {
            this.incident.start_date = "";
            this.incidentState.start_date = null;
            this.incident.end_date = "";
            this.incidentState.end_date = null;
            this.incident.description = "";
            this.incidentState.description = null;
            this.incident.crisis_scenario = 0;
            this.incidentState.crisis_scenario = null;
        },
        /**
         * Create
         */
        handleSubmitCreate() {
            // Inicializamos variables de estados
            this.incidentState.start_date = null;
            this.incidentState.start_time = null;
            this.incidentState.end_date = null;
            this.incidentState.end_time = null;
            this.incidentState.description = null;
            this.incidentState.crisis_scenario = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create");
            });
        },
        async createIncident() {
            this.incident.start_date =
                this.startDateTime.date + " " + this.startDateTime.time;

            if (this.endDateTime.date && this.endDateTime.time) {
                this.incident.end_date =
                    this.endDateTime.date + " " + this.endDateTime.time;
            } else {
                this.incident.end_date = null;
            }

            axios
                .post(
                    `${SERVER_ADDRESS}/api/phase3/incident-histories/`,
                    this.incident,
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
                        "¡El incidente ha sido creado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    this.getIncidents();
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
            this.incidentState.start_date = null;
            this.incidentState.start_time = null;
            this.incidentState.end_date = null;
            this.incidentState.end_time = null;
            this.incidentState.description = null;
            this.incidentState.crisis_scenario = null;

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
            this.incidentId = id;

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase3/incident-history/${this.incidentId}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.incident = {
                        description: res.data.description,
                        crisis_scenario: res.data.crisis_scenario,
                    };
                    this.startDateTime = {
                        date: res.data.start_date.slice(0, 10),
                        time: res.data.start_date.slice(11, 16),
                    };
                    if (res.date.end_date) {
                        this.endDateTime = {
                            date: res.data.end_date.slice(0, 10),
                            time: res.data.end_date.slice(11, 16),
                        };
                    }

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
        async updateIncident() {
            this.incident.start_date =
                this.startDateTime.date + " " + this.startDateTime.time;

            if (this.endDateTime.date && this.endDateTime.time) {
                this.incident.end_date =
                    this.endDateTime.date + " " + this.endDateTime.time;
            } else {
                this.incident.end_date = null;
            }

            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase3/incident-history/${this.incidentId}/`,
                    this.incident,
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
                        "¡El incidente ha sido actualizado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });

                    // Cargamos de nuevo la tabla de escenario crítico
                    this.getIncidents();
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
        show_modal_delete(id) {
            this.incidentId = id;

            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
        async deleteIncident() {
            axios
                .delete(
                    `${SERVER_ADDRESS}/api/phase3/incident-history/${this.incidentId}/`,
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
                        "¡El incidente ha sido eliminado exitosamente!"
                    );
                    this.getIncidents();

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
    },
};
</script>
<style lang="scss">
</style>
