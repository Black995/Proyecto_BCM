<template>
	<v-dialog v-model="dialog">
		<template v-slot:activator="{ on, attrs }">
			<v-icon
				color="blue"
				title="Asociar riesgos"
				v-bind="attrs"
				v-on="on"
				v-on:click="getCrisis"
				>mdi-clipboard-text</v-icon
			>
		</template>

		<v-card>
			<v-card-title class="header-table">
				<v-row justify="space-between" class="pa-2">
					<span class="text-h5"
						>Asociar riesgos al escenario crítico</span
					>
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
					<h2 class="font-weight-medium text-center my-2">
						Riesgos de la organización
					</h2>
					<v-list flat subheader three-line class="my-4">
						<v-list-item-group
							multiple
							v-for="item in risks"
							:key="item.key"
						>
							<v-list-item
								@click="item.selected = !item.selected"
							>
								<v-list-item-action>
									<v-checkbox
										v-model="item.selected"
										:input-value="item.selected"
									></v-checkbox>
								</v-list-item-action>

								<v-list-item-content>
									<v-list-item-title>{{
										item.name
									}}</v-list-item-title>
									<v-list-item-subtitle>{{
										item.description
									}}</v-list-item-subtitle>
								</v-list-item-content>
							</v-list-item>
						</v-list-item-group>
					</v-list>
				</v-container>
			</v-card-text>

			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn color="primary darken-1" @click="dialog = false" text>
					Cerrar
				</v-btn>
				<v-btn color="primary" v-on:click="associateRisks">
					Asociar riesgos
				</v-btn>
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

import AlertError from '../Genericos/AlertError.vue'

interface Risk {
	id: number
	selected: boolean
	name: string
	description: string
}

interface CrisisScenario {
	name: string
	description: string
	_risks: Risk[]
}

export default Vue.extend({
	components: {
		AlertError,
	},

	props: ['id'],
	data() {
		return {
			loading: true,
			formValido: true,
			dialog: false,

			risks: [] as Risk[],
			scenarioRiskIds: [] as number[],
			criticidad: ['Alto', 'Mediano', 'Bajo'],

			//Para el manejo del mensaje
			mensajeError: '',
			snackbar: false,
		}
	},
	methods: {
		associateRisks() {
			this.scenarioRiskIds = []
			for (let i = 0; i < this.risks.length; i++) {
				if (this.risks[i].selected) {
					this.scenarioRiskIds.push(this.risks[i].id)
				}
			}

			//Es necesario que el array de IDs tenga este nombre
			let ids = {
				risks: this.scenarioRiskIds,
			}

			axios
				.patch(
					`${SERVER_ADDRESS}/api/risks/crisis_scenario/${this.$props.id}/`,
					ids,
					{
						withCredentials: true,
						headers: {
							Authorization: TOKEN,
						},
					}
				)
				.then((res) => {
					//Si el escenario crítico fue exitosamente creada, mostramos mensaje de éxito y cerramos el modal
					this.dialog = false

					this.$emit(
						'alertexito',
						'¡Los riesgos fueron asociados al escenario crítico satisfactoriamente!'
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
		async getCrisis() {
			this.scenarioRiskIds = []

			axios
				.get<CrisisScenario>(
					`${SERVER_ADDRESS}/api/risks/crisis_scenario/${this.$props.id}/`,
					{
						withCredentials: true,
						headers: {
							Authorization: TOKEN,
						},
					}
				)
				.then((res) => {
					for (let i = 0; i < res.data._risks.length; i++) {
						this.scenarioRiskIds.push(res.data._risks[i].id)
					}
					this.getRisks()
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
		async getRisks() {
			this.risks = []
			axios
				.get<Risk[]>(`${SERVER_ADDRESS}/api/risks/risks/`, {
					withCredentials: true,
					headers: {
						Authorization: TOKEN,
					},
				})
				.then((res) => {
					for (let i = 0; i < res.data.length; i++) {
						var risk: Risk = {
							id: res.data[i].id,
							name: res.data[i].name,
							description: res.data[i].description,
							selected: false,
						}
						if (this.scenarioRiskIds.includes(res.data[i].id)) {
							risk.selected = true
						} else {
							risk.selected = false
						}
						this.risks.push(risk)
					}

					this.loading = false
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
		seleccionarCheckbox(item: boolean) {
			item = !item
		},
	},
})
</script>

<style></style>