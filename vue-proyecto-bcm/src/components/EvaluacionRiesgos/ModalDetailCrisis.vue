<template>
	<v-dialog v-model="dialog">
		<template v-slot:activator="{ on, attrs }">
			<v-icon
				color="secondary"
				style="color: black"
				title="Detalle del riesgo"
				v-bind="attrs"
				v-on="on"
				v-on:click="getDetail"
				>mdi-magnify
			</v-icon>
		</template>

		<v-card>
			<v-card-title class="header-table">
				<v-row justify="space-between" class="pa-2">
					<span class="text-h5">Detalle del riesgo</span>
					<v-btn icon @click="dialog = false">
						<v-icon color="white">mdi-close</v-icon>
					</v-btn></v-row
				>
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
					<v-list three-line subheader>
						<v-list-item>
							<v-list-item-content>
								<v-list-item-title
									><h2>
										{{ crisis.name }}
									</h2></v-list-item-title
								>
							</v-list-item-content>
						</v-list-item>
						<v-row>
							<v-list-item>
								<v-list-item-content>
									<v-list-item-title
										><strong
											>Descripción</strong
										></v-list-item-title
									>
									<v-list-item-title>{{
										crisis.description
									}}</v-list-item-title>
								</v-list-item-content>
							</v-list-item>
						</v-row>
					</v-list>

					<v-divider></v-divider>

					<h2 class="text-center my-5">
						Riesgos del escenario crítico
					</h2>

					<v-list flat subheader three-line class="my-4">
						<v-list-item
							v-for="item in crisis._risks"
							:key="item.key"
						>
							<v-list-item-content>
								<v-list-item-title>{{
									item.name
								}}</v-list-item-title>
								<v-list-item-subtitle>{{
									item.description
								}}</v-list-item-subtitle>
							</v-list-item-content>
						</v-list-item>
					</v-list>
				</v-container>
			</v-card-text>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn color="primary darken-1" text @click="dialog = false">
					Cerrar
				</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import { SERVER_ADDRESS, TOKEN } from '../../../config/config'

interface Risk {
	id: number
	name: string
	description: string
}

interface CrisisScenario {
	name: string
	description: string
	_risks: Risk[]
}

export default Vue.extend({
	props: ['id'],
	data() {
		return {
			loading: true,
			crisis: {} as CrisisScenario,
			dialog: false,

			//Para el manejo del mensaje
			mensajeError: '' as string,
			snackbar: false as boolean,
		}
	},
	methods: {
		getDetail() {
			console.log('[ID del escenario crítico detalle] ', this.$props.id)

			axios
				.get<CrisisScenario>(
					`${SERVER_ADDRESS}/api/phase1/crisis_scenario/${this.$props.id}/`,
					{
						withCredentials: true,
						headers: {
							Authorization: TOKEN,
						},
					}
				)
				.then((res) => {
					this.loading = false
					this.crisis = res.data
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
	},
})
</script>

<style></style>