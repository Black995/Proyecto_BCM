<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="users"
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
                                'email',
                                'staff_number',
                                'names',
                                'surnames',
                                'is_active',
                            ]"
                            :filters="filterGlobal"
                        >
                            <template #header>
                                <b-row class="justify-content-between">
                                    <b-col sm="4">
                                        <b-button
                                            title="Crear usuario"
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
                            <Column field="email" header="Correo"></Column>
                            <Column
                                field="staff_number"
                                header="Número de Identificación"
                            ></Column>
                            <Column field="names" header="Nombre completo">
                                <template #body="slotProps">
                                    {{ slotProps.data.names }}
                                    {{ slotProps.data.surnames }}
                                </template>
                            </Column>
                            <Column field="is_active" header="Usuario activo">
                                <template #body="slotProps">
                                    <div v-if="slotProps.data.is_active">
                                        Sí
                                    </div>
                                    <div v-if="!slotProps.data.is_active">
                                        No
                                    </div>
                                </template>
                            </Column>
                            <Column field="id" header="Opciones">
                                <template #body="slotProps">
                                    <b-button
                                        title="Detalle del usuario"
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
                                        title="Editar usuario"
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
                                        title="Eliminar usuario"
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
                                No hay usuarios encontrados.
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
            title="Detalle del usuario"
            ref="modal"
            size="lg"
            centered
        >
            <h3 v-if="userDetail.names" class="text-center font-weight-bold">
                {{ userDetail.names }} {{ userDetail.surnames }}
            </h3>
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <strong>Correo: </strong>{{ userDetail.email }}
                </li>
                <li v-if="userDetail.staff_number" class="list-group-item">
                    <strong>Número de identificación: </strong
                    >{{ userDetail.staff_number }}
                </li>
                <li class="list-group-item">
                    <div v-if="userDetail.is_active">
                        <strong>Usuario activo</strong>
                    </div>
                    <div v-if="!userDetail.is_active">
                        <strong>Usuario inactivo</strong>
                    </div>
                </li>
                <li v-if="userDetail.is_superuser" class="list-group-item">
                    <strong>Este usuario tiene el rol de súper usuario</strong>
                </li>
                <li v-if="userDetail.area_name" class="list-group-item">
                    <strong>Area de la organización: </strong
                    >{{ userDetail.area_name }}
                </li>
                <li v-if="userDetail.position_name" class="list-group-item">
                    <strong>Cargo: </strong>{{ userDetail.position_name }}
                </li>
                <li v-if="userDetail.headquarter_name" class="list-group-item">
                    <strong>Sede: </strong>{{ userDetail.headquarter_name }}
                </li>
            </ul>

            <!--h4 class="mt-5 text-center font-weight-bold">
                Permisos del usuario
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
                No existen riesgos asociados a este servicio de soporte
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
            id="modal-create"
            title="Crear usuario"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-form-group
                    label="Ingrese el correo del usuario"
                    invalid-feedback="Este campo es obligatorio"
                    :state="userState.email"
                >
                    <b-form-input
                        type="email"
                        v-model="user.email"
                        :state="userState.email"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-row align-v="center">
                    <b-col>
                        <b-form-group
                            label="Ingrese la contraseña del usuario"
                            invalid-feedback="Este campo es obligatorio"
                            :state="userState.password"
                        >
                            <b-form-input
                                type="password"
                                v-model="user.password"
                                :state="userState.password"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Repita la contraseña"
                            invalid-feedback="Este campo es obligatorio"
                            :state="userState.password2"
                        >
                            <b-form-input
                                type="password"
                                v-model="password2"
                                :state="userState.password2"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-form-group
                    label="Seleccione el personal asociado a este usuario"
                    invalid-feedback="Este campo es obligatorio"
                    :state="userState.staff"
                >
                    <b-form-select
                        v-model="user.staff"
                        :options="staffsWithoutUser"
                        value-field="value"
                        text-field="text"
                        :state="userState.staff"
                        required
                    ></b-form-select>
                </b-form-group>
                <b-form-group>
                    <b-form-checkbox v-model="user.is_superuser">
                        Súper usuario
                    </b-form-checkbox>
                </b-form-group>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitCreate"
                    >
                        Crear usuario
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear  
        -->
        <b-modal
            id="modal-confirm-create"
            title="Confirmar crear usuario"
            centered
        >
            <h4>¿Está seguro de crear este usuario?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createUser"
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
            title="Editar usuario"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-form-group
                    label="Ingrese el correo del usuario"
                    invalid-feedback="Este campo es obligatorio"
                    :state="userState.email"
                >
                    <b-form-input
                        type="email"
                        v-model="user.email"
                        :state="userState.email"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-row align-v="center">
                    <b-col>
                        <b-form-group
                            label="Ingrese la contraseña del usuario"
                            invalid-feedback="Este campo es obligatorio"
                            :state="userState.password"
                        >
                            <b-form-input
                                type="password"
                                v-model="user.password"
                                :state="userState.password"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Repita la contraseña"
                            invalid-feedback="Este campo es obligatorio"
                            :state="userState.password2"
                        >
                            <b-form-input
                                type="password"
                                v-model="password2"
                                :state="userState.password2"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-form-group
                    label="Seleccione el personal asociado a este usuario"
                    invalid-feedback="Este campo es obligatorio"
                    :state="userState.staff"
                >
                    <b-form-select
                        v-model="user.staff"
                        :options="staffsWithoutUser"
                        value-field="value"
                        text-field="text"
                        :state="userState.staff"
                        required
                    ></b-form-select>
                </b-form-group>
                <b-form-group>
                    <b-form-checkbox v-model="user.is_active">
                        Usuario activo
                    </b-form-checkbox>
                </b-form-group>
                <b-form-group>
                    <b-form-checkbox v-model="user.is_superuser">
                        Súper usuario
                    </b-form-checkbox>
                </b-form-group>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitUpdate"
                    >
                        Editar usuario
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar editar  
        -->
        <b-modal
            id="modal-confirm-update"
            title="Confirmar editar usuario"
            centered
        >
            <h4>¿Está seguro de editar este usuario?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="updateUser"
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
            title="Confirmar eliminar usuario"
            centered
        >
            <h4>¿Está seguro de eliminar este usuario?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteUser"
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
    name: "Users",

    data: () => ({
        loading: false,
        filterGlobal: {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        },

        users: [],
        userDetail: {
            email: "",
            is_active: false,
            is_admin: false,
            is_superuser: false,
            staff_number: "",
            names: "",
            surnames: "",
            area_name: "",
            position_name: "",
            headquarter_name: "",
            permissions: [],
        },
        userId: 0,

        user: {
            email: "",
            password: "",
            is_superuser: false,
            is_active: true,
            staff: 0,
        },
        password2: "",
        userState: {
            email: null,
            password: null,
            password2: null,
            staff: null,
        },

        staffsWithoutUser: [],
    }),
    mounted() {
        this.getUsers();
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
        async getUsers() {
            this.loading = true;
            this.users = [];

            axios
                .get(`${SERVER_ADDRESS}/api/users/users/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.users = res.data;
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
        async getStaffsWithoutUser() {
            this.staffsWithoutUser = [];

            axios
                .get(`${SERVER_ADDRESS}/api/users/staffs-without-user/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for (let i = 0; i < res.data.length; i++) {
                        let obj = {
                            value: res.data[i].id,
                            text:
                                res.data[i].names +
                                " " +
                                res.data[i].surnames +
                                " (área: " +
                                res.data[i].area_name +
                                ", cargo: " +
                                res.data[i].position_name +
                                ")",
                        };
                        this.staffsWithoutUser.push(obj);
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
            if (!this.user.email) {
                this.userState.email = false;
                valid = false;
            }
            if (!this.user.password) {
                this.userState.password = false;
                valid = false;
            }
            if (!this.password2) {
                this.userState.password2 = false;
                valid = false;
            }
            if (this.user.password != this.password2) {
                this.errorMessage("Las contraseñas ingresadas no coinciden");
                valid = false;
            }
            if (this.user.staff == 0) {
                this.userState.staff = false;
                valid = false;
            }
            return valid;
        },
        resetModal() {
            this.user.email = "";
            this.userState.email = null;
            this.user.password = "";
            this.userState.password = null;
            this.password2 = "";
            this.userState.password2 = null;
            this.user.staff = 0;
            this.userState.staff = null;
            this.user.is_superuser = false;
            this.user.is_active = true;
        },

        async show_modal_detail(id) {
            this.userDetail = {
                email: "",
                is_active: false,
                is_admin: false,
                is_superuser: false,
                staff_number: "",
                names: "",
                surnames: "",
                area_name: "",
                position_name: "",
                headquarter_name: "",
                permissions: [],
            };

            axios
                .get(`${SERVER_ADDRESS}/api/users/user/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.userDetail = res.data;
                    console.log(this.userDetail);

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
            this.getStaffsWithoutUser();
            this.$nextTick(() => {
                this.$bvModal.show("modal-create");
            });
        },
        handleSubmitCreate() {
            // Inicializamos variables de estados
            this.userState.email = null;
            this.userState.password = null;
            this.userState.staff = null;
            this.userState.password2 = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create");
            });
        },
        async createUser() {
            axios
                .post(`${SERVER_ADDRESS}/api/users/users/`, this.user, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡El usuario ha sido creado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    this.getUsers();
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
            this.userState.email = null;
            this.userState.password = null;
            this.userState.staff = null;
            this.userState.password2 = null;

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
            this.userId = id;

            axios
                .get(`${SERVER_ADDRESS}/api/users/user/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.user = res.data;
                    this.password2 = res.data.password;
                    this.getStaffsWithoutUser();
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
        async updateUser() {
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/users/user/${this.userId}/`,
                    this.user,
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
                        "¡El usuario ha sido actualizado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });

                    this.getUsers();
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
            this.userId = id;
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
        async deleteUser() {
            axios
                .delete(`${SERVER_ADDRESS}/api/users/user/${this.userId}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡El usuario ha sido eliminado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-delete");
                    });

                    this.getUsers();
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
