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
							<td>{{ row.item.criticality }}</td>
							<td>{{ row.item.area_name }}</td>
							<td style="width: 100px">
								<v-row justify="center">
									<!--v-icon
												color="yellow"
												title="Editar riesgo"
												>mdi-notebook-edit</v-icon
											-->
									<modal-update-risk
										:id="row.item.id"
										v-on:alertexito="alertExito"
									></modal-update-risk>
									<modal-confirm-delete-risk
										:id="row.item.id"
										v-on:alertexito="alertExito"
									></modal-confirm-delete-risk>
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

import ModalCreateServiceOffered from '../components/ServiciosOfrecidos/ModalCreateServiceOffered.vue'
import ModalUpdateRisk from '../components/EvaluacionRiesgos/ModalUpdateRisk.vue'
import ModalConfirmDeleteRisk from '../components/EvaluacionRiesgos/ModalConfirmDeleteRisk.vue'
import AlertSuccess from '../components/Genericos/AlertSuccess.vue'

interface ServiceOffered {
	id: number
	name: string
	type: number
	type_name: string
	profit: number
	recovery_time: string
	criticality: number
	area: number
	area_name: string
}

export default Vue.extend({
	name: 'ServicesOffered',

	components: {
		AlertSuccess,
		ModalCreateServiceOffered,
		ModalUpdateRisk,
		ModalConfirmDeleteRisk,
	},

	data: () => ({
		search: '',
		headersServices: [
			{
				text: 'Nombre',
				align: 'start',
				value: 'nombre',
				class: 'header-table',
				sortable: true,
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
		deleteServiceId: 0 as number,

		//Para el manejo del mensaje de éxito
		mensajeExito: '',
		alertaExito: false,

		//Para el manejo del mensaje
		mensajeError: '' as string,
		snackbar: false as boolean,
	}),
	mounted() {
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
					this.services = res.data
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