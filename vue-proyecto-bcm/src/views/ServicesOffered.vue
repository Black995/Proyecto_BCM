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
					<v-col cols="12" sm="4" md="4" lg="4" xl="4">
						<div class="text-center">
							<div class="my-4">
								<!--Llamamos al componente de crear riesgo-->
								<modal-create-risk
									v-on:alertexito="alertExito"
								></modal-create-risk>
							</div>
						</div>
					</v-col>
					<v-col cols="12" sm="8" md="8" lg="8" xl="8">
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
					:headers="headersRisk"
					:items="risks"
					:search="search"
					:items-per-page="5"
				>
					<template v-slot:item="row">
						<tr>
							<td>{{ row.item.name }}</td>
							<td>{{ row.item.description }}</td>
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

import ModalCreateRisk from '../components/EvaluacionRiesgos/ModalCreateRisk.vue'
import ModalUpdateRisk from '../components/EvaluacionRiesgos/ModalUpdateRisk.vue'
import ModalConfirmDeleteRisk from '../components/EvaluacionRiesgos/ModalConfirmDeleteRisk.vue'
import AlertSuccess from '../components/Genericos/AlertSuccess.vue'

interface Risk {
	id: number
	name: string
	description: string
}

interface CrisisScenario {
	id: number
	name: string
	description: string
}

export default Vue.extend({
	name: 'ServicesOffered',

	components: {
		AlertSuccess,
		ModalCreateRisk,
		ModalUpdateRisk,
		ModalConfirmDeleteRisk,
	},

	data: () => ({
		search: '',
		headersRisk: [
			{
				text: 'Nombre',
				align: 'start',
				value: 'nombre',
				class: 'header-table',
				sortable: true,
				filterable: true,
			},
			{
				text: 'Descripción',
				value: 'descripcion',
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
		risks: [] as Risk[],
		deleteRiskId: 0 as number,

		//Para el manejo del mensaje de éxito
		mensajeExito: '',
		alertaExito: false,

		//Para el manejo del mensaje
		mensajeError: '' as string,
		snackbar: false as boolean,
	}),
	mounted() {
		this.getRisks()
	},
	methods: {
		async getRisks() {
			this.risks = []
			axios
				.get<Risk[]>(`${SERVER_ADDRESS}/api/phase1/risks/`, {
					withCredentials: true,
					headers: {
						Authorization: TOKEN,
					},
				})
				.then((res) => {
					this.risks = res.data
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
			this.getRisks()
		},
		dismissSuccess() {
			this.alertaExito = !this.alertaExito
		},
	},
})
</script>

<style lang="scss">
</style>