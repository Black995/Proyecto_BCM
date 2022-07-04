<template>
    <div class="row">
        <div class="col-xl-4 col-lg-5 col-md-6">
            <card class="card-user">
                <div slot="image">
                    <b-img :src="org.logo" fluid alt="Responsive image"></b-img>
                </div>
                <div>
                    <p><strong>Imagen de texto:</strong> {{ org.logo }}</p>
                    <h3 class="text-center">
                        {{ org.name }}
                    </h3>
                    <h5 class="text-center">
                        Número legal: <strong>{{ org.legal_id }}</strong>
                    </h5>
                    <p class="description text-center">
                        {{ org.description }}
                    </p>
                </div>
            </card>
        </div>
        <div class="col-xl-8 col-lg-7 col-md-6">
            <card class="card" title="Edit Profile">
                <div>
                    <form @submit.prevent>
                        <div class="row">
                            <div class="col-md-12">
                                <fg-input
                                    type="text"
                                    label="Address"
                                    placeholder="Home Address"
                                    v-model="user.address"
                                >
                                </fg-input>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-12">
                                <div class="form-group">
                                    <label>About Me</label>
                                    <textarea
                                        rows="5"
                                        class="form-control border-input"
                                        placeholder="Here can be your description"
                                        v-model="user.aboutMe"
                                    >
                                    </textarea>
                                </div>
                            </div>
                        </div>
                        <div class="text-center">
                            <p-button type="info" round>
                                Update Profile
                            </p-button>
                        </div>
                        <div class="clearfix"></div>
                    </form>
                </div>
            </card>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import NotificationTemplate from "../Notifications/NotificationTemplate";

export default {
    name: "Organization",

    data: () => ({
        orgId: 0,

        org: {
            name: "",
            legal_id: "",
            description: "",
            logo: "",
        },
        areaState: {
            name: null,
            legal_id: null,
            description: null,
            logo: null,
        },

        user: {
            company: "Paper Dashboard",
            username: "michael23",
            email: "",
            firstName: "Chet",
            lastName: "Faker",
            address: "Melbourne, Australia",
            city: "Melbourne",
            postalCode: "",
            aboutMe: `We must accept finite disappointment, but hold on to infinite hope.`,
        },
    }),
    mounted() {
        this.getOrganization();
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

        async getOrganization() {
            this.org = {
                name: "",
                legal_id: "",
                description: "",
                logo: "",
            };
            axios
                .get(`${SERVER_ADDRESS}/api/config/organizations/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.org = res.data[0];
                    console.log(this.org);
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
         * Validar formularios
         */
        checkFormValidity() {
            let valid = true;
            if (!this.org.name) {
                this.orgState.name = false;
                valid = false;
            }
            return valid;
        },
        resetModal() {
            this.org.name = "";
            this.orgState.name = null;
        },
        /**
         * Update
         */
        handleSubmitUpdate() {
            // Inicializamos variables de estados
            this.orgState.name = null;

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
            this.orgId = id;
        },
        async updateOrg() {
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/config/organization/${this.orgId}/`,
                    this.org,
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
                        "¡Los datos de la empresa han sido actualizados exitosamente!"
                    );

                    // Cargamos de nuevo la tabla de riesgos
                    this.getOrganization();
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
