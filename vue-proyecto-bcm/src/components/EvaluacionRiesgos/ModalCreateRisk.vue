<template>
	<v-dialog v-model="dialog" id="modal-crear">
		<template v-slot:activator="{ on, attrs }">
			<v-btn
				color="secondary"
				style="color: black"
				rounded
				v-bind="attrs"
				v-on="on"
			>
				Agregar un nuevo riesgo
			</v-btn>
		</template>

		<v-card>
			<v-form ref="formulario" v-model="formValido" lazy-validation>
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
							:rules="[(v) => !!v || 'Este campo es obligatorio']"
							label="Ingrese el título del riesgo"
						></v-text-field>

						<!--v-row>
							<v-col cols="6" sm="6" md="6" lg="6" xl="6">
								<v-select
									v-model="riesgo.criticidad"
									:items="criticidad"
									:rules="[
										(v) =>
											!!v || 'Este campo es obligatorio',
									]"
									label="Criticidad"
									required
								></v-select>
							</v-col>
							<v-col cols="6" sm="6" md="6" lg="6" xl="6">
								<v-text-field
									v-model="riesgo.porcentaje"
									:counter="3"
									:rules="[
										(v) =>
											!!v || 'Este campo es obligatorio',
									]"
									label="Ingrese el porcentaje"
									required
								></v-text-field>
							</v-col>
						</v-row-->
						<v-row>
							<v-col cols="12" sm="12" md="12" lg="12" xl="12">
								<v-textarea
									v-model="risk.description"
									label="Ingrese la descripción del riesgo"
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

				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn
						color="primary darken-1"
						@click="dialog = false"
						text
					>
						Cerrar
					</v-btn>
					<!--v-btn color="primary" v-on:click="crear">
						Crear riesgo
					</v-btn-->
					<modal-confirm-create-risk
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
	</v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import { SERVER_ADDRESS, TOKEN } from '../../../config/config'

import ModalConfirmCreateRisk from './ModalConfirmCreateRisk.vue'
import AlertError from '../Genericos/AlertError.vue'

interface Risk {
	name: string
	description: string
}

/*
interface Riesgo {
	titulo: string
	descripcion: string
	criticidad: string
	porcentaje: number
}
*/

//import { validationMixin } from 'vuelidate';
//import { required, maxLength, email } from 'vuelidate/lib/valid;

export default Vue.extend({
	components: {
		AlertError,
		ModalConfirmCreateRisk,
	},

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

			risk: {
				name: '',
				description: '',
			} as Risk,
			criticidad: ['Alto', 'Mediano', 'Bajo'],

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
		async Crear() {
			console.log('Objeto a enviar: ')
			console.log(this.risk)

			axios
				.post(`${SERVER_ADDRESS}/api/risks/risks/`, this.risk, {
					withCredentials: true,
					headers: {
						Authorization: TOKEN,
					},
				})
				.then((res) => {
					if (res.status == 200 || res.status == 201) {
						this.estaCargando = false

						console.log('[Oferta creada satisfactoriamente]')

						//Si la oferta fue exitosamente creada, mostramos mensaje de éxito y cerramos el modal
						this.dialog = false

						//Reinicializamos variable del crear
						this.risk = {
							name: '',
							description: '',
						}

						this.$emit(
							'alertexito',
							'¡El riesgo ha sido creado satisfactoriamente!'
						)
					}
				})
				.catch((err) => {
					try {
						// Error 400 por unicidad o 500 generico
						if (err.response.status) {
							this.mensajeError = err.response.data
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