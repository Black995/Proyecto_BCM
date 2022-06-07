<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="risks"
                            responsiveLayout="scroll"
                            :paginator="true"
                            :rows="10"
                            :rowsPerPageOptions="[10, 20]"
                            :resizableColumns="true"
                            :autoLayout="true"
                            :responsive="true"
                            :reorderableColumns="true"
                            :loading="loading"
                            :globalFilterFields="['name', 'description']"
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
                                                v-model="filterGlobal"
                                                placeholder="Buscar..."
                                            />
                                        </span>
                                    </b-col>
                                </b-row>
                            </template>
                            <Column field="name" header="Nombre"></Column>
                            <Column
                                field="description"
                                header="Descripción"
                            ></Column>
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
                                No hay riesgos encontrados.
                            </template>
                        </DataTable>
                    </div>
                    <!-- /.card-body -->
                </div>
                <!-- /.card -->
            </div>
            <!-- /.col -->
        </div>

        <!--
            Modal de crear  
        -->
        <b-modal
            v-model="show_modal_create"
            id="modal-create"
            title="Crear riesgo"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-form-group
                    label="Ingrese el título del riesgo"
                    label-for="name-input-create"
                    invalid-feedback="Este campo es obligatorio"
                    :state="riskState.name"
                >
                    <b-form-input
                        id="name-input"
                        v-model="risk.name"
                        :state="riskState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción del riesgo"
                    label-for="description-input-create"
                    invalid-feedback="Este campo es obligatorio"
                    :state="riskState.description"
                >
                    <b-form-textarea
                        id="name-input"
                        v-model="risk.description"
                        :state="riskState.description"
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
                        Crear riesgo
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear  
        -->
        <b-modal
            id="modal-confirm-create"
            title="Confirmar crear riesgo"
            centered
        >
            <h4>¿Está seguro de crear este riesgo?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createRisk"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de actualizar  
        -->
        <b-modal
            id="modal-update"
            title="Editar riesgo"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-form-group
                    label="Ingrese el título del riesgo"
                    label-for="name-input-update"
                    invalid-feedback="Este campo es obligatorio"
                    :state="riskState.name"
                >
                    <b-form-input
                        id="name-input"
                        v-model="risk.name"
                        :state="riskState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción del riesgo"
                    label-for="description-input-update"
                    invalid-feedback="Este campo es obligatorio"
                    :state="riskState.description"
                >
                    <b-form-textarea
                        id="name-input"
                        v-model="risk.description"
                        :state="riskState.description"
                        required
                        rows="3"
                    ></b-form-textarea>
                </b-form-group>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitUpdate"
                    >
                        Editar riesgo
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar actualizar  
        -->
        <b-modal
            id="modal-confirm-update"
            title="Confirmar actualizar riesgo"
            centered
        >
            <h4>¿Está seguro de actualizar este riesgo?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="updateRisk"
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
            title="Confirmar eliminar riesgo"
            centered
        >
            <h4>¿Está seguro de eliminar este riesgo?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteRisk"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--Stats cards-->
        <!--div class="row">
          <div class="col-md-6 col-xl-3" v-for="stats in statsCards" :key="stats.title">
            <stats-card>
              <div class="icon-big text-center" :class="`icon-${stats.type}`" slot="header">
                <i :class="stats.icon"></i>
              </div>
              <div class="numbers" slot="content">
                <p>{{stats.title}}</p>
                {{stats.value}}
              </div>
              <div class="stats" slot="footer">
                <i :class="stats.footerIcon"></i> {{stats.footerText}}
              </div>
            </stats-card>
          </div>
        </div-->
        <!--Charts-->
        <div class="row"></div>
        <!-- /.row -->
    </div>
</template>
<script>
//import { StatsCard } from "@/components/index";
/**
 * El ejemplo de Stats Cards puede servir para futuras versiones del sistema
 */
// import Chartist from 'chartist';

import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import { FilterMatchMode } from "primevue/api";

import NotificationTemplate from "../Notifications/NotificationTemplate";

export default {
    name: "Risks",

    data: () => ({
        loading: false,
        filterGlobal: null,

        // Variables para maanejar los modales
        show_modal_create: false,

        risks: [],
        riskId: 0,

        risk: {
            name: "",
            description: "",
        },
        riskState: {
            name: null,
            description: null,
        },
    }),
    mounted() {
        this.getRisks();
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
        async getRisks() {
            this.loading = true;
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
                    this.loading = false;
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
                value: null,
                matchMode: FilterMatchMode.CONTAINS,
            };
        },

        /**
         * Validar formularios
         */
        checkFormValidity() {
            /*
            const valid = this.$refs.form.checkValidity();
            this.riskState.name = valid;
            this.riskState.description = valid;
            return valid;
            */
            let valid = true;
            if (!this.risk.name) {
                this.riskState.name = false;
                valid = false;
            }
            if (!this.risk.description) {
                this.riskState.description = false;
                valid = false;
            }
            return valid;
        },
        resetModal() {
            this.risk.name = "";
            this.riskState.name = null;
            this.risk.description = "";
            this.riskState.description = null;
        },
        /**
         * Create
         */
        handleSubmitCreate() {
            // Inicializamos variables de estados
            this.riskState.name = null;
            this.riskState.description = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create");
            });
        },
        async createRisk() {
            axios
                .post(`${SERVER_ADDRESS}/api/phase1/risks/`, this.risk, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "El riesgo ha sido creado exitosamente"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getRisks();
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
            this.riskState.name = null;
            this.riskState.description = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-update");
            });
        },
        async show_modal_update(id) {
            this.riskId = id;

            axios
                .get(`${SERVER_ADDRESS}/api/phase1/risk/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.risk = res.data;
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
        async updateRisk() {
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase1/risk/${this.riskId}/`,
                    this.risk,
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
                        "El riesgo ha sido actualizado exitosamente"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getRisks();
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
            this.riskId = id;
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
        async deleteRisk() {
            axios
                .delete(`${SERVER_ADDRESS}/api/phase1/risk/${this.riskId}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "El riesgo ha sido eliminado exitosamente"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-delete");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getRisks();
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

    /**
     * Ejemplo con data para las tarjetas del comienzo
     */
    /*
    components: {
        StatsCard,
    },
    data() {
        return {
      statsCards: [
        {
          type: "warning",
          icon: "ti-server",
          title: "Capacity",
          value: "105GB",
          footerText: "Updated now",
          footerIcon: "ti-reload"
        },
        {
          type: "success",
          icon: "ti-wallet",
          title: "Revenue",
          value: "$1,345",
          footerText: "Last day",
          footerIcon: "ti-calendar"
        },
        {
          type: "danger",
          icon: "ti-pulse",
          title: "Errors",
          value: "23",
          footerText: "In the last hour",
          footerIcon: "ti-timer"
        },
        {
          type: "info",
          icon: "ti-twitter-alt",
          title: "Followers",
          value: "+45",
          footerText: "Updated now",
          footerIcon: "ti-reload"
        }
      ],
      };
    },
      */
};
</script>
<style lang="scss">
.header-table {
    background-color: rgb(17, 17, 17);
    color: rgb(255, 255, 255);
}
</style>
