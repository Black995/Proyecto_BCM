<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">{{ routeName }}</a>
            <button
                class="navbar-toggler navbar-burger"
                type="button"
                @click="toggleSidebar"
                :aria-expanded="$sidebar.showSidebar"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-bar"></span>
                <span class="navbar-toggler-bar"></span>
                <span class="navbar-toggler-bar"></span>
            </button>
            <div class="collapse navbar-collapse">
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item" title-classes="nav-link">
                        <a
                            href="/#/layout/notificaciones"
                            class="nav-link notif"
                        >
                            <h1>{{ $numberNotifications }}</h1>
                            <span
                                v-if="$numberNotifications != 0"
                                class="badge"
                                >{{ $numberNotifications }}</span
                            >
                            <i class="ti-bell"></i> Notificaciones
                        </a>
                    </li>
                    <!--drop-down
                        class="nav-item"
                        title="5 Notifications"
                        title-classes="nav-link"
                        icon="ti-bell"
                    >
                        <a class="dropdown-item" href="#">Notification 1</a>
                        <a class="dropdown-item" href="#">Notification 2</a>
                        <a class="dropdown-item" href="#">Notification 3</a>
                        <a class="dropdown-item" href="#">Notification 4</a>
                        <a class="dropdown-item" href="#"
                            >Prueba de notificación lo suficientemente larga
                            como para hacer una prueba</a
                        >
                    </drop-down-->
                    <drop-down
                        class="nav-item"
                        title="Configuraciones"
                        title-classes="nav-link"
                        icon="ti-settings"
                    >
                        <a
                            class="dropdown-item"
                            href="#"
                            @click="show_modal_change_password = true"
                            >Cambiar contraseña</a
                        >
                        <a
                            class="dropdown-item"
                            href="#"
                            @click="show_modal_activation"
                            >Activar producto</a
                        >
                        <a class="dropdown-item" href="#" @click="logout"
                            >Cerrar sesión</a
                        >
                    </drop-down>
                </ul>
            </div>
        </div>

        <!--
            Modal cambiar contraseña  
        -->
        <b-modal
            v-model="show_modal_change_password"
            id="modal-change-password"
            title="Cambiar contraseña"
            ref="modal"
            centered
            @show="resetModalPassword"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitChangePassword">
                <b-form-group
                    label="Ingrese la contraseña actual"
                    invalid-feedback="Este campo es obligatorio"
                    :state="passwordsState.old_password"
                >
                    <b-form-input
                        type="password"
                        v-model="passwords.old_password"
                        :state="passwordsState.old_password"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    label="Ingrese la nueva contraseña"
                    invalid-feedback="Este campo es obligatorio"
                    :state="passwordsState.new_password"
                >
                    <b-form-input
                        type="password"
                        v-model="passwords.new_password"
                        :state="passwordsState.new_password"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    label="Repita la nueva contraseña"
                    invalid-feedback="Este campo es obligatorio"
                    :state="passwordsState.new_password2"
                >
                    <b-form-input
                        type="password"
                        v-model="new_password2"
                        :state="passwordsState.new_password2"
                        required
                    ></b-form-input>
                </b-form-group>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitChangePassword"
                    >
                        Cambiar contraseña
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar cambiar contraseña  
        -->
        <b-modal
            id="modal-confirm-change-password"
            title="Confirmar cambiar contraseña"
            centered
        >
            <h4>¿Está seguro de cambiar la contraseña?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="changePassword"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal activación de producto
        -->
        <b-modal
            id="modal-activate-product"
            title="Activar producto"
            ref="mmodal"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitActivate">
                <b-form-group
                    label="Ingrese la llave de activación"
                    invalid-feedback="Seleccione un archivo valido"
                    :state="fileState"
                >
                    <b-row align-v="center">
                        <b-form-file
                            v-model="file"
                            :state="fileState"
                            size="sm"
                            required
                        ></b-form-file>
                    </b-row>
                </b-form-group>
            </form>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitActivate"
                    >
                        Activar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal confirmar activar
        -->
        <b-modal
            id="modal-confirm-activate"
            title="Confirmar activación del producto"
            centered
        >
            <h4>¿Está seguro que desea activar el producto?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="activateProduct"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>
    </nav>
</template>

<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import NotificationTemplate from "../../pages/Notifications/NotificationTemplate";
// import { store } from "../../store/index";

