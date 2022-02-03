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
				Agregar producto/servicio ofrecido
			</v-btn>
		</template>

		<v-card>
			<v-form ref="form" v-model="validForm" lazy-validation>
				<v-card-title class="header-table">
					<v-row justify="space-between" class="pa-1">
						<span class="text-h5"
							>Crear nuevo producto/servicio ofrecido</span
						>
						<v-btn icon @click="dialog = false">
							<v-icon color="white">mdi-close</v-icon>
						</v-btn>
					</v-row>
				</v-card-title>
				<v-divider></v-divider>
				<v-card-text>
					<v-container>
						<v-text-field
							v-model="service.name"
							:counter="50"
							:rules="rules.name"
							label="Ingrese el título del producto/servicio"
						></v-text-field>
						<v-row>
							<v-col cols="12" sm="6" md="6" lg="6" xl="6">
								<v-select
									v-model="service.type"
									:items="types"
									item-text="name"
									item-value="value"
									:rules="rules.type"
									label="Tipo"
									required
								></v-select>
							</v-col>
							<v-col cols="12" sm="6" md="6" lg="6" xl="6">
								<v-text-field
									v-model="service.profit"
									:rules="rules.profit"
									label="Ingrese la ganancia"
									prefix="$"
									type="number"
									required
								></v-text-field>
							</v-col>
						</v-row>
						<v-row>
							<v-card-text>
								<v-slider
									v-model="service.criticality"
									label="Criticidad"
									step="1"
									ticks="always"
									thumb-label="always"
									tick-size="3"
									min="0"
									max="9"
								></v-slider>
							</v-card-text>
						</v-row>
						<v-row align="center">
							<v-col cols="12" sm="6" md="6" lg="6" xl="6">
								<v-select
									v-model="service.area"
									:items="areas"
									item-text="name"
									item-value="id"
									:rules="rules.area"
									label="Area de la organización"
									required
								></v-select>
							</v-col>
							<v-col cols="12" sm="6" md="6" lg="6" xl="6">
								<v-subheader>
									Tiempo de recuperación
								</v-subheader>
								<v-row>
									<v-col cols="3" sm="4" md="4" lg="4" xl="4">
										<v-text-field
											v-model="duration.days"
											:rules="rules.type"
											label="Días"
											type="number"
											required
										></v-text-field>
									</v-col>
									<v-col cols="3" sm="4" md="4" lg="4" xl="4">
										<v-select
											v-model="duration.hours"
											:items="hours"
											label="Horas"
											required
										></v-select>
									</v-col>
									<v-col cols="3" sm="4" md="4" lg="4" xl="4">
										<v-select
											v-model="duration.minutes"
											:items="minutes"
											label="Minutos"
											required
										></v-select>
									</v-col>
								</v-row>
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
					<modal-confirm-create-service-offered
						:disabled="validForm"
						v-on:crear="Crear"
					></modal-confirm-create-service-offered>
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

import ModalConfirmCreateServiceOffered from './ModalConfirmCreateServiceOffered.vue'
import AlertError from '../Genericos/AlertError.vue'

interface ServiceOffered {
	name: string
	type: number
	profit: number
	recovery_time: string
	criticality: number
	area: number
}

interface TypeOption {
	value: number
	name: string
}

interface Area {
	id: number
	name: string
}

interface Duration {
	days: number
	hours: number
	minutes: number
}

function getRecoveryTime(duration: Duration) {
	let day = ''
	let hour = ''
	let minute = ''

	if (duration.days <= 9) day = '0' + duration.days.toString()
	else day = duration.days.toString()

	if (duration.hours <= 9) hour = '0' + duration.hours.toString()
	else hour = duration.hours.toString()

	if (duration.minutes <= 9) minute = '0' + duration.minutes.toString()
	else minute = duration.minutes.toString()

	return day + ':' + hour + ':' + minute
}

export default Vue.extend({
	components: {
		AlertError,
		ModalConfirmCreateServiceOffered,
	},

	data() {
		return {
			loading: true,
			validForm: false,
			dialog: false,

			service: {
				name: '',
				type: 0,
				profit: 0,
				recovery_time: '',
				criticality: 0,
				area: 0,
			} as ServiceOffered,
			duration: {
				days: 0,
				hours: 0,
				minutes: 0,
			} as Duration,
			hours: [
				0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
				18, 19, 20, 21, 22, 23,
			] as number[],
			minutes: [0, 15, 30, 45] as number[],
			areas: [] as Area[],
			types: [
				{
					value: 1,
					name: 'Producto',
				},
				{
					value: 2,
					name: 'Servicio',
				},
			] as TypeOption[],
			//Para el manejo del mensaje
			mensajeError: '' as string,
			snackbar: false as boolean,

			rules: {
				name: [
					(v: any) => !!v || 'Este campo es obligatorio',
					(v: any) =>
						(v && v.length <= 50) ||
						'El nombre debe contener como máximo 50 caracteres',
				],
				type: [(v: any) => !!v || 'Este campo es obligatorio'],
				profit: [
					(v: any) =>
						v === null ||
						typeof v !== 'number' ||
						'Este campo debe ser un numérico',
					(v: any) =>
						v === null ||
						v >= 0 ||
						'La ganancia debe ser mayor o igual a 0',
				],
				area: [(v: any) => !!v || 'Este campo es obligatorio'],
				recovery_time: [(v: any) => !!v || 'Este campo es obligatorio'],
			},
		}
	},
	mounted() {
		this.getAreas()
	},
	methods: {
		async Crear() {
			//Validación de los inputs
			if (
				!(
					this.$refs.form as Vue & { validate: () => boolean }
				).validate()
			)
				return

			this.service.recovery_time = getRecoveryTime(this.duration)

			axios
				.post(
					`${SERVER_ADDRESS}/api/phase2/services/offered/`,
					this.service,
					{
						withCredentials: true,
						headers: {
							Authorization: TOKEN,
						},
					}
				)
				.then((res) => {
					this.loading = false
					this.dialog = false

					let successType = ''
					if (this.service.type == 1) successType = 'producto'
					else successType = 'servicio'

					//Reinicializamos variable del crear
					this.service = {
						name: '',
						type: 0,
						profit: 0,
						recovery_time: '',
						criticality: 0,
						area: 0,
					}
					this.duration = {
						days: 0,
						hours: 0,
						minutes: 0,
					}

					this.$emit(
						'alertexito',
						'¡El ' +
							successType +
							' ha sido creado satisfactoriamente!'
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
		async getAreas() {
			this.areas = []
			axios
				.get<Area[]>(`${SERVER_ADDRESS}/api/config/areas/`, {
					withCredentials: true,
					headers: {
						Authorization: TOKEN,
					},
				})
				.then((res) => {
					this.areas = res.data
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