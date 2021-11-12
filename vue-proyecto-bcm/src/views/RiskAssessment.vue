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
					style="height: 150px"
					align="center"
					justify="center"
				>
					<v-col cols="12" sm="8" md="8" lg="8" xl="8">
						<h2 class="font-weight-medium">
							Riesgos de la organización
						</h2>
					</v-col>
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
				</v-row>

				<v-row
					no-gutters
					style="height: 150px"
					align="center"
					justify="center"
				>
					<v-card>
						<v-card-title class="header-table">
							Riesgos
							<v-spacer></v-spacer>
							<v-text-field
								v-model="search"
								append-icon="mdi-magnify"
								label="Buscar por nombre"
								single-line
								hide-details
								dark
								class="header-table"
							></v-text-field>
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
										<v-row style="display: inline-block">
											<modal-detail-risk
												:id="row.item.id"
											></modal-detail-risk>
											<v-icon
												color="yellow"
												title="Editar riesgo"
												>mdi-notebook-edit</v-icon
											>
											<v-icon
												color="red"
												title="Eliminar riesgo"
												>mdi-delete-forever</v-icon
											>
										</v-row>
									</td>
								</tr>
							</template>
						</v-data-table>
					</v-card>
				</v-row>
			</div>
		</v-fade-transition>
		<v-fade-transition>
			<div v-show="expandScenario">
				<v-row
					no-gutters
					style="height: 150px"
					align="center"
					justify="center"
				>
					<v-col cols="12" sm="8" md="8" lg="8" xl="8">
						<h2 class="font-weight-medium">Escenarios críticos</h2>
					</v-col>
					<v-col cols="12" sm="4" md="4" lg="4" xl="4">
						<div class="text-center">
							<div class="my-4">
								<v-btn
									color="secondary"
									style="color: black"
									rounded
								>
									Agregar escenario crítico
								</v-btn>
							</div>
						</div>
					</v-col>
				</v-row>

				<v-row
					no-gutters
					style="height: 150px"
					align="center"
					justify="center"
				>
					<v-card>
						<v-card-title class="header-table">
							Riesgos
							<v-spacer></v-spacer>
							<v-text-field
								v-model="search"
								append-icon="mdi-magnify"
								label="Buscar por nombre"
								single-line
								hide-details
								dark
								class="header-table"
							></v-text-field>
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
									<td style="width: 100px">
										<v-row style="display: inline-block">
											<v-icon
												color="yellow"
												title="Editar riesgo"
												>mdi-notebook-edit</v-icon
											>
											<v-icon
												color="red"
												title="Eliminar riesgo"
												>mdi-delete-forever</v-icon
											>
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
				</v-row>
			</div>
		</v-fade-transition>

		<v-row align="center" no-gutters style="height: 200px"> </v-row>
	</v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import { SERVER_ADDRESS, TOKEN } from '../../config/config'

import ModalCreateRisk from '../components/EvaluacionRiesgos/ModalCreateRisk.vue'
import ModalDetailRisk from '../components/EvaluacionRiesgos/ModalDetailRisk.vue'
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
		ModalDetailRisk,
		ModalAssociateRisks,
	},

	data: () => ({
		search: '',
		headersRisk: [
			{
				text: 'Nombre',
				align: 'start',
				value: 'nombre',
				class: 'header-table',
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
		headersCrisisScenario: [
			{
				text: 'Nombre',
				align: 'start',
				value: 'nombre',
				class: 'header-table',
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
		crisisScenarios: [
			{
				id: 1,
				name: 'Terremoto',
				description:
					'Terremoto entre el grado 4 y 8 de la escala según la escala de Ritcher.',
			},
			{
				id: 2,
				name: 'Apagón nacional de luz',
				description:
					'Ausencia de la energía eléctrica en parte del territorio nacional o en su totalidad.',
			},
		] as CrisisScenario[],

		//Variables para expandir vistas
		expandRisk: true,
		expandScenario: false,

		//Para el manejo del mensaje de éxito
		mensajeExito: '',
		alertaExito: false,
	}),
	mounted() {
		this.getRisks()
	},
	methods: {
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
					console.log(res)
					console.log(res.data)

					this.risks = res.data
				})
				.catch(function (error) {
					console.log('Ups! Ha ocurrido un error en el servidor')
					console.log(error.toJSON())
				})
		},

		alertExito(mensaje: string) {
			this.alertaExito = true
			this.mensajeExito = mensaje
			this.getRisks()
			//this.recargarTabla();
		},
		dismissSuccess() {
			console.log('Cerrar alerta exito padre')
			this.alertaExito = !this.alertaExito
		},
		cambiarVistaRiesgo() {
			if (!this.expandRisk) {
				this.expandScenario = !this.expandScenario
				setTimeout(() => {
					console.log('World!')
					this.expandRisk = !this.expandRisk
				}, 500)
			}
		},
		cambiarVistaEscenario() {
			if (!this.expandScenario) {
				this.expandRisk = !this.expandRisk
				setTimeout(() => {
					this.expandScenario = !this.expandScenario
					console.log('World!')
				}, 500)
			}
		},
	},
})
</script>

<style lang="scss">
</style>