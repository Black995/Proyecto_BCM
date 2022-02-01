<template>
	<v-container>
		<alert-exito
			v-if="alertaExito"
			:mensaje="mensajeExito"
			v-on:dismissexito="dismissExito"
		></alert-exito>

		<v-row no-gutters style="height: 150px" align="center" justify="center">
			<v-card>
				<v-card-title class="header-table">
							<v-spacer></v-spacer>
							<v-col cols="12" sm="4" md="4" lg="4" xl="4">
								<div class="text-center">
									<div class="my-4">
										<!--Llamamos al componente de crear riesgo-->
										<modal-create-activity
											v-on:alertexito="alertExito"
										></modal-create-activity>
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
					:headers="headers"
					:items="actividades"
					:search="search"
					:items-per-page="5"
				>
					<template v-slot:item="row">
						<tr>
							<td style="width: 200px">{{ row.item.nombre }}</td>
							<td style="width: 200px">
								{{ row.item.descripcion }}
							</td>
							<td style="width: 200px">{{ row.item.costo }}</td>
							<td style="width: 200px">
								{{ row.item.frecuencia }}
							</td>
							<td style="width: 200px">
								{{ row.item.criticidad }}
							</td>
							<td style="width: 200px">
								{{ row.item.tiempo_recuperacion }}
							</td>
							<td style="width: 100px">
								<v-row style="display: inline-block">
									<modal-detalle-riesgo
										:uuid="row.item.id"
									></modal-detalle-riesgo>
									<v-icon color="yellow" title="Editar parte"
										>mdi-notebook-edit</v-icon
									>
									<modal-confirm-delete
										:id="row.item.id"
										v-on:alertexito="alertExito"
									></modal-confirm-delete>
								</v-row>
							</td>
						</tr>
					</template>
				</v-data-table>
			</v-card>
		</v-row>

		<v-row align="center" no-gutters style="height: 350px"> </v-row>
	</v-container>
</template>


<script lang="ts">
import Vue from 'vue'

import ModalCreateActivity from '../components/ActividadesOrganizacion/ModalCreateActivity.vue'
import ModalConfirmDelete from '../components/ActividadesOrganizacion/ModalConfirmDelete.vue'
import AlertExito from '../components/Genericos/AlertSuccess.vue'

interface Actividad {
	id: number
	nombre: string
	descripcion: string
	costo: string
	frecuencia: string
	criticidad: string
	tiempo_recuperacion: string
}
export default Vue.extend({
	//name: 'ActividadesNegocio',

	components: {
		AlertExito,
		ModalCreateActivity,
		ModalConfirmDelete,
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
				text: 'Costo',
				value: 'Costo',
				class: 'header-table',
				filterable: false,
			},
			{
				text: 'Frecuencia',
				value: 'Frecuencia',
				class: 'header-table',
				filterable: false,
			},
			{
				text: 'Criticidad',
				value: 'Criticidad',
				class: 'header-table',
				filterable: false,
			},
			{
				text: 'Tiempo de Recuperación',
				value: 'Criticidad',
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
		actividades: [
			{
				id: 1,
				nombre: 'Compra de materiales',
				descripcion: 'Compra de materiales',
				costo: '100',
				frecuencia: 'Semanal',
				criticidad: '3',
				tiempo_recuperacion: '1 semana',
			},
			{
				id: 2,
				nombre: 'Compra de materiales',
				descripcion: 'Compra de materiales',
				costo: '100',
				frecuencia: 'Semanal',
				criticidad: '3',
				tiempo_recuperacion: '1 semana',
			},
			{
				id: 3,
				nombre: 'Compra de materiales',
				descripcion: 'Compra de materiales',
				costo: '100',
				frecuencia: 'Semanal',
				criticidad: '3',
				tiempo_recuperacion: '1 semana',
			},
		] as Actividad[],

		//Para el manejo del mensaje de éxito
		mensajeExito: '',
		alertaExito: false,
	}),
	/*methods: {
		alertExito(mensaje: string) {
			this.alertaExito = true
			this.mensajeExito = mensaje
			//this.recargarTabla();
		},
		dismissExito() {
			console.log('Cerrar alerta exito padre')
			this.alertaExito = !this.alertaExito
		},
	},*/
})
</script>


<style lang="scss">
</style>