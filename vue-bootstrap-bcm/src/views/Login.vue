<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <h1 class="text-center">Login</h1>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import { SERVER_ADDRESS } from "../../config/config";

interface User {
    email: string;
    password: string;
}

export default Vue.extend({
    data() {
        return {
            estaCargando: true,
            validForm: false,
            loadingForm: false,
            dialog: false,

            user: {
                email: "",
                password: "",
            } as User,

            //Para el manejo del mensaje
            mensajeError: "" as string,
            snackbar: false as boolean,
        };
    },
    methods: {
        async login() {
            //if (this.$refs.form.validate()) {
            this.mensajeError = "";
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
                .catch((error) => {
                    try {
                        this.loadingForm = false;
                        //this.$refs.form.reset();
                        this.mensajeError =
                            error.response.status === 500
                                ? "Ha ocurrido un error inesperado en el servidor, por favor inténtalo de nuevo."
                                : "Correo electrónico o contraseña incorrecta.";
                    } catch {
                        this.mensajeError =
                            "Ha ocurrido un error inesperado en el servidor, por favor inténtalo de nuevo.";
                    }
                });
            //}
        },
    },
});
</script>

<style lang="scss">
.login {
    background: #f1f1f1;
}
</style>
