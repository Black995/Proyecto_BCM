<template>
	<v-dialog v-model="dialog">
		<template v-slot:activator="{ on, attrs }">
			<v-icon
				color="secondary"
				style="color: black"
				title="Detalle del riesgo"
				v-bind="attrs"
				v-on="on"
				v-on:click="obtenerDetalle"
				>mdi-magnify
			</v-icon>
		</template>

		<v-card>
			<v-card-title class="header-table">
				<v-row justify="space-between" class="pa-2">
					<span class="text-h5">Detalle del riesgo</span>
					<v-btn icon @click="dialog = false">
						<v-icon color="white">mdi-close</v-icon>
					</v-btn></v-row
				>
			</v-card-title>
			<v-divider></v-divider>
			<v-card-text>
				<v-container>
					<v-row v-show="estaCargando">
						<v-progress-linear
							indeterminate
							color="primary"
						></v-progress-linear
					></v-row>
					<v-list three-line subheader>
						<v-list-item>
							<v-list-item-content>
								<v-list-item-title
									><h2>
										{{ riesgo.titulo }}
									</h2></v-list-item-title
								>
							</v-list-item-content>
						</v-list-item>
						<v-row>
							<v-col cols="6" sm="6" md="6" lg="6" xl="6">
								<v-list-item>
									<v-list-item-content>
										<v-list-item-title
											><strong
												>Criticidad</strong
											></v-list-item-title
										>
										<v-list-item-title>{{
											riesgo.criticidad
										}}</v-list-item-title>
									</v-list-item-content>
								</v-list-item>
							</v-col>
							<v-col cols="6" sm="6" md="6" lg="6" xl="6">
								<v-list-item>
									<v-list-item-content>
										<v-list-item-title
											><strong
												>Porcentaje</strong
											></v-list-item-title
										>
										<v-list-item-title
											>{{
												riesgo.porcentaje
											}}%</v-list-item-title
										>
									</v-list-item-content>
								</v-list-item>
							</v-col>
						</v-row>
						<v-row>
							<v-list-item>
								<v-list-item-content>
									<v-list-item-title
										><strong
											>Descripción</strong
										></v-list-item-title
									>
									<v-list-item-title>{{
										riesgo.descripcion
									}}</v-list-item-title>
								</v-list-item-content>
							</v-list-item>
						</v-row>
					</v-list>
				</v-container>
			</v-card-text>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn color="primary darken-1" text @click="dialog = false">
					Cerrar
				</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'

interface Riesgo {
	titulo: string
	descripcion: string
	criticidad: string
	porcentaje: number
}

export default Vue.extend({
	props: ['id'],
	data() {
		return {
			estaCargando: true,
			riesgo: {} as Riesgo,
			dialog: false,
		}
	},
	methods: {
		obtenerDetalle() {
			console.log('[ID del riesgo detalle] ', this.$props.id)

			this.estaCargando = false

			this.riesgo = {
				titulo: 'Fallo de la electricidad',
				descripcion:
					'Fallo parcial o general del servicio eléctrico en la organización',
				criticidad: 'Alto',
				porcentaje: 25,
			}
		},
	},
})
</script>

<style></style>