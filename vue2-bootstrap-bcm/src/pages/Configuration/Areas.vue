<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="areas"
                            responsiveLayout="scroll"
                            :paginator="true"
                            :rows="10"
                            :rowsPerPageOptions="[10, 20]"
                            :resizableColumns="true"
                            :autoLayout="true"
                            :responsive="true"
                            :reorderableColumns="true"
                            :loading="loading"
                            :globalFilterFields="['name']"
                            :filters="filterGlobal"
                        >
                            <template #header>
                                <b-row class="justify-content-between">
                                    <b-col sm="4">
                                        <b-button
                                            v-if="
                                                is_superuser == true ||
                                                permissions.includes(
                                                    'configuration.add_area'
                                                )
                                            "
                                            title="Crear área"
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
                            <Column field="id" header="Opciones">
                                <template #body="slotProps">
                                    <b-button
                                        v-if="
                                            is_superuser == true ||
                                            permissions.includes(
                                                'configuration.change_area'
                                            )
                                        "
                                        title="Editar área"
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
                                                'configuration.delete_area'
                                            )
                                        "
                                        title="Eliminar área"
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
                                No hay áreas encontradas.
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
            title="Crear área de la organización"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-form-group
                    label="Ingrese el título del área"
                    label-for="name-input-create"
                    invalid-feedback="Este campo es obligatorio"
                    :state="areaState.name"
                >
                    <b-form-input
                        id="name-input"
                        v-model="area.name"
                        :state="areaState.name"
                        required
                    ></b-form-input>
                </b-form-group>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitCreate"
                    >
                        Crear área
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear  
        -->
        <b-modal
            id="modal-confirm-create"
            title="Confirmar crear área"
            centered
        >
            <h4>¿Está seguro de crear esta área de la organización?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createArea"
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
            title="Editar área de la organización"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-form-group
                    label="Ingrese el título del área"
                    label-for="name-input-update"
                    invalid-feedback="Este campo es obligatorio"
                    :state="areaState.name"
                >
                    <b-form-input
                        id="name-input"
                        v-model="area.name"
                        :state="areaState.name"
                        required
                    ></b-form-input>
                </b-form-group>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitUpdate"
                    >
                        Editar área
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar editar  
        -->
        <b-modal
            id="modal-confirm-update"
            title="Confirmar editar área"
            centered
        >
            <h4>¿Está seguro de editar esta área de la organización?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="updateArea"
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
            title="Confirmar eliminar área"
            centered
        >
            <h4>¿Está seguro de eliminar esta área de la organización?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteArea"
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
import NotificationTemplate from "../Notifications/NotificationTemplate";

export default {
    name: "Areas",

    data: () => ({
        loading: false,
        filterGlobal: {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        },
        permissions: [],
        is_superuser: false,

        // Variables para manejar los modales
        show_modal_create: false,

        areas: [],
        areaId: 0,

        area: {
            name: "",
        },
        areaState: {
            name: null,
        },
    }),
    mounted() {
        this.getAreas();
        this.permissions = localStorage.getItem("permissions");
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
        async getAreas() {
            this.loading = true;
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
                value: null,
                matchMode: FilterMatchMode.CONTAINS,
            };
        },

        /**
         * Validar formularios
         */
        checkFormValidity() {
            let valid = true;
            if (!this.area.name) {
                this.areaState.name = false;
                valid = false;
            }
            return valid;
        },
        resetModal() {
            this.area.name = "";
            this.areaState.name = null;
        },
        /**
         * Create
         */
        handleSubmitCreate() {
            // Inicializamos variables de estados
            this.areaState.name = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create");
            });
        },
        async createArea() {
            axios
                .post(`${SERVER_ADDRESS}/api/config/areas/`, this.area, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡El área ha sido creada exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getAreas();
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
            this.areaState.name = null;

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
            this.areaId = id;

            axios
                .get(`${SERVER_ADDRESS}/api/config/area/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.area = res.data;
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
        async updateArea() {
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/config/area/${this.areaId}/`,
                    this.area,
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
                        "¡El área ha sido actualizada exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getAreas();
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
            this.areaId = id;
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
        async deleteArea() {
            axios
                .delete(`${SERVER_ADDRESS}/api/config/area/${this.areaId}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡El área ha sido eliminada exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-delete");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getAreas();
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
