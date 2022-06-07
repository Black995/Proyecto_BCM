<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="crisisScenarios"
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
                                    <b-button
                                        pill
                                        variant="primary"
                                        @click="
                                            show_modal_association(
                                                slotProps.data.id
                                            )
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-clipboard-list"
                                        />
                                    </b-button>
                                </template>
                            </Column>

                            <template #empty>
                                No hay escenarios críticos encontrados.
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
            title="Crear escenario crítico"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-form-group
                    label="Ingrese el título del escenario crítico"
                    label-for="name-input-create"
                    invalid-feedback="Este campo es obligatorio"
                    :state="crisisState.name"
                >
                    <b-form-input
                        id="name-input"
                        v-model="crisisScenario.name"
                        :state="crisisState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción del escenario crítico"
                    label-for="description-input-create"
                    invalid-feedback="Este campo es obligatorio"
                    :state="crisisState.description"
                >
                    <b-form-textarea
                        id="name-input"
                        v-model="crisisScenario.description"
                        :state="crisisState.description"
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
                        Crear escenario crítico
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear  
        -->
        <b-modal
            id="modal-confirm-create"
            title="Confirmar crear escenario crítico"
            centered
        >
            <h4>¿Está seguro de crear este escenario crítico?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createCrisisScenario"
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
            title="Editar escenario crítico"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-form-group
                    label="Ingrese el título del escenario crítico"
                    label-for="name-input-update"
                    invalid-feedback="Este campo es obligatorio"
                    :state="crisisState.name"
                >
                    <b-form-input
                        id="name-input"
                        v-model="crisisScenario.name"
                        :state="crisisState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción del escenario crítico"
                    label-for="description-input-update"
                    invalid-feedback="Este campo es obligatorio"
                    :state="crisisState.description"
                >
                    <b-form-textarea
                        id="name-input"
                        v-model="crisisScenario.description"
                        :state="crisisState.description"
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
                        Editar escenario crítico
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar actualizar  
        -->
        <b-modal
            id="modal-confirm-update"
            title="Confirmar actualizar escenario crítico"
            centered
        >
            <h4>¿Está seguro de actualizar este escenario crítico?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="updateCrisisScenario"
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
            title="Confirmar eliminar escenario crítico"
            centered
        >
            <h4>¿Está seguro de eliminar este escenario crítico?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteCrisisScenario"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de asociar riesgos con escenario crítico  
        -->
        <b-modal
            id="modal-associate-risks"
            title="Asociar riesgos al escenario crítico"
            ref="modal"
            size="lg"
            centered
        >
            <h3>a</h3>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="primary"
                        class="float-right"
                        @click="handleSubmitUpdate"
                    >
                        Asociar riesgos
                    </b-button>
                </div>
            </template>
        </b-modal>

        <div class="row"></div>
        <!-- /.row -->
    </div>
</template>
<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import { FilterMatchMode } from "primevue/api";

import NotificationTemplate from "../Notifications/NotificationTemplate";

export default {
    name: "CrisisScenarios",

    data: () => ({
        loading: false,
        filterGlobal: null,

        // Variables para maanejar los modales
        show_modal_create: false,

        crisisScenarios: [],
        crisisId: 0,

        crisisScenario: {
            name: "",
            description: "",
        },
        crisisState: {
            name: null,
            description: null,
        },
    }),
    mounted() {
        this.getCrisisScenarios();
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
        async getCrisisScenarios() {
            this.loading = true;
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
            let valid = true;
            if (!this.crisisScenario.name) {
                this.crisisState.name = false;
                valid = false;
            }
            if (!this.crisisScenario.description) {
                this.crisisState.description = false;
                valid = false;
            }
            return valid;
        },
        resetModal() {
            this.crisisScenario.name = "";
            this.crisisState.name = null;
            this.crisisScenario.description = "";
            this.crisisState.description = null;
        },
        /**
         * Create
         */
        handleSubmitCreate() {
            // Inicializamos variables de estados
            this.crisisState.name = null;
            this.crisisState.description = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create");
            });
        },
        async createCrisisScenario() {
            axios
                .post(
                    `${SERVER_ADDRESS}/api/phase1/crisis_scenarios/`,
                    this.crisisScenario,
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
                        "El escenario crítico ha sido creado exitosamente"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    // Cargamos de nuevo la tabla de escenarios críticos
                    this.getCrisisScenarios();
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
            this.crisisState.name = null;
            this.crisisState.description = null;

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
            this.crisisId = id;

            axios
                .get(`${SERVER_ADDRESS}/api/phase1/crisis_scenario/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.crisisScenario = res.data;
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
        async updateCrisisScenario() {
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase1/crisis_scenario/${this.crisisId}/`,
                    this.crisisScenario,
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
                        "El escenario crítico ha sido actualizado exitosamente"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });

                    // Cargamos de nuevo la tabla de escenario crítico
                    this.getCrisisScenarios();
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
            this.crisisId = id;
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
        async deleteCrisisScenario() {
            axios
                .delete(
                    `${SERVER_ADDRESS}/api/phase1/crisis_scenario/${this.crisisId}/`,
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
                        "El escenario crítico ha sido eliminado exitosamente"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-delete");
                    });

                    // Cargamos de nuevo la tabla de escenarios críticos
                    this.getCrisisScenarios();
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
         * Associate risks with the crisis scenario
         */
        show_modal_association(id) {
            this.crisisId = id;
            this.$nextTick(() => {
                this.$bvModal.show("modal-associate-risks");
            });
        },
    },
};
</script>
<style lang="scss">
.header-table {
    background-color: rgb(17, 17, 17);
    color: rgb(255, 255, 255);
}
</style>
