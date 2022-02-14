<template>
	<v-container>
		<alert-success
			v-if="alertaExito"
			:message="mensajeExito"
			v-on:dismisssuccess="dismissSuccess"
		></alert-success>

		<v-row no-gutters style="height: 150px" align="center" justify="center">
			<v-card>
				<v-card-title class="header-table">
					<v-spacer></v-spacer>
					<v-col cols="12" sm="6" md="6" lg="6" xl="6">
						<div class="text-center">
							<div class="my-4">
								<modal-create-service-offered
									:scale_id="scaleView.id"
									:minValue="scaleView.scale_min_value"
									:maxValue="scaleView.scale_max_value"
									:scaleName="scaleView.scale_name"
									v-on:alertexito="alertExito"
								></modal-create-service-offered>
							</div>
						</div>
					</v-col>
					<v-col cols="12" sm="6" md="6" lg="6" xl="6">
						<v-text-field
							v-model="search"
							append-icon="mdi-magnify"
							label="Buscar por nombre"
							single-line
							hide-details
							dark
							class="header-table"
						></v-text-field>
					</v-col>
				</v-card-title>
				<v-data-table
					:headers="headersServices"
					:items="services"
					:search="search"
					:items-per-page="5"
				>
					<template v-slot:item="row">
						<tr>
							<td>{{ row.item.name }}</td>
							<td>{{ row.item.type_name }}</td>
							<td>{{ row.item.profit }}</td>
							<td>{{ row.item.recovery_time }}</td>
							<td v-if="!row.item.scale_max_value">
								{{ row.item.criticality }}
							</td>
							<td v-if="row.item.scale_max_value">
								{{ row.item.criticality }}/{{
									row.item.scale_max_value
								}}
							</td>
							<td>{{ row.item.area_name }}</td>
							<td style="width: 110px">
								<v-row justify="center">
									<modal-update-service-offered
										:id="row.item.id"
										:scale_id="scaleView.id"
										:minValue="scaleView.scale_min_value"
										:maxValue="scaleView.scale_max_value"
										:scaleName="scaleView.scale_name"
										v-on:alertexito="alertExito"
									></modal-update-service-offered>
									<modal-confirm-delete-service-offered
										:id="row.item.id"
										:type="row.item.type_name"
										v-on:alertexito="alertExito"
									></modal-confirm-delete-service-offered>
								</v-row>
							</td>
						</tr>
					</template>
				</v-data-table>
			</v-card>
		</v-row>

		<v-row align="center" no-gutters style="height: 300px"> </v-row>
	</v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import { SERVER_ADDRESS, TOKEN } from '../../config/config'

import ModalCreateServiceOffered from '../components/ServicesOffered/ModalCreateServiceOffered.vue'
import ModalUpdateServiceOffered from '../components/ServicesOffered/ModalUpdateServiceOffered.vue'
import ModalConfirmDeleteServiceOffered from '../components/ServicesOffered/ModalConfirmDeleteServiceOffered.vue'
import AlertSuccess from '../components/Genericos/AlertSuccess.vue'

import { getRecoveryTimeText } from '../helpers/helpers'

interface ServiceOffered {
	id: number
	name: string
	type: number
	type_name: string
	profit: number
	recovery_time: string
	criticality: number
	area_name: string
	scale_max_value: number
}

interface ScaleView {
	id: number
	name: string
	scale: number
	scale_name: string
	scale_min_value: number
	scale_max_value: number
}

export default Vue.extend({
	name: 'ServicesOffered',

	components: {
		AlertSuccess,
		ModalCreateServiceOffered,
		ModalUpdateServiceOffered,
		ModalConfirmDeleteServiceOffered,
	},

	data: () => ({
		search: '',
		headersServices: [
			{
				text: 'Nombre',
				value: 'nombre',
				class: 'header-table',
				filterable: true,
			},
			{
				text: 'Tipo',
				value: 'type_name',
				class: 'header-table',
				filterable: true,
			},
			{
				text: 'Ganancia',
				value: 'profit',
				class: 'header-table',
				filterable: true,
			},
			{
				text: 'Tiempo de recuperación (estimado)',
				value: 'recovery_time',
				class: 'header-table',
				filterable: true,
			},
			{
				text: 'Criticidad',
				value: 'criticality',
				class: 'header-table',
				filterable: true,
			},
			{
				text: 'Area',
				value: 'area_name',
				class: 'header-table',
				filterable: true,
			},
			{
				text: 'Acciones',
				value: 'acciones',
				class: 'header-table',
				align: 'center',
				disableSort: true,
				disableFiltering: true,
			},
		],
		services: [] as ServiceOffered[],
		scaleView: {
			id: 0,
			name: '',
			scale: 0,
			scale_name: '',
			scale_min_value: 0,
			scale_max_value: 0,
		} as ScaleView,

		//Para el manejo del mensaje de éxito
		mensajeExito: '',
		alertaExito: false,

		//Para el manejo del mensaje
		mensajeError: '' as string,
		snackbar: false as boolean,
	}),
	mounted() {
		this.getScaleView()
		this.getServicesOffered()
	},
	methods: {
		async getServicesOffered() {
			this.services = []
			axios
				.get<ServiceOffered[]>(
					`${SERVER_ADDRESS}/api/phase2/services/offered/`,
					{
						withCredentials: true,
						headers: {
							Authorization: TOKEN,
						},
					}
				)
				.then((res) => {
					for (var i = 0; i < res.data.length; i++) {
						//Convertimos en texto la duración
						res.data[i].recovery_time = getRecoveryTimeText(
							res.data[i].recovery_time
						)

						this.services.push(res.data[i])
					}
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
		async getScaleView() {
			this.services = []
			axios
				.get<ScaleView[]>(`${SERVER_ADDRESS}/api/config/scales/view/`, {
					params: { name: 'Servicios Ofrecidos' },
					withCredentials: true,
					headers: {
						Authorization: TOKEN,
					},
				})
				.then((res) => {
					this.scaleView = res.data[0]
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

		alertExito(mensaje: string) {
			this.alertaExito = true
			this.mensajeExito = mensaje
			this.getServicesOffered()
		},
		dismissSuccess() {
			this.alertaExito = !this.alertaExito
		},
	},
})
</script>

<style lang="scss">
</style>