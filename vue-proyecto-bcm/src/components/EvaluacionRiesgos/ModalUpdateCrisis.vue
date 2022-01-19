<template>
	<v-dialog v-model="dialog" id="modal-crear">
		<template v-slot:activator="{ on, attrs }">
			<v-icon
				color="yellow"
				title="Editar escenario crítico"
				v-bind="attrs"
				v-on="on"
				v-on:click="getDetail"
				>mdi-notebook-edit
			</v-icon>
		</template>

		<v-card>
			<v-form ref="formulario" v-model="formValido" lazy-validation>
				<v-card-title class="header-table">
					<v-row justify="space-between" class="pa-1">
						<span class="text-h5">Editar escenario crítico</span>
						<v-btn icon @click="dialog = false">
							<v-icon color="white">mdi-close</v-icon>
						</v-btn>
					</v-row>
				</v-card-title>
				<v-divider></v-divider>
				<v-card-text>
					<v-container>
						<v-text-field
							v-model="crisis.name"
							:counter="50"
							:rules="[(v) => !!v || 'Este campo es obligatorio']"
							label="Ingrese el título del escenario crítico"
						></v-text-field>
						<v-row>
							<v-col cols="12" sm="12" md="12" lg="12" xl="12">
								<v-textarea
									v-model="crisis.description"
									label="Ingrese la descripción del escenario crítico"
									hint="La descripción debería tener entre 10 y 200 caracteres"
									:rules="[
										(v) =>
											!!v || 'Este campo es obligatorio',
									]"
								></v-textarea>
							</v-col>
						</v-row>
					</v-container>
				</v-card-text>
			</v-form>

			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn color="primary darken-1" @click="dialog = false" text>
					Cerrar
				</v-btn>
				<!--v-btn color="primary" v-on:click="crear">
						Crear riesgo
					</v-btn-->
				<modal-confirm-update-crisis
					v-on:editar="Editar"
				></modal-confirm-update-crisis>
			</v-card-actions>

			<alert-error
				:message="mensajeError"
				:snackbar="snackbar"
				v-on:alertend="alertEnd"
			></alert-error>
		</v-card>
	</v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import { SERVER_ADDRESS, TOKEN } from '../../../config/config'

import ModalConfirmUpdateCrisis from './ModalConfirmUpdateCrisis.vue'
import AlertError from '../Genericos/AlertError.vue'

interface Crisis {
	name: string
	description: string
}

//import { validationMixin } from 'vuelidate';
//import { required, maxLength, email } from 'vuelidate/lib/valid;

export default Vue.extend({
	components: {
		AlertError,
		ModalConfirmUpdateCrisis,
	},
	props: ['id'],

	/*
	mixins: [validationMixin],

    validations: {
      name: { required, maxLength: maxLength(10) },
      email: { required, email },
      select: { required },
      checkbox: {
        checked (val) {
          return val
        },
      },
    },
	*/

	data() {
		return {
			estaCargando: true,
			formValido: true,
			dialog: false,

			crisis: {
				name: '',
				description: '',
			} as Crisis,

			//Para el manejo del mensaje
			mensajeError: '' as string,
			snackbar: false as boolean,
		}
	},
	computed: {
		/*
      nameErrors () {
        const errors = []
        if (!this.$v.name.$dirty) return errors
        !this.$v.name.maxLength && errors.push('Name must be at most 10 characters long')
        !this.$v.name.required && errors.push('Name is required.')
        return errors
      },
		*/
	},
	methods: {
		async getDetail() {
			console.log('[ID del riesgo detalle] ', this.$props.id)

			axios
				.get<Crisis>(
					`${SERVER_ADDRESS}/api/risks/crisis_scenario/${this.$props.id}/`,
					{
						withCredentials: true,
						headers: {
							Authorization: TOKEN,
						},
					}
				)
				.then((res) => {
					console.log(res.data)

					this.crisis = {
						name: res.data.name,
						description: res.data.description,
					}
				})
				.catch(function (error) {
					console.log('Ups! Ha ocurrido un error en el servidor')
					console.log(error.toJSON())
				})
		},
		async Editar() {
			console.log('Objeto a enviar para actualizar crisis: ')
			console.log(this.crisis)

			axios
				.patch(
					`${SERVER_ADDRESS}/api/risks/crisis_scenario/${this.$props.id}/`,
					this.crisis,
					{
						withCredentials: true,
						headers: {
							Authorization: TOKEN,
						},
					}
				)
				.then((res) => {
					this.estaCargando = false

					console.log(
						'[Escenario crítico actualizado satisfactoriamente]'
					)

					this.dialog = false

					//Reinicializamos variable del crear
					this.crisis = {
						name: '',
						description: '',
					}

					this.$emit(
						'alertexito',
						'¡El escenario crítico ha sido actualizado satisfactoriamente!'
					)
				})
				.catch((err) => {
					try {
						console.log('Error')
						console.log(err)
						console.log(err.response)
						// Error 400 por unicidad o 500 generico
						if (err.response.status == 400) {
							this.mensajeError = err.response.data
							this.snackbar = true
						} else {
							// Servidor no disponible
							this.mensajeError =
								'Ups! Ha ocurrido un error en el servidor'
							this.snackbar = true
						}
					} catch {
						// Servidor no disponible
						this.mensajeError =
							'Ups! Ha ocurrido un error en el servidor'
						this.snackbar = true
					}
				})
		},
		alertEnd() {
			this.snackbar = false
		},
	},
})
</script>

<style></style>