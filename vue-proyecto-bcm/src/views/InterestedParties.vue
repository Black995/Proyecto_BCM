<template>
	<v-container>
		<alert-success
			v-if="alertaExito"
			:mensaje="mensajeExito"
			v-on:dismissexito="dismissExito"
		></alert-success>

		<v-row no-gutters style="height: 150px" align="center" justify="center">
			<v-card>
				<v-card-title class="header-table">
							<v-spacer></v-spacer>
							<v-col cols="12" sm="4" md="4" lg="4" xl="4">
								<div class="text-center">
									<div class="my-4">
										<!--Llamamos al componente de crear riesgo-->
										<modal-create-parties
											v-on:alertexito="alertExito"
										></modal-create-parties>
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
					:items="partes"
					:search="search"
					:items-per-page="5"
				>
					<template v-slot:item="row">
						<tr>
							<td style="width: 300px">{{ row.item.nombre }}</td>
							<td style="width: 300px">
								{{ row.item.descripcion }}
							</td>
							<td style="width: 300px">{{ row.item.tipo }}</td>
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

import ModalCreateParties from '../components/PartesInteresadas/ModalCreateParties.vue'
import ModalConfirmDelete from '../components/PartesInteresadas/ModalConfirmDelete.vue'
import AlertSuccess from '../components/Genericos/AlertSuccess.vue'

interface parteInteresada {
	id: number
	nombre: string
	descripcion: string
	tipo: string
}

export default Vue.extend({
	//name: 'PartesInteresadas',

	components: {
		AlertSuccess,
		ModalCreateParties,
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
				text: 'Tipo',
				value: 'tipo',
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
		partes: [
			{
				id: 1,
				nombre: 'Parte interesada 1',
				descripcion: 'Parte interesada 1',
				tipo: 'AAA',
			},
			{
				id: 2,
				nombre: 'Parte interesada 2',
				descripcion: 'Parte interesada 2',
				tipo: 'AAA',
			},
			{
				id: 2,
				nombre: 'Parte interesada 2',
				descripcion: 'Parte interesada 2',
				tipo: 'AAA',
			},
		] as parteInteresada[],

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
