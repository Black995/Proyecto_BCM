<template>
    <div>
        <div class="modal-header">
            <h4 class="modal-title">Crear Crisis</h4>
            <button
                type="button"
                class="close"
                data-dismiss="modal"
                aria-label="Close"
                @click="dialog = false"
            >
                <span aria-hidden="true">&times;</span>
            </button>
        </div>
        <div class="modal-body">
            <form ref="form">
                <div class="form-group">
                    <label><b>Nombre:</b></label>
                    <input
                        formControlName="name"
                        [class]="validate_control('name')"
                        type="text"
                        placeholder="Ingrese el nombre del documento..."
                    />
                    <!--div class="mt-1 mb-2 text-danger" *ngIf="document_form.controls['name'].invalid && 
        (document_form.controls['name'].dirty || document_form.controls['name'].touched)">
          <div *ngIf="document_form.controls['name'].errors?.required">
            El campo "Documento Oficial" no puede estar vacío.
          </div>
        </div-->
                </div>
                <div class="form-group">
                    <label><b>Descripción:</b></label>
                    <input
                        formControlName="name"
                        [class]="validate_control('name')"
                        type="text"
                        placeholder="Ingrese el nombre del documento..."
                    />
                    <!--div class="mt-1 mb-2 text-danger" *ngIf="document_form.controls['name'].invalid && 
        (document_form.controls['name'].dirty || document_form.controls['name'].touched)">
          <div *ngIf="document_form.controls['name'].errors?.required">
            El campo "Documento Oficial" no puede estar vacío.
          </div>
        </div-->
                </div>

                <hr
                    *ngIf="document_form.get('link') || document_form.get('file')"
                />
                <div class="form-group text-right mt-3">
                    <button
                        type="submit"
                        class="btn btn-md btn-success mr-3"
                        @click="confirm_create"
                    >
                        Crear
                    </button>
                    <button
                        type="button"
                        class="btn btn-md btn-danger"
                        data-dismiss="modal"
                        @click="close_modal()"
                    >
                        Cerrar
                    </button>
                </div>
            </form>
        </div>

        <!--v-dialog v-model="dialog" id="modal-crear">
		<template v-slot:activator="{ on, attrs }">
			<v-btn
				color="secondary"
				style="color: black"
				rounded
				v-bind="attrs"
				v-on="on"
			>
				Agregar riesgo
			</v-btn>
		</template>

		<v-card>
			<v-form ref="form" v-model="validForm" lazy-validation>
				<v-card-title class="header-table">
					<v-row justify="space-between" class="pa-1">
						<span class="text-h5">Crear nuevo riesgo</span>
						<v-btn icon @click="dialog = false">
							<v-icon color="white">mdi-close</v-icon>
						</v-btn>
					</v-row>
				</v-card-title>
				<v-divider></v-divider>
				<v-card-text>
					<v-container>
						<v-text-field
							v-model="risk.name"
							:counter="50"
							:rules="rules.name"
							label="Ingrese el título del riesgo"
						></v-text-field>

						<v-row>
							<v-col cols="12" sm="12" md="12" lg="12" xl="12">
								<v-textarea
									v-model="risk.description"
									:counter="200"
									label="Ingrese la descripción del riesgo"
									hint="La descripción debería tener entre 10 y 200 caracteres"
									:rules="rules.description"
								></v-textarea>
							</v-col>
						</v-row>
					</v-container>
				</v-card-text>

				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn
						color="primary darken-1"
						@click="dialog = false"
						text
					>
						Cerrar
					</v-btn>
					<modal-confirm-create-risk
						:disabled="validForm"
						v-on:crear="Crear"
					></modal-confirm-create-risk>
				</v-card-actions>

				<alert-error
					:message="mensajeError"
					:snackbar="snackbar"
					v-on:alertend="alertEnd"
				></alert-error>
			</v-form>
		</v-card>
	</v-dialog-->
    </div>
</template>

<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";

import ModalConfirmCreateRisk from "./ModalConfirmCreateRisk.vue";
import AlertError from "../Genericos/AlertError.vue";

export default {
    components: {
        AlertError,
        ModalConfirmCreateRisk,
    },

    data() {
        return {
            loading: true,
            validForm: false,
            dialog: false,

            risk: {
                name: "",
                description: "",
            },
            criticidad: ["Alto", "Mediano", "Bajo"],

            //Para el manejo del mensaje
            mensajeError: "",
            snackbar: false,

            rules: {
                name: [
                    (v) => !!v || "Este campo es obligatorio",
                    (v) =>
                        (v && v.length <= 50) ||
                        "El nombre debe contener como máximo 50 caracteres",
                    //Validación de correo
                    //v => v === null || v.length === 0 || (/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(v)) || 'Debe ser un correo electrónico valido'
                ],
                description: [
                    (v) => !!v || "Este campo es obligatorio",
                    (v) =>
                        (v && v.length >= 10 && v && v.length <= 200) ||
                        "La descripción debe contener entre 10 y 200 caracteres",
                ],
            },
        };
    },
    methods: {
        confirm_create() {},
        async Crear() {
            //Validación de los inputs
            /*
			if (
				!(
					this.$refs.form as Vue & { validate: () => boolean }
				).validate()
			)
				return
			*/

            axios
                .post(`${SERVER_ADDRESS}/api/phase1/risks/`, this.risk, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.loading = false;
                    this.dialog = false;

                    //Reinicializamos variable del crear
                    this.risk = {
                        name: "",
                        description: "",
                    };

                    this.$emit(
                        "alertexito",
                        "¡El riesgo ha sido creado satisfactoriamente!"
                    );
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.mensajeError = err.response.data;
                            this.snackbar = true;
                        } else {
                            // Servidor no disponible
                            this.mensajeError =
                                "Ups! Ha ocurrido un error en el servidor";
                            this.snackbar = true;
                        }
                    } catch {
                        // Servidor no disponible
                        this.mensajeError =
                            "Ups! Ha ocurrido un error en el servidor";
                        this.snackbar = true;
                    }
                });
        },
        alertEnd() {
            this.snackbar = false;
        },
    },
};
</script>

<style></style>