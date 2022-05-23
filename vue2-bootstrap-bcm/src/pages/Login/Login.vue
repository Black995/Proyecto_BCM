<template>
    <div>
        <div class="login">
            <h1 class="text-center">Login</h1>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { SERVER_ADDRESS } from "../../../config/config";

export default {
    name: "Login",

    data: () => ({
        validForm: false,
        loadingForm: false,

        user: {
            email: "",
            password: "",
        },
    }),
    /**
     * Se deja el mounted termporalmente
     */
    mounted() {
        this.user = {
            email: "alansaul25@gmail.com",
            password: "12345",
        };
        this.login();
    },
    methods: {
        async login() {
            //if (this.$refs.form.validate()) {
            this.loadingForm = true;

            axios
                .post(`${SERVER_ADDRESS}/api/token/`, this.user)
                .then((res) => {
                    if (res.status === 200) {
                        /**
                         * Se guarda el token en local storage (provicionalmente)
                         */
                        localStorage.setItem("token", res.data.access);
                        this.$router.push("/riesgos");
                    }
                })
                .catch((err) => {
                    try {
                        if (err.response.status == 400) {
                            console.log(err.response.data);
                        } else {
                            this.loadingForm = false;
                            //this.$refs.form.reset();
                            console.log("Ha surgido un error en el servidor");
                            //this.mensajeError =
                            //	error.response.status === 500
                            //		? 'Ha ocurrido un error inesperado en el servidor, por favor inténtalo de nuevo.'
                            //		: 'Correo electrónico o contraseña incorrecta.'
                        }
                    } catch {
                        console.log("Ha surgido un error en el servidor");
                        //this.mensajeError =
                        //	'Ha ocurrido un error inesperado en el servidor, por favor inténtalo de nuevo.'
                    }
                });
            //}
        },
    },
};
</script>

<style>
.login {
    background: #f1f1f1;
}
</style>
