<template>
    <div class="row">
        <div class="col-xl-4 col-lg-5 col-md-6">
            <card class="card-user">
                <div slot="image">
                    <b-img
                        :src="'data:image/jpeg;base64,' + org.logo_base64"
                        fluid
                        :alt="org.name"
                    ></b-img>
                </div>
                <div>
                    <h3 class="text-center">
                        {{ org.name }}
                    </h3>
                    <h5 class="text-center">
                        Identificación legal:
                        {{ org.legal_id }}
                    </h5>
                    <p class="description text-center">
                        {{ org.description }}
                    </p>
                </div>
            </card>
        </div>
        <div class="col-xl-8 col-lg-7 col-md-6">
            <card class="card" title="Editar datos de la empresa">
                <div>
                    <form>
                        <b-form-group
                            label="Ingrese el nombre de la empresa"
                            invalid-feedback="Este campo es obligatorio"
                            :state="orgState.name"
                        >
                            <b-form-input
                                v-model="orgEdit.name"
                                :state="orgState.name"
                                required
                            >
                            </b-form-input>
                        </b-form-group>
                        <b-form-group
                            label="Ingrese la identificación legal de la empresa"
                            invalid-feedback="Este campo es obligatorio"
                            :state="orgState.legal_id"
                        >
                            <b-form-input
                                v-model="orgEdit.legal_id"
                                :state="orgState.legal_id"
                                required
                            >
                            </b-form-input>
                        </b-form-group>
                        <b-form-group
                            label="Ingrese la descripción de la empresa"
                            invalid-feedback="Este campo es obligatorio"
                            :state="orgState.description"
                        >
                            <b-form-textarea
                                v-model="orgEdit.description"
                                :state="orgState.description"
                                required
                                rows="3"
                            ></b-form-textarea>
                        </b-form-group>
                        <b-form-file
                            v-model="orgEdit.logo"
                            :state="orgState.logo"
                            placeholder="Elija un archivo o arrástrelo aquí"
                            drop-placeholder="Arrastre el archivo aquí"
                        ></b-form-file>
                        <div class="text-center mt-3">
                            <b-button
                                variant="info"
                                round
                                @click="handleSubmitUpdate(org.id)"
                            >
                                Actualizar
                            </b-button>
                        </div>
                        <div class="clearfix"></div>
                    </form>

                    <!--form @submit.prevent>
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
                            <p-button
                                type="info"
                                round
                                @click="handleSubmitUpdate(org.id)"
                            >
                                Actualizar
                            </p-button>
                        </div>
                        <div class="clearfix"></div>
                    </form-->
                </div>
            </card>

            <!--
                Modal confirmar actualizar
            -->
            <b-modal
                id="modal-confirm-update"
                title="Confirmar editar datos de la empresa"
                centered
            >
                <h4>¿Está seguro de editar los datos de la empresa?</h4>
                <template #modal-footer>
                    <div class="w-100">
                        <b-button
                            variant="info"
                            class="float-right"
                            @click="updateOrg"
                        >
                            Confirmar
                        </b-button>
                    </div>
                </template>
            </b-modal>
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
            id: 0,
            name: "",
            legal_id: "",
            description: "",
            logo: null,
            logo_base64: null,
        },
        orgEdit: {
            name: "",
            legal_id: "",
            description: "",
            logo: null,
        },
        orgState: {
            name: null,
            legal_id: null,
            description: null,
            logo: null,
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
                logo: null,
                logo_base64: null,
            };
            this.orgEdit = {
                name: "",
                legal_id: "",
                description: "",
                logo: null,
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
                    this.orgEdit = {
                        name: res.data[0].name,
                        legal_id: res.data[0].legal_id,
                        description: res.data[0].description,
                        logo: null,
                    };
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
            if (!this.orgEdit.name) {
                this.orgState.name = false;
                valid = false;
            }
            if (!this.orgEdit.legal_id) {
                this.orgState.legal_id = false;
                valid = false;
            }
            if (!this.orgEdit.description) {
                this.orgState.description = false;
                valid = false;
            }
            return valid;
        },
        /**
         * Update
         */
        handleSubmitUpdate(id) {
            this.orgId = id;
            // Inicializamos variables de estados
            this.orgState.name = null;
            this.orgState.legal_id = null;
            this.orgState.description = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-update");
            });
        },
        async updateOrg() {
            let formData = new FormData();
            formData.append("name", this.orgEdit.name);
            formData.append("legal_id", this.orgEdit.legal_id);
            formData.append("description", this.orgEdit.description);
            if (this.orgEdit.logo) {
                formData.append(
                    "logo",
                    this.orgEdit.logo,
                    this.orgEdit.logo.name
                );
            }

            axios
                .patch(
                    `${SERVER_ADDRESS}/api/config/organization/${this.orgId}/`,
                    formData,
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

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                    });

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
