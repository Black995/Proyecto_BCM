<template>
	<v-dialog v-model="dialog" persistent max-width="350">
		<template v-slot:activator="{ on, attrs }">
			<v-icon
				color="red"
				style="color: black"
				title="Eliminar riesgo"
				v-bind="attrs"
				v-on="on"
			>
				mdi-delete-forever
			</v-icon>
		</template>

		<v-card>
			<v-card-title class="text-h5">
				¿Está seguro de eliminar este escenario crítico?
			</v-card-title>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn color="primary darken-1" text @click="dialog = false">
					Cerrar
				</v-btn>
				<v-btn color="primary" text @click="confirmDelete">
					Confirmar
				</v-btn>
			</v-card-actions>
		</v-card>

		<alert-error
			:mensaje="mensajeError"
			:snackbar="snackbar"
			v-on:alertfin="alertaFin"
		></alert-error>
	</v-dialog>
</template>


<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import { SERVER_ADDRESS, TOKEN } from '../../../config/config'
import AlertError from '../Genericos/AlertError.vue'

export default Vue.extend({
	components: {
		AlertError,
	},
	props: ['id'],
	data() {
		return {
			dialog: false,

			//Para el manejo del mensaje de error
			mensajeError: '',
			snackbar: false,
		}
	},
	methods: {
		async confirmDelete() {
			axios
				.delete(
					`${SERVER_ADDRESS}/api/risks/crisis_scenario/${this.$props.id}/`,
					{
						withCredentials: true,
						headers: {
							Authorization: TOKEN,
						},
					}
				)
				.then((res) => {
					//Si la oferta fue eliminada exitosamente, mostramos mensaje de éxito y cerramos el modal
					this.dialog = false

					this.$emit(
						'alertexito',
						'¡El escenario crítico ha sido eliminado satisfactoriamente!'
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
		alertaFin() {
			this.snackbar = false
		},
	},
})
</script>

