<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="roles"
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
                                                    'auth.add_group'
                                                )
                                            "
                                            title="Crear rol"
                                            variant="success"
                                            @click="show_modal_create()"
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
                                        title="Detalle del rol"
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
                                        v-if="
                                            is_superuser == true ||
                                            permissions.includes(
                                                'auth.change_group'
                                            )
                                        "
                                        title="Editar rol"
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
                                                'auth.delete_group'
                                            )
                                        "
                                        title="Eliminar rol"
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
                                No hay roles encontrados.
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
            title="Detalle del rol"
            ref="modal"
            size="lg"
            centered
        >
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <strong>Nombre: </strong>{{ roleDetail.name }}
                </li>
            </ul>

            <h4 class="mt-1 text-center font-weight-bold">Permisos del rol</h4>
            <b-list-group-item
                class="mt-1 flex-column align-items-start"
                v-for="item in roleDetail.permissions"
                :key="item.key"
            >
                <h5 class="mb-1">{{ item.name }}</h5>
                <p class="mb-2">Nombre clave: {{ item.codename }}</p>
            </b-list-group-item>
            <h3 class="mt-3 text-center" v-if="!roleDetail.permissions.length">
                No existen permisos asociados a este rol
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
            id="modal-create"
            title="Crear rol"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-form-group
                    label="Ingrese el nombre del rol"
                    invalid-feedback="Este campo es obligatorio"
                    :state="roleState.email"
                >
                    <b-form-input
                        v-model="role.name"
                        :state="roleState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-row class="text-center">
                    <b-col>
                        <b-button
                            variant="primary"
                            align-v="center"
                            @click="addAllRoles"
                        >
                            Agregar todos los roles
                        </b-button>
                    </b-col>
                </b-row>
                <multiselect
                    class="mt-2"
                    v-model="selectedPermissions"
                    placeholder="Buscar permiso"
                    label="name"
                    track-by="id"
                    :options="permissionsList"
                    :multiple="true"
                ></multiselect>

                <div v-if="selectedPermissions.length" class="mt-5">
                    <h3 class="text-center">Permisos separados por tablas</h3>
                    <div v-for="title in modelsList" :key="title">
                        <b-card header-tag="header" footer-tag="footer">
                            <template #header>
                                <h5>{{ title }}</h5>
                            </template>
                            <div
                                v-for="item in selectedPermissions"
                                :key="item.key"
                            >
                                <b-list-group-item
                                    v-if="title == item.model_name"
                                    href="#"
                                    class="flex-column align-items-start"
                                >
                                    <h5 class="mb-1">{{ item.name }}</h5>
                                    <p class="mb-2">
                                        Nombre clave: {{ item.codename }}
                                    </p>
                                </b-list-group-item>
                            </div>
                        </b-card>
                    </div>
                </div>

                <h3 class="mt-3 text-center" v-if="!selectedPermissions.length">
                    No existen permisos asociados a este rol
                </h3>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitCreate"
                    >
                        Crear rol
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear  
        -->
        <b-modal id="modal-confirm-create" title="Confirmar crear rol" centered>
            <h4>¿Está seguro de crear este rol?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createRole"
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
            title="Editar rol"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-form-group
                    label="Ingrese el nombre del rol"
                    invalid-feedback="Este campo es obligatorio"
                    :state="roleState.name"
                >
                    <b-form-input
                        v-model="role.name"
                        :state="roleState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-row class="text-center">
                    <b-col>
                        <b-button
                            variant="primary"
                            align-v="center"
                            @click="addAllRoles"
                        >
                            Agregar todos los roles
                        </b-button>
                    </b-col>
                </b-row>
                <multiselect
                    v-model="selectedPermissions"
                    placeholder="Buscar permiso"
                    label="name"
                    track-by="id"
                    :options="permissionsList"
                    :multiple="true"
                ></multiselect>

                <div v-if="selectedPermissions.length" class="mt-5">
                    <h3 class="text-center">Permisos separados por tablas</h3>
                    <div v-for="title in modelsList" :key="title">
                        <b-card header-tag="header" footer-tag="footer">
                            <template #header>
                                <h5>{{ title }}</h5>
                            </template>
                            <div
                                v-for="item in selectedPermissions"
                                :key="item.key"
                            >
                                <b-list-group-item
                                    v-if="title == item.model_name"
                                    href="#"
                                    class="flex-column align-items-start"
                                >
                                    <h5 class="mb-1">{{ item.name }}</h5>
                                    <p class="mb-2">
                                        Nombre clave: {{ item.codename }}
                                    </p>
                                </b-list-group-item>
                            </div>
                        </b-card>
                    </div>
                </div>

                <h3 class="mt-3 text-center" v-if="!selectedPermissions.length">
                    No existen permisos asociados a este rol
                </h3>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitUpdate"
                    >
                        Editar rol
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar editar  
        -->
        <b-modal
            id="modal-confirm-update"
            title="Confirmar editar rol"
            centered
        >
            <h4>¿Está seguro de editar este rol?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="updateRole"
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
            title="Confirmar eliminar rol"
            centered
        >
            <h4>¿Está seguro de eliminar este rol?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteRole"
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
    name: "Roles",
    components: {
        Multiselect,
    },
    data: () => ({
        loading: false,
        filterGlobal: {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        },
        permissionsList: [],
        modelsList: [],
        is_superuser: false,

        roles: [],
        roleDetail: {
            name: "",
            permissions: [],
        },
        roleId: 0,

        role: {
            name: "",
            _permissions: [],
        },
        roleState: {
            name: null,
        },

        permissions: [],
        selectedPermissions: [],
    }),
    mounted() {
        this.getRoles();
        this.getPermissions();
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
        async getRoles() {
            this.loading = true;
            this.roles = [];

            axios
                .get(`${SERVER_ADDRESS}/api/users/groups/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.roles = res.data;
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
        async getPermissions() {
            this.permissionsList = [];
            this.modelsList = [];

            axios
                .get(`${SERVER_ADDRESS}/api/users/permissions/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.permissionsList = res.data;

                    // Guardar solamente los nombres de los modelos
                    this.permissionsList.forEach((x) => {
                        if (!this.modelsList.includes(x.model_name)) {
                            this.modelsList.push(x.model_name);
                        }
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
            if (!this.role.name) {
                this.roleState.name = false;
                valid = false;
            }
            /**
             * Validar que se haya elegido al menos 1 permiso
             */
            if (!this.selectedPermissions.length) {
                this.errorMessage(
                    "Debe asociar al menos un permiso a este rol"
                );
                valid = false;
            }

            return valid;
        },
        resetModal() {
            this.role.name = "";
            this.roleState.name = null;
            this.role._permissions = [];
            this.selectedPermissions = [];
        },
        async show_modal_detail(id) {
            this.roleDetail = {
                name: "",
                permissions: [],
            };

            axios
                .get(`${SERVER_ADDRESS}/api/users/group/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.roleDetail = res.data;

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
        async show_modal_create() {
            this.$nextTick(() => {
                this.$bvModal.show("modal-create");
            });
        },
        handleSubmitCreate() {
            // Inicializamos variables de estados
            this.roleState.name = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }
            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create");
            });
        },
        async createRole() {
            this.role._permissions = [];

            for (let i = 0; i < this.selectedPermissions.length; i++) {
                this.role._permissions.push(
                    this.selectedPermissions[i].codename
                );
            }

            axios
                .post(`${SERVER_ADDRESS}/api/users/groups/`, this.role, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage("¡El rol ha sido creado exitosamente!");

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    this.getRoles();
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
            this.roleState.name = null;

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
            this.roleId = id;

            axios
                .get(`${SERVER_ADDRESS}/api/users/group/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.role = res.data;

                    this.selectedPermissions = [];
                    for (let i = 0; i < res.data.permissions.length; i++) {
                        this.selectedPermissions.push(res.data.permissions[i]);
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
        async updateRole() {
            this.role._permissions = [];

            for (let i = 0; i < this.selectedPermissions.length; i++) {
                this.role._permissions.push(
                    this.selectedPermissions[i].codename
                );
            }

            axios
                .patch(
                    `${SERVER_ADDRESS}/api/users/group/${this.roleId}/`,
                    this.role,
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
                        "¡El rol ha sido actualizado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });

                    this.getRoles();
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
            this.roleId = id;
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
        async deleteRole() {
            axios
                .delete(`${SERVER_ADDRESS}/api/users/group/${this.roleId}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡El rol ha sido eliminado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-delete");
                    });

                    this.getRoles();
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
        addAllRoles() {
            this.selectedPermissions = [];

            for (let i = 0; i < this.permissionsList.length; i++) {
                this.selectedPermissions.push(this.permissionsList[i]);
            }
        },
    },
};
</script>
<style lang="scss">
</style>
