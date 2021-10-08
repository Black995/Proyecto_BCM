<template>
	<v-container>
		<alerta-exito
			v-if="alertaExito"
			:mensaje="mensajeExito"
			v-on:dismissexito="dismissExito"
		></alerta-exito>

		<v-row no-gutters style="height: 150px" align="center" justify="center">
			<v-col cols="12" sm="8" md="8" lg="8" xl="8">
				<h2 class="font-weight-medium">Evaluación de Riesgos</h2>
			</v-col>
			<v-col cols="12" sm="4" md="4" lg="4" xl="4">
				<div class="text-center">
					<div class="my-4">
						<!--Llamamos al componente de crear riesgo-->
						<modal-crear-riesgo
							v-on:alertexito="alertExito"
						></modal-crear-riesgo>
					</div>
					<div class="my-4">
						<v-btn color="primary" style="color: black" rounded>
							Asociar escenarios críticos
						</v-btn>
					</div>
				</div>
			</v-col>
		</v-row>

		<v-row no-gutters style="height: 150px" align="center" justify="center">
			<v-card>
				<v-card-title class="header-table">
					Riesgos
					<v-spacer></v-spacer>
					<v-text-field
						v-model="search"
						append-icon="mdi-magnify"
						label="Buscar por nombre o porcentaje"
						single-line
						hide-details
						dark
						class="header-table"
					></v-text-field>
				</v-card-title>
				<v-data-table
					:headers="headers"
					:items="riesgos"
					:search="search"
					:items-per-page="5"
				>
					<template v-slot:item="row">
						<tr>
							<td>{{ row.item.titulo }}</td>
							<td>{{ row.item.descripcion }}</td>
							<td>{{ row.item.criticidad }}</td>
							<td>{{ row.item.porcentaje }}%</td>
							<td style="width: 100px">
								<v-row style="display: inline-block">
									<modal-detalle-riesgo
										:uuid="row.item.id"
									></modal-detalle-riesgo>
									<v-icon color="yellow" title="Editar riesgo"
										>mdi-notebook-edit</v-icon
									>
									<v-icon color="red" title="Eliminar riesgo"
										>mdi-delete-forever</v-icon
									>
								</v-row>
							</td>
						</tr>
					</template>
				</v-data-table>
			</v-card>
		</v-row>

		<v-row align="center" no-gutters style="height: 200px"> </v-row>
	</v-container>
</template>

<script lang="ts">
import Vue from 'vue'

import ModalCrearRiesgo from '../components/EvaluacionRiesgos/ModalCrearRiesgo.vue'
import ModalDetalleRiesgo from '../components/EvaluacionRiesgos/ModalDetalleRiesgo.vue'
import AlertaExito from '../components/Genericos/AlertaExito.vue'

interface Riesgo {
	id: number
	titulo: string
	descripcion: string
	criticidad: string
	porcentaje: number
}

export default Vue.extend({
	//name: 'EvaluacionRiesgos',

	components: {
		AlertaExito,
		ModalCrearRiesgo,
		ModalDetalleRiesgo,
	},

	data: () => ({
		search: '',
		headers: [
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
				text: 'Porcentaje de ocurrencia',
				value: 'ocurrencia',
				class: 'header-table',
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
				porcentaje: 15,
			},
			{
				id: 2,
				titulo: 'Corte del servicio de internet de Netuno',
				descripcion:
					'Corte del servicio de internet de fibra óptica de Netuno.',
				criticidad: 'Mediana',
				porcentaje: 5,
			},
			{
				id: 3,
				titulo: 'Corte del servicio de agua',
				descripcion:
					'Corte del servicio del servicio de agua dentro de la organización.',
				criticidad: 'Baja',
				porcentaje: 30,
			},
		] as Riesgo[],

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
	},
})
</script>


<style lang="scss">
</style>