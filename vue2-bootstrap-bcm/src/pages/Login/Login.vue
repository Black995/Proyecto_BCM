<template>
    <div class="wrapper fadeInDown">
        <div id="formContent">
            <!-- Icon -->
            <div class="fadeIn first mt-3">
                <img
                    src="../../assets/img/login_icon.png"
                    id="icon"
                    alt="User Icon"
                    class="rounded mx-auto d-block icon-login"
                />
            </div>

            <!-- Login Form -->
            <form ref="form" @submit.stop.prevent="handleSubmit">
                <b-form-input
                    type="text"
                    class="fadeIn second"
                    placeholder="correo"
                    v-model="user.email"
                    required
                ></b-form-input>
                <b-form-input
                    type="password"
                    class="fadeIn third"
                    placeholder="contraseña"
                    v-model="user.password"
                    required
                ></b-form-input>
                <button
                    v-if="activation.state"
                    type="submit"
                    class="fadeIn fourth"
                    :disabled="loadingButton && activation.state"
                >
                    <div v-if="!loadingButton">Iniciar sesión</div>
                    <b-spinner v-if="loadingButton" small></b-spinner>
                </button>
                <h6 v-if="!activation.state" style="color: red">
                    Sistema descativado. Ingrese una llave para activarlo.
                </h6>
            </form>

            <!-- Remind Passowrd -->
            <div id="formFooter">
                <a
                    v-if="activation.state"
                    class="underlineHover"
                    href="#"
                    @click="show_modal_forget_password"
                    >¿Olvidó su contraseña?</a
                >
                <div class="row"></div>
                <a
                    class="underlineHover"
                    href="#"
                    @click="show_modal_activation"
                    >Activar producto</a
                >
            </div>
        </div>
        <div class="row"></div>

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
                    :state="keyState"
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

        <!--
            Modal olvidar contraseña
        -->
        <b-modal
            id="modal-forget-password"
            title="Olvido de contraseña"
            ref="mmodal"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitForgetPassword">
                <b-form-group
                    label="Ingrese el correo al que se le enviarán las instrucciones para recuperar la cuenta"
                    invalid-feedback="Este campo no puede estar vacio"
                    :state="emailForgetState"
                >
                    <div class="text-center">
                        <b-form-input
                            v-model="emailForget"
                            :state="emailForgetState"
                            required
                        ></b-form-input>
                    </div>
                </b-form-group>
            </form>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitForgetPassword"
                        :disabled="loadingPasswordButton"
                    >
                        <div v-if="!loadingPasswordButton">Enviar correo</div>
                        <b-spinner
                            v-if="loadingPasswordButton"
                            small
                        ></b-spinner>
                    </b-button>
                </div>
            </template>
        </b-modal>
    </div>
</template>

<script>
import axios from "axios";
import { SERVER_ADDRESS } from "../../../config/config";

import NotificationTemplate from "../Notifications/NotificationTemplate";

