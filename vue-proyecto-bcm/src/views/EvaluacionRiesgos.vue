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

		<alerta-exito
			v-if="alertaExito"
			:mensaje="mensajeExito"
			v-on:dismissexito="dismissExito"
		></alerta-exito>

		<v-fade-transition>
			<div v-show="expandirRiesgo">
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
								<modal-crear-riesgo
									v-on:alertexito="alertExito"
								></modal-crear-riesgo>
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
							:headers="headersRiesgos"
							:items="riesgos"
							:search="search"
							:items-per-page="5"
						>
							<template v-slot:item="row">
								<tr>
									<td>{{ row.item.titulo }}</td>
									<td>{{ row.item.descripcion }}</td>
									<td>{{ row.item.criticidad }}</td>
									<td style="width: 100px">
										<v-row style="display: inline-block">
											<modal-detalle-riesgo
												:id="row.item.id"
											></modal-detalle-riesgo>
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
			<div v-show="expandirEscenario">
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
							:headers="headersEscenarios"
							:items="escenarios"
							:search="search"
							:items-per-page="5"
						>
							<template v-slot:item="row">
								<tr>
									<td>{{ row.item.titulo }}</td>
									<td>{{ row.item.descripcion }}</td>
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
											<modal-asociar-riesgos
												:id="row.item.id"
												v-on:alertexito="alertExito"
											></modal-asociar-riesgos>
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

import ModalCrearRiesgo from '../components/EvaluacionRiesgos/ModalCrearRiesgo.vue'
import ModalDetalleRiesgo from '../components/EvaluacionRiesgos/ModalDetalleRiesgo.vue'
import ModalAsociarRiesgos from '../components/EvaluacionRiesgos/ModalAsociarRiesgos.vue'
import AlertaExito from '../components/Genericos/AlertaExito.vue'

interface Riesgo {
	id: number
	titulo: string
	descripcion: string
	criticidad: string
}

interface Escenario {
	id: number
	titulo: string
	descripcion: string
}

export default Vue.extend({
	//name: 'EvaluacionRiesgos',

	components: {
		AlertaExito,
		ModalCrearRiesgo,
		ModalDetalleRiesgo,
		ModalAsociarRiesgos,
	},

	data: () => ({
		search: '',
		headersRiesgos: [
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
				text: 'Criticidad',
				value: 'criticidad',
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
		headersEscenarios: [
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
		riesgos: [
			{
				id: 1,
				titulo: 'Corte del servicio de energía eléctrica',
				descripcion:
					'Corte repentino de la electricidad en la totalidad de la organización.',
				criticidad: 'Alta',
			},
			{
				id: 2,
				titulo: 'Corte del servicio de internet de Netuno',
				descripcion:
					'Corte del servicio de internet de fibra óptica de Netuno.',
				criticidad: 'Mediana',
			},
			{
				id: 3,
				titulo: 'Corte del servicio de agua',
				descripcion:
					'Corte del servicio del servicio de agua dentro de la organización.',
				criticidad: 'Baja',
			},
		] as Riesgo[],
		escenarios: [
			{
				id: 1,
				titulo: 'Terremoto',
				descripcion:
					'Terremoto entre el grado 4 y 8 de la escala según la escala de Ritcher.',
			},
			{
				id: 2,
				titulo: 'Apagón nacional de luz',
				descripcion:
					'Ausencia de la energía eléctrica en parte del territorio nacional o en su totalidad.',
			},
		] as Escenario[],

		//Variables para expandir vistas
		expandirRiesgo: true,
		expandirEscenario: false,

		//Para el manejo del mensaje de éxito
		mensajeExito: '',
		alertaExito: false,
	}),
	methods: {
		alertExito(mensaje: string) {
			this.alertaExito = true
			this.mensajeExito = mensaje
			//this.recargarTabla();
		},
		dismissExito() {
			console.log('Cerrar alerta exito padre')
			this.alertaExito = !this.alertaExito
		},
		cambiarVistaRiesgo() {
			if (!this.expandirRiesgo) {
				this.expandirEscenario = !this.expandirEscenario
				setTimeout(() => {
					console.log('World!')
					this.expandirRiesgo = !this.expandirRiesgo
				}, 500)
			}
		},
		cambiarVistaEscenario() {
			if (!this.expandirEscenario) {
				this.expandirRiesgo = !this.expandirRiesgo
				setTimeout(() => {
					this.expandirEscenario = !this.expandirEscenario
					console.log('World!')
				}, 500)
			}
		},
	},
})
</script>

<style lang="scss">
</style>