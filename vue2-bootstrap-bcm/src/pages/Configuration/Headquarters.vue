<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="headquarters"
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
                                'city_name',
                                'parish_name',
                                'township_name',
                                'state_name',
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
                                                    'configuration.add_headquarter'
                                                )
                                            "
                                            title="Crear sede"
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
                            <Column field="state_name" header="Estado"></Column>
                            <Column field="city_name" header="Ciudad"></Column>
                            <Column
                                field="township_name"
                                header="Municipio"
                            ></Column>
                            <Column
                                field="parish_name"
                                header="Parroquia"
                            ></Column>
                            <Column field="id_2" header="Opciones">
                                <template #body="slotProps">
                                    <b-button
                                        v-if="
                                            is_superuser == true ||
                                            permissions.includes(
                                                'configuration.change_headquarter'
                                            )
                                        "
                                        title="Editar sede"
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
                                                'configuration.delete_headquarter'
                                            )
                                        "
                                        title="Eliminar sede"
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
                                No hay sedes encontradas.
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
            title="Crear sede de la organización"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-form-group
                    label="Ingrese el título de la sede"
                    label-for="name-input-create"
                    invalid-feedback="Este campo es obligatorio"
                    :state="headquarterState.name"
                >
                    <b-form-input
                        id="name-input"
                        v-model="headquarter.name"
                        :state="headquarterState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    label="Seleccione el Estado"
                    invalid-feedback="Este campo es obligatorio"
                    :state="headquarterState.state"
                >
                    <b-form-select
                        @change="
                            getCities(true);
                            getTownships(true);
                        "
                        v-model="stateId"
                        :options="states"
                        value-field="id"
                        text-field="name"
                        :state="headquarterState.state"
                        required
                    ></b-form-select>
                </b-form-group>
                <b-row align-v="center">
                    <b-col>
                        <b-form-group
                            v-if="stateId"
                            label="Seleccione la ciudad"
                            invalid-feedback="Este campo es obligatorio"
                            :state="headquarterState.city"
                        >
                            <b-form-select
                                v-model="headquarter.city"
                                :options="cities"
                                value-field="id"
                                text-field="name"
                                :state="headquarterState.city"
                                required
                            ></b-form-select>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            v-if="stateId"
                            label="Seleccione el municipio"
                            invalid-feedback="Este campo es obligatorio"
                            :state="headquarterState.township"
                        >
                            <b-form-select
                                @change="getParishes(true)"
                                v-model="townshipId"
                                :options="townships"
                                value-field="id"
                                text-field="name"
                                :state="headquarterState.township"
                                required
                            ></b-form-select>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-form-group
                    v-if="townshipId"
                    label="Seleccione la parroquia"
                    invalid-feedback="Este campo es obligatorio"
                    :state="headquarterState.parish"
                >
                    <b-form-select
                        v-model="headquarter.parish"
                        :options="parishes"
                        value-field="id"
                        text-field="name"
                        :state="headquarterState.parish"
                        required
                    ></b-form-select>
                </b-form-group>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitCreate"
                    >
                        Crear sede
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear  
        -->
        <b-modal
            id="modal-confirm-create"
            title="Confirmar crear sede"
            centered
        >
            <h4>¿Está seguro de crear esta sede de la organización?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createHeadquarter"
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
            title="Editar sede de la organización"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-form-group
                    label="Ingrese el título de la sede"
                    label-for="name-input-update"
                    invalid-feedback="Este campo es obligatorio"
                    :state="headquarterState.name"
                >
                    <b-form-input
                        id="name-input"
                        v-model="headquarter.name"
                        :state="headquarterState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    label="Seleccione el Estado"
                    invalid-feedback="Este campo es obligatorio"
                    :state="headquarterState.state"
                >
                    <b-form-select
                        @change="
                            getCities(true);
                            getTownships(true);
                        "
                        v-model="stateId"
                        :options="states"
                        value-field="id"
                        text-field="name"
                        :state="headquarterState.state"
                        required
                    ></b-form-select>
                </b-form-group>
                <b-row align-v="center">
                    <b-col>
                        <b-form-group
                            v-if="stateId"
                            label="Seleccione la ciudad"
                            invalid-feedback="Este campo es obligatorio"
                            :state="headquarterState.city"
                        >
                            <b-form-select
                                v-model="headquarter.city"
                                :options="cities"
                                value-field="id"
                                text-field="name"
                                :state="headquarterState.city"
                                required
                            ></b-form-select>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            v-if="stateId"
                            label="Seleccione el municipio"
                            invalid-feedback="Este campo es obligatorio"
                            :state="headquarterState.township"
                        >
                            <b-form-select
                                @change="getParishes(true)"
                                v-model="townshipId"
                                :options="townships"
                                value-field="id"
                                text-field="name"
                                :state="headquarterState.township"
                                required
                            ></b-form-select>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-form-group
                    v-if="townshipId"
                    label="Seleccione la parroquia"
                    invalid-feedback="Este campo es obligatorio"
                    :state="headquarterState.parish"
                >
                    <b-form-select
                        v-model="headquarter.parish"
                        :options="parishes"
                        value-field="id"
                        text-field="name"
                        :state="headquarterState.parish"
                        required
                    ></b-form-select>
                </b-form-group>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitUpdate"
                    >
                        Editar sede
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar editar  
        -->
        <b-modal
            id="modal-confirm-update"
            title="Confirmar editar sede"
            centered
        >
            <h4>¿Está seguro de editar esta sede de la organización?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="updateHeadquarter"
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
            title="Confirmar eliminar sede"
            centered
        >
            <h4>¿Está seguro de eliminar esta sede de la organización?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteHeadquarter"
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
    name: "Headquarters",

    data: () => ({
        loading: false,
        filterGlobal: {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        },
        permissions: [],
        is_superuser: false,

        // Variables para manejar los modales
        show_modal_create: false,

        headquarters: [],
        headquarterId: 0,

        headquarter: {
            name: "",
            city: 0,
            parish: 0,
        },
        headquarterState: {
            name: null,
            state: null,
            city: null,
            township: null,
            parish: null,
        },

        /**
         * Variables utilizadas para manejo de estados, ciudades, municipios y parroquias
         */
        states: [],
        cities: [],
        townships: [],
        parishes: [],
        stateId: 0,
        townshipId: 0,
    }),
    mounted() {
        this.getHeadquarters();
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
                icon: "ti-close",
                horizontalAlign: "right",
                verticalAlign: "top",
                type: "danger",
            });
        },
        async getHeadquarters() {
            this.loading = true;
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
                    this.loading = false;

                    // Mientras tanto vamos cargando la lista de estados
                    this.getStates();
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
            if (!this.headquarter.name) {
                this.headquarterState.name = false;
                valid = false;
            }
            if (this.stateId == 0) {
                this.headquarterState.state = false;
                valid = false;
            }
            if (this.townshipId == 0) {
                this.headquarterState.township = false;
                valid = false;
            }
            if (this.headquarter.city == 0) {
                this.headquarterState.city = false;
                valid = false;
            }
            if (this.headquarter.parish == 0) {
                this.headquarterState.parish = false;
                valid = false;
            }
            return valid;
        },
        resetModal() {
            this.headquarter.name = "";
            this.headquarterState.name = null;
            this.stateId = 0;
            this.headquarterState.state = null;
            this.townshipId = 0;
            this.headquarterState.township = null;
            this.headquarter.city = 0;
            this.headquarterState.city = null;
            this.headquarter.parish = 0;
            this.headquarterState.parish = null;
        },
        /**
         * Create
         */
        handleSubmitCreate() {
            // Inicializamos variables de estados
            this.headquarterState.name = null;
            this.headquarterState.state = null;
            this.headquarterState.township = null;
            this.headquarterState.city = null;
            this.headquarterState.parish = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create");
            });
        },
        async createHeadquarter() {
            axios
                .post(
                    `${SERVER_ADDRESS}/api/config/headquarters/`,
                    this.headquarter,
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
                        "¡La sede ha sido creada exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getHeadquarters();
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
            this.headquarterState.name = null;
            this.headquarterState.state = null;
            this.headquarterState.township = null;
            this.headquarterState.city = null;
            this.headquarterState.parish = null;

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
            this.headquarterId = id;

            axios
                .get(`${SERVER_ADDRESS}/api/config/headquarter/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.headquarter.name = res.data.name;
                    this.headquarter.city = res.data.city;
                    this.headquarter.parish = res.data.parish;
                    this.stateId = res.data.state;
                    this.townshipId = res.data.township;
                    this.getCities(false);
                    this.getTownships(false);
                    this.getParishes(false);

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
        async updateHeadquarter() {
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/config/headquarter/${this.headquarterId}/`,
                    this.headquarter,
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
                        "¡La sede ha sido actualizada exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getHeadquarters();
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
            this.headquarterId = id;
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
        async deleteHeadquarter() {
            axios
                .delete(
                    `${SERVER_ADDRESS}/api/config/headquarter/${this.headquarterId}/`,
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
                        "¡La sede ha sido eliminada exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-delete");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getHeadquarters();
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
         * Obtener estados, ciudades, municipios y parroquias
         */
        async getStates() {
            this.states = [];

            axios
                .get(`${SERVER_ADDRESS}/api/config/states/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.states = res.data;
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
        async getCities(reset) {
            this.cities = [];
            if (reset) {
                this.headquarter.city = 0;
            }

            axios
                .get(`${SERVER_ADDRESS}/api/config/cities/`, {
                    params: { state_id: this.stateId },
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.cities = res.data;
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
        async getTownships(reset) {
            this.townships = [];
            if (reset) {
                this.townshipId = 0;
            }

            axios
                .get(`${SERVER_ADDRESS}/api/config/townships/`, {
                    params: { state_id: this.stateId },
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.townships = res.data;
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
        async getParishes(reset) {
            this.parishes = [];
            if (reset) {
                this.headquarter.parish = 0;
            }

            axios
                .get(`${SERVER_ADDRESS}/api/config/parishes/`, {
                    params: { township_id: this.townshipId },
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.parishes = res.data;
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
