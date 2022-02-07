<template>
	<v-dialog v-model="dialog" id="modal-crear">
		<template v-slot:activator="{ on, attrs }">
			<v-btn
				class="mx-2"
				fab
				dark
				small
				color="yellow"
				title="Editar riesgo"
				v-bind="attrs"
				v-on="on"
				v-on:click="getDetail"
			>
				<v-icon color="black">mdi-notebook-edit </v-icon>
			</v-btn>
		</template>

		<v-card>
			<v-form ref="form" v-model="validForm" lazy-validation>
				<v-card-title class="header-table">
					<v-row justify="space-between" class="pa-1">
						<span class="text-h5">Editar riesgo</span>
						<v-btn icon @click="dialog = false">
							<v-icon color="white">mdi-close</v-icon>
						</v-btn>
					</v-row>
				</v-card-title>
				<v-divider></v-divider>
				<v-card-text>
					<v-container>
						<v-row v-show="loading">
							<v-progress-linear
								indeterminate
								color="primary"
							></v-progress-linear
						></v-row>
						<v-text-field
							v-model="risk.name"
							:counter="50"
							:rules="rules.name"
							label="Ingrese el título del escenario crítico"
						></v-text-field>
						<v-row>
							<v-col cols="12" sm="12" md="12" lg="12" xl="12">
								<v-textarea
									v-model="risk.description"
									:counter="200"
									label="Ingrese la descripción del escenario crítico"
									hint="La descripción debería tener entre 10 y 200 caracteres"
									:rules="rules.description"
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
					:disabled="validForm"
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

import ModalConfirmUpdateCrisis from './ModalConfirmUpdateRisk.vue'
import AlertError from '../Genericos/AlertError.vue'

interface Risk {
	name: string
	description: string
}

export default Vue.extend({
	components: {
		AlertError,
		ModalConfirmUpdateCrisis,
	},
	props: ['id'],

	data() {
		return {
			loading: true,
			validForm: false,
			dialog: false,

			risk: {
				name: '',
				description: '',
			} as Risk,

			//Para el manejo del mensaje
			mensajeError: '' as string,
			snackbar: false as boolean,

			rules: {
				name: [
					(v: any) => !!v || 'Este campo es obligatorio',
					(v: any) =>
						(v && v.length <= 50) ||
						'El nombre debe contener como máximo 50 caracteres',
					//Validación de correo
					//v => v === null || v.length === 0 || (/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(v)) || 'Debe ser un correo electrónico valido'
				],
				description: [
					(v: any) => !!v || 'Este campo es obligatorio',
					(v: any) =>
						(v && v.length >= 10 && v && v.length <= 200) ||
						'La descripción debe contener entre 10 y 200 caracteres',
				],
			},
		}
	},
	methods: {
		async getDetail() {
			console.log('[ID del riesgo detalle] ', this.$props.id)

			axios
				.get<Risk>(
					`${SERVER_ADDRESS}/api/phase1/risk/${this.$props.id}/`,
					{
						withCredentials: true,
						headers: {
							Authorization: TOKEN,
						},
					}
				)
				.then((res) => {
					this.loading = false

					this.risk = res.data
				})
				.catch(function (error) {
					console.log('Ups! Ha ocurrido un error en el servidor')
					console.log(error.toJSON())
				})
		},
		async Editar() {
			console.log('Objeto a enviar: ')
			console.log(this.risk)

			//Validación de los inputs
			if (
				!(
					this.$refs.form as Vue & { validate: () => boolean }
				).validate()
			)
				return

			axios
				.patch(
					`${SERVER_ADDRESS}/api/phase1/risk/${this.$props.id}/`,
					this.risk,
					{
						withCredentials: true,
						headers: {
							Authorization: TOKEN,
						},
					}
				)
				.then((res) => {
					this.loading = false

					console.log('[Riesgo actualizado satisfactoriamente]')

					this.dialog = false

					//Reinicializamos variable del crear
					this.risk = {
						name: '',
						description: '',
					}

					this.$emit(
						'alertexito',
						'¡El riesgo ha sido actualizado satisfactoriamente!'
					)
				})
				.catch((err) => {
					try {
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