export default {
    computed: {
        routeName() {
            const { name } = this.$route;
            return this.capitalizeFirstLetter(name);
        },
    },
    data() {
        return {
            activeNotifications: false,

            show_modal_change_password: false,
            passwords: {
                old_password: "",
                new_password: "",
            },
            new_password2: "",
            passwordsState: {
                old_password: null,
                new_password2: null,
                new_password: null,
            },

            is_superuser: null,

            file: null,
            fileState: null,
        };
    },
    mounted() {
        this.is_superuser = localStorage.getItem("is_superuser");

        this.getNumberOfUnreadNorifications();
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
        capitalizeFirstLetter(string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        },
        toggleNotificationDropDown() {
            this.activeNotifications = !this.activeNotifications;
        },
        closeDropDown() {
            this.activeNotifications = false;
        },
        toggleSidebar() {
            this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
        },
        hideSidebar() {
            this.$sidebar.displaySidebar(false);
        },

        checkFormValidity() {
            let valid = true;
            if (!this.passwords.old_password) {
                this.passwordsState.old_password = false;
                valid = false;
            }
            if (!this.passwords.new_password) {
                this.passwordsState.new_password = false;
                valid = false;
            }
            if (!this.new_password2) {
                this.passwordsState.new_password2 = false;
                valid = false;
            }
            if (
                this.passwords.new_password != this.new_password2 &&
                (this.passwords.new_password || this.new_password2)
            ) {
                this.errorMessage("Las contraseñas ingresadas no coinciden");
                valid = false;
            }
            return valid;
        },
        resetModalPassword() {
            this.passwords.old_password = "";
            this.passwordsState.old_password = null;
            this.passwords.new_password = "";
            this.passwordsState.new_password = null;
            this.new_password2 = "";
            this.passwordsState.new_password2 = null;
        },

        /**
         * Create
         */
        handleSubmitChangePassword() {
            // Inicializamos variables de estados
            this.passwordsState.old_password = null;
            this.passwordsState.new_password = null;
            this.passwordsState.new_password2 = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-change-password");
            });
        },
        async changePassword() {
            axios
                .post(
                    `${SERVER_ADDRESS}/api/users/change_password/`,
                    this.passwords,
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
                        "¡La contraseña fue cambiada exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-change-password");
                        this.$bvModal.hide("modal-change-password");
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

        logout() {
            localStorage.removeItem("token");
            localStorage.removeItem("isLoggedin");

            this.$router.push("/");
        },
        async getActivationState() {
            axios
                .get(`${SERVER_ADDRESS}/api/config/get_activation_state/`)
                .then((res) => {
                    if (res.data.length) {
                        this.activation = {
                            state: res.data[0].state,
                            activation_date: res.data[0].activation_date,
                        };
                    } else {
                        this.activation = {
                            state: false,
                            activation_date: null,
                        };
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
        show_modal_activation() {
            this.file = null;
            this.fileState = null;
            this.$nextTick(() => {
                this.$bvModal.show("modal-activate-product");
            });
        },
        handleSubmitActivate() {
            this.fileState = null;
            if (!this.file || !this.file.name.endsWith(".txt")) {
                this.fileState = false;
            } else {
                this.$nextTick(() => {
                    this.$bvModal.show("modal-confirm-activate");
                });
            }
        },
        async activateProduct() {
            let usedKey = {
                key: this.key,
            };
            let formData = new FormData();
            formData.append("licencia", this.file, this.file.name);
            axios
                .post(`${SERVER_ADDRESS}/api/config/activate/`, formData)
                .then((res) => {
                    this.$bvModal.hide("modal-activate-product");
                    this.$bvModal.hide("modal-confirm-activate");
                    this.getActivationState();
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
        async getNumberOfUnreadNorifications() {
            axios
                .get(
                    `${SERVER_ADDRESS}/api/notifications/unread_notifications/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    console.log("Cantidad de notificaciones");
                    console.log(res);
                    console.log(this.$numberNotifications);
                    if (res.data <= 9) {
                        this.$changeNumberNotif(res.data);
                        //this.$numberNotifications = res.data;
                    } else {
                        this.$changeNumberNotif("+9");
                        //this.$numberNotifications = "+9";
                    }
                    console.log(this.$numberNotifications);
                })
                .catch((err) => {
                    console.log("err");
                    console.log(err);
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
<style>
.notif .badge {
    position: relative;
    top: -15px;
    right: -27px;
    padding: 5px 7px;
    border-radius: 50%;
    background: red;
    color: white;
}
</style>