export default {
    name: "Login",

    data: () => ({
        user: {
            email: "",
            password: "",
        },
        loadingButton: false,
        loadingPasswordButton: false,
        activation: {
            id: 0,
            state: null,
            activation_date: null,
        },
        key: "",
        keyState: null,

        file: null,
        fileState: null,

        emailForget: "",
        emailForgetState: null,
    }),
    /**
     * Se deja el mounted termporalmente
     */
    mounted() {
        this.getActivationState();
        /*
        this.user = {
            email: "alansaul25@gmail.com",
            password: "12345",
        };
        this.login();
      */
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
        async handleSubmit() {
            this.loadingButton = true;
            axios
                .post(`${SERVER_ADDRESS}/api/token/`, this.user)
                .then((res) => {
                    if (res.status === 200) {
                        /**
                         * Se guarda el token en local storage (provisionalmente)
                         */
                        localStorage.clear();

                        localStorage.setItem("token", res.data.access);
                        localStorage.setItem("isLoggedin", true);

                        /**
                         * Se obtienen los permisos
                         */
                        let token = "Bearer " + res.data.access;
                        axios
                            .get(`${SERVER_ADDRESS}/api/users/profile/`, {
                                withCredentials: true,
                                headers: {
                                    Authorization: token,
                                },
                            })
                            .then((res) => {
                                localStorage.setItem(
                                    "is_superuser",
                                    res.data.is_superuser
                                );
                                localStorage.setItem(
                                    "permissions",
                                    JSON.stringify(res.data.permissions)
                                );

                                this.$router.push("/layout/perfil");
                                location.reload();
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
                    }
                })
                .catch((err) => {
                    try {
                        this.loadingButton = false;
                        if (
                            err.response.status == 400 ||
                            err.response.status == 401
                        ) {
                            this.errorMessage(
                                "Las credenciales ingresadas son inválidas"
                            );
                        } else {
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    } catch {
                        this.loadingButton = false;
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                });
            //}
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
            this.keyState = null;
            this.key = "";
            this.$nextTick(() => {
                this.$bvModal.show("modal-activate-product");
            });
        },
        handleSubmitActivate() {
            this.fileState = null;
            if ((!this.file) || (!this.file.name.endsWith('.txt'))) {
                this.fileState = false;
            } else {
                this.$nextTick(() => {
                    this.$bvModal.show("modal-confirm-activate");
                });
            }
        },
        async activateProduct(){
            let usedKey ={
                key: this.key
            }
            let formData = new FormData()
            formData.append("licencia", this.file,this.file.name)
            axios
                .post(`${SERVER_ADDRESS}/api/config/activate/`, formData)
                .then((res)=>{
                    this.$bvModal.hide("modal-activate-product")
                    this.$bvModal.hide("modal-confirm-activate")
                    this.getActivationState()
                    
                })
                .catch((err) => {
                    try {
                        console.log(err)
                        console.log(err.response.data)
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
        show_modal_forget_password() {
            this.emailForgetState = null;
            this.emailForget = "";
            this.$nextTick(() => {
                this.$bvModal.show("modal-forget-password");
            });
        },
        async handleSubmitForgetPassword() {
            this.emailForgetState = null;
            if (!this.emailForget) {
                this.emailForgetState = false;
            } else {
                this.loadingPasswordButton = true;

                let forgetPassword = {
                    email: this.emailForget,
                };
                axios
                    .post(
                        `${SERVER_ADDRESS}/api/users/recover-account/`,
                        forgetPassword
                    )
                    .then((res) => {
                        this.loadingPasswordButton = true;
                        console.log("FORGOT PASSWORD");
                        //Ocultamos los modales
                        this.$nextTick(() => {
                            this.$bvModal.hide("modal-forget-password");
                        });

                        // Mensaje de éxito
                        this.successMessage(
                            "¡El correo ha sido enviado exitosamente! Por favor verificar en la bandeja de correos o en spam el email enviado"
                        );
                    })
                    .catch((err) => {
                        console.log("ERR");
                        console.log(err);
                        try {
                            this.loadingPasswordButton = false;

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
                            this.loadingPasswordButton = false;

                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    });
            }
        },
    },
};
</script>

<style scoped>
.login {
    background: #f1f1f1;
}

.icon-login {
    height: 150px !important;
    width: 150px !important;
}

a {
    color: #92badd;
    display: inline-block;
    text-decoration: none;
    font-weight: 400;
}

h2 {
    text-align: center;
    font-size: 16px;
    font-weight: 600;
    text-transform: uppercase;
    display: inline-block;
    margin: 40px 8px 10px 8px;
    color: #cccccc;
}

/* STRUCTURE */

.wrapper {
    font-family: "Poppins", sans-serif;
    display: flex;
    align-items: center;
    flex-direction: column;
    justify-content: center;
    min-height: 100%;
    padding: 20px;
}

#formContent {
    -webkit-border-radius: 10px 10px 10px 10px;
    border-radius: 10px 10px 10px 10px;
    background: #fff;
    padding: 30px;
    width: 90%;
    max-width: 450px;
    position: relative;
    padding: 0px;
    -webkit-box-shadow: 0 30px 60px 0 rgba(0, 0, 0, 0.3);
    box-shadow: 0 30px 60px 0 rgba(0, 0, 0, 0.3);
    text-align: center;
}

#formFooter {
    background-color: #f6f6f6;
    border-top: 1px solid #dce8f1;
    padding: 25px;
    text-align: center;
    -webkit-border-radius: 0 0 10px 10px;
    border-radius: 0 0 10px 10px;
}

/* TABS */

h2.inactive {
    color: #cccccc;
}

h2.active {
    color: #0d0d0d;
    border-bottom: 2px solid #5fbae9;
}

/* FORM TYPOGRAPHY*/

input[type="button"],
button[type="submit"],
input[type="reset"] {
    background-color: #56baed;
    border: none;
    color: white;
    padding: 15px 80px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    text-transform: uppercase;
    font-size: 13px;
    -webkit-box-shadow: 0 10px 30px 0 rgba(95, 186, 233, 0.4);
    box-shadow: 0 10px 30px 0 rgba(95, 186, 233, 0.4);
    -webkit-border-radius: 5px 5px 5px 5px;
    border-radius: 5px 5px 5px 5px;
    margin: 5px 20px 40px 20px;
    -webkit-transition: all 0.3s ease-in-out;
    -moz-transition: all 0.3s ease-in-out;
    -ms-transition: all 0.3s ease-in-out;
    -o-transition: all 0.3s ease-in-out;
    transition: all 0.3s ease-in-out;
}

input[type="button"]:hover,
button[type="submit"]:hover,
input[type="reset"]:hover {
    background-color: #39ace7;
}

input[type="button"]:active,
button[type="submit"]:active,
input[type="reset"]:active {
    -moz-transform: scale(0.95);
    -webkit-transform: scale(0.95);
    -o-transform: scale(0.95);
    -ms-transform: scale(0.95);
    transform: scale(0.95);
}

input[type="text"],
input[type="password"] {
    background-color: #f6f6f6;
    border: none;
    color: #0d0d0d;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 5px;
    width: 85%;
    border: 2px solid #f6f6f6;
    -webkit-transition: all 0.5s ease-in-out;
    -moz-transition: all 0.5s ease-in-out;
    -ms-transition: all 0.5s ease-in-out;
    -o-transition: all 0.5s ease-in-out;
    transition: all 0.5s ease-in-out;
    -webkit-border-radius: 5px 5px 5px 5px;
    border-radius: 5px 5px 5px 5px;
}

input[type="text"]:focus {
    background-color: #fff;
    border-bottom: 2px solid #5fbae9;
}

input[type="text"]:placeholder {
    color: #cccccc;
}

/* ANIMATIONS */

/* Simple CSS3 Fade-in-down Animation */
.fadeInDown {
    -webkit-animation-name: fadeInDown;
    animation-name: fadeInDown;
    -webkit-animation-duration: 1s;
    animation-duration: 1s;
    -webkit-animation-fill-mode: both;
    animation-fill-mode: both;
}

@-webkit-keyframes fadeInDown {
    0% {
        opacity: 0;
        -webkit-transform: translate3d(0, -100%, 0);
        transform: translate3d(0, -100%, 0);
    }
    100% {
        opacity: 1;
        -webkit-transform: none;
        transform: none;
    }
}

@keyframes fadeInDown {
    0% {
        opacity: 0;
        -webkit-transform: translate3d(0, -100%, 0);
        transform: translate3d(0, -100%, 0);
    }
    100% {
        opacity: 1;
        -webkit-transform: none;
        transform: none;
    }
}

/* Simple CSS3 Fade-in Animation */
@-webkit-keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
@-moz-keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}
@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

.fadeIn {
    opacity: 0;
    -webkit-animation: fadeIn ease-in 1;
    -moz-animation: fadeIn ease-in 1;
    animation: fadeIn ease-in 1;

    -webkit-animation-fill-mode: forwards;
    -moz-animation-fill-mode: forwards;
    animation-fill-mode: forwards;

    -webkit-animation-duration: 1s;
    -moz-animation-duration: 1s;
    animation-duration: 1s;
}

.fadeIn.first {
    -webkit-animation-delay: 0.4s;
    -moz-animation-delay: 0.4s;
    animation-delay: 0.4s;
}

.fadeIn.second {
    -webkit-animation-delay: 0.6s;
    -moz-animation-delay: 0.6s;
    animation-delay: 0.6s;
}

.fadeIn.third {
    -webkit-animation-delay: 0.8s;
    -moz-animation-delay: 0.8s;
    animation-delay: 0.8s;
}

.fadeIn.fourth {
    -webkit-animation-delay: 1s;
    -moz-animation-delay: 1s;
    animation-delay: 1s;
}

/* Simple CSS3 Fade-in Animation */
.underlineHover:after {
    display: block;
    left: 0;
    bottom: -10px;
    width: 0;
    height: 2px;
    background-color: #56baed;
    content: "";
    transition: width 0.2s;
}

.underlineHover:hover {
    color: #0d0d0d;
}

.underlineHover:hover:after {
    width: 100%;
}

/* OTHERS */

*:focus {
    outline: none;
}

#icon {
    width: 60%;
}
</style>
