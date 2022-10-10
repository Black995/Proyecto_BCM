<template>
    <div class="row">
        <div class="col-xl-4 col-lg-5 col-md-6">
            <card class="card-user">
                <div class="text-center">
                    <b-img
                        height="150"
                        width="150"
                        src="../../assets/img/login_icon.png"
                        fluid
                        :alt="profile.names"
                    ></b-img>
                </div>

                <div class="mt-3">
                    <h3 class="text-center">
                        {{ profile.names }} {{ profile.surnames }}
                    </h3>
                    <h5 class="text-center">
                        Correo:
                        {{ profile.email }}
                    </h5>
                    <p class="description">
                        Número de identificación:
                        {{ profile.staff_number }}
                    </p>
                    <p class="description">
                        Area:
                        {{ profile.area_name }}
                    </p>
                    <p class="description">
                        Cargo:
                        {{ profile.position_name }}
                    </p>
                    <p class="description">
                        Sede:
                        {{ profile.headquarter_name }}
                    </p>
                </div>
            </card>
        </div>
        <div class="col-xl-8 col-lg-7 col-md-6">
            <b-card-group deck>
                <b-card>
                    <b-list-group flush>
                        <b-list-group-item
                            style="background: #d8d8d8"
                            class="flex-column align-items-start"
                        >
                            <strong>Roles del usuario</strong>
                        </b-list-group-item>
                        <b-list-group-item
                            href="#"
                            class="flex-column align-items-start"
                            v-for="item in profile.groups"
                            :key="item.key"
                        >
                            {{ item.name }}
                        </b-list-group-item>
                    </b-list-group>
                </b-card>
            </b-card-group>
            <card class="card mt-3" title="Editar datos del perfil">
                <div>
                    <form>
                        <b-row align-v="center">
                            <b-col>
                                <b-form-group
                                    label="Ingrese sus nombres"
                                    invalid-feedback="Este campo es obligatorio"
                                    :state="profileState.names"
                                >
                                    <b-form-input
                                        v-model="profileEdit.names"
                                        :state="profileState.names"
                                        required
                                    ></b-form-input>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                    label="Ingrese sus apellidos"
                                    invalid-feedback="Este campo es obligatorio"
                                    :state="profileState.surnames"
                                >
                                    <b-form-input
                                        v-model="profileEdit.surnames"
                                        :state="profileState.surnames"
                                        required
                                    ></b-form-input>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        <b-row>
                            <b-col>
                                <b-form-group
                                    label="Ingrese el número de staff"
                                    invalid-feedback="Este campo es obligatorio"
                                    :state="profileState.staff_number"
                                >
                                    <b-form-input
                                        v-model="profileEdit.staff_number"
                                        :state="profileState.staff_number"
                                        required
                                    ></b-form-input>
                                </b-form-group>
                            </b-col>
                            <b-col>
                                <b-form-group
                                    label="Seleccione el área a la que pertenece"
                                    invalid-feedback="Este campo es obligatorio"
                                    :state="profileState.area"
                                >
                                    <b-form-select
                                        v-model="profileEdit.area"
                                        :options="areas"
                                        value-field="id"
                                        text-field="name"
                                        :state="profileState.area"
                                        required
                                    ></b-form-select>
                                </b-form-group>
                            </b-col>
                        </b-row>
                        <div class="text-center mt-3">
                            <b-button
                                variant="info"
                                round
                                @click="handleSubmitUpdate(profile.staff)"
                            >
                                Actualizar
                            </b-button>
                        </div>
                        <div class="clearfix"></div>
                    </form>
                </div>
            </card>

            <b-modal
                id="modal-confirm-update"
                title="Confirmar editar datos del perfil"
                centered
            >
                <h4>¿Está seguro de editar los datos del perfil?</h4>
                <template #modal-footer>
                    <div class="w-100">
                        <b-button
                            variant="info"
                            class="float-right"
                            @click="updateProfile"
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
    name: "Profile",

    data: () => ({
        profileId: 0,

        profile: {
            id: 0,
            staff: 0,
            email: "",
            names: "",
            surnames: "",
            staff_number: "",
            area_name: "",
            position_name: "",
            headquarter_name: "",
            groups: [],
        },
        profileEdit: {
            names: "",
            surnames: "",
            staff_number: "",
            area: 0,
        },
        profileState: {
            names: null,
            surnames: null,
            staff_number: null,
            area: null,
        },

        areas: [],
    }),
    mounted() {
        this.getProfile();
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
        async getAreas() {
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
        async getProfile() {
            this.profile = {
                email: "",
                names: "",
                surnames: "",
                staff_number: "",
                area_name: "",
                position_name: "",
                headquarter_name: "",
                groups: [],
            };
            this.profileEdit = {
                names: "",
                surnames: "",
                staff_number: "",
                area: 0,
            };
            axios
                .get(`${SERVER_ADDRESS}/api/users/profile/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.profile = res.data;
                    this.profileEdit = {
                        names: res.data.names,
                        surnames: res.data.surnames,
                        staff_number: res.data.staff_number,
                        area: res.data.area,
                    };

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
         * Validar formularios
         */
        checkFormValidity() {
            let valid = true;
            if (!this.profileEdit.names) {
                this.profileState.names = false;
                valid = false;
            }
            if (!this.profileEdit.surnames) {
                this.profileState.surnames = false;
                valid = false;
            }
            if (!this.profileEdit.staff_number) {
                this.profileState.staff_number = false;
                valid = false;
            }
            return valid;
        },
        /**
         * Update
         */
        handleSubmitUpdate(staff_id) {
            this.profileId = staff_id;
            // Inicializamos variables de estados
            this.profileState.names = null;
            this.profileState.surnames = null;
            this.profileState.staff_number = null;
            this.profileState.area = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-update");
            });
        },
        async updateProfile() {
            console.log("Editar perfil");
            console.log(this.profileEdit);
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/staff/${this.profileId}/`,
                    this.profileEdit,
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
                        "¡Los datos del perfil han sido actualizados exitosamente!"
                    );

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getProfile();
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
