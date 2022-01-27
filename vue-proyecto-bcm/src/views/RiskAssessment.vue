<template>
	<v-container>
		<v-app-bar color="#002060" dark>
			<v-tabs align-with-title fixed-tabs>
				<v-tab @click="cambiarVistaRiesgo">Evaluación de riesgos</v-tab>
				<v-tab @click="cambiarVistaEscenario"
					>Escenarios críticos</v-tab
				>
			</v-tabs>
		</v-app-bar>

		<alert-success
			v-if="alertaExito"
			:message="mensajeExito"
			v-on:dismisssuccess="dismissSuccess"
		></alert-success>

		<v-fade-transition>
			<div v-show="expandRisk">
				<v-row
					no-gutters
					style="height: 25px"
					align="center"
					justify="center"
				>
				</v-row>

				<v-layout child-flex>
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
				</v-layout>
			</div>
		</v-fade-transition>
		<v-fade-transition>
			<div v-show="expandScenario">
				<v-row
					no-gutters
					style="height: 25px"
					align="center"
					justify="center"
				></v-row>

				<v-layout child-flex>
					<v-card>
						<v-card-title class="header-table">
							<v-spacer></v-spacer>
							<v-col cols="12" sm="4" md="4" lg="4" xl="4">
								<div class="text-center">
									<div class="my-4">
										<modal-create-crisis
											v-on:alertexito="alertExito"
										></modal-create-crisis>
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
							:headers="headersCrisisScenario"
							:items="crisisScenarios"
							:search="search"
							:items-per-page="5"
						>
							<template v-slot:item="row">
								<tr>
									<td>{{ row.item.name }}</td>
									<td>{{ row.item.description }}</td>
									<td style="width: 120px">
										<v-row style="display: inline-block">
											<modal-detail-crisis
												:id="row.item.id"
											></modal-detail-crisis>
											<modal-update-crisis
												:id="row.item.id"
												v-on:alertexito="alertExito"
											></modal-update-crisis>
											<modal-confirm-delete-crisis
												:id="row.item.id"
												v-on:alertexito="alertExito"
											></modal-confirm-delete-crisis>
											<!--Llamamos al componente de asociar riesgos-->
											<modal-associate-risks
												:id="row.item.id"
												v-on:alertexito="alertExito"
											></modal-associate-risks>
										</v-row>
									</td>
								</tr>
							</template>
						</v-data-table>
					</v-card>
				</v-layout>
			</div>
		</v-fade-transition>

		<v-row align="center" no-gutters style="height: 100px"> </v-row>
	</v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import { SERVER_ADDRESS, TOKEN } from '../../config/config'

import ModalCreateRisk from '../components/EvaluacionRiesgos/ModalCreateRisk.vue'
import ModalCreateCrisis from '../components/EvaluacionRiesgos/ModalCreateCrisis.vue'
import ModalUpdateRisk from '../components/EvaluacionRiesgos/ModalUpdateRisk.vue'
import ModalUpdateCrisis from '../components/EvaluacionRiesgos/ModalUpdateCrisis.vue'
import ModalDetailCrisis from '../components/EvaluacionRiesgos/ModalDetailCrisis.vue'
import ModalConfirmDeleteRisk from '../components/EvaluacionRiesgos/ModalConfirmDeleteRisk.vue'
import ModalConfirmDeleteCrisis from '../components/EvaluacionRiesgos/ModalConfirmDeleteCrisis.vue'
import ModalAssociateRisks from '../components/EvaluacionRiesgos/ModalAssociateRisks.vue'
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
	name: 'RiskAssessment',

	components: {
		AlertSuccess,
		ModalCreateRisk,
		ModalCreateCrisis,
		ModalUpdateRisk,
		ModalUpdateCrisis,
		ModalDetailCrisis,
		ModalAssociateRisks,
		ModalConfirmDeleteRisk,
		ModalConfirmDeleteCrisis,
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
		headersCrisisScenario: [
			{
				text: 'Nombre',
				align: 'start',
				value: 'nombre',
				class: 'header-table',
				sortable: true,
			},
			{
				text: 'Descripción',
				value: 'descripcion',
				class: 'header-table',
				filterable: false,
			},
			{
				text: 'Acciones',
				value: 'acciones',
				class: 'header-table',
				align: 'center',
				filterable: false,
				disableSort: true,
				disableFiltering: true,
			},
		],
		risks: [] as Risk[],
		crisisScenarios: [] as CrisisScenario[],
		deleteRiskId: 0 as number,

		//Variables para expandir vistas
		expandRisk: true,
		expandScenario: false,

		//Para el manejo del mensaje de éxito
		mensajeExito: '',
		alertaExito: false,

		//Para el manejo del mensaje
		mensajeError: '' as string,
		snackbar: false as boolean,
	}),
	mounted() {
		this.getRisks()
		this.getCrisisScenarios()
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

		async getCrisisScenarios() {
			this.crisisScenarios = []
			axios
				.get<CrisisScenario[]>(
					`${SERVER_ADDRESS}/api/phase1/crisis_scenarios_list/`,
					{
						withCredentials: true,
						headers: {
							Authorization: TOKEN,
						},
					}
				)
				.then((res) => {
					this.crisisScenarios = res.data
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
			this.getCrisisScenarios()
		},
		dismissSuccess() {
			this.alertaExito = !this.alertaExito
		},
		cambiarVistaRiesgo() {
			if (!this.expandRisk) {
				this.expandScenario = !this.expandScenario
				setTimeout(() => {
					this.expandRisk = !this.expandRisk
				}, 500)
			}
		},
		cambiarVistaEscenario() {
			if (!this.expandScenario) {
				this.expandRisk = !this.expandRisk
				setTimeout(() => {
					this.expandScenario = !this.expandScenario
				}, 500)
			}
		},
	},
})
</script>

<style lang="scss">
</style>