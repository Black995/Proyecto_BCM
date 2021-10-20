<template>
	<v-dialog v-model="dialog">
		<template v-slot:activator="{ on, attrs }">
			<v-icon
				color="blue"
				title="Asociar riesgos"
				v-bind="attrs"
				v-on="on"
				v-on:click="obtenerRiesgos"
				>mdi-clipboard-text</v-icon
			>
		</template>

		<v-card>
			<v-card-title class="header-table">
				<v-row justify="space-between" class="pa-2">
					<span class="text-h5"
						>Asociar riesgos al escenario crítico</span
					>
					<v-btn icon @click="dialog = false">
						<v-icon color="white">mdi-close</v-icon>
					</v-btn>
				</v-row>
			</v-card-title>
			<v-divider></v-divider>
			<v-card-text>
				<v-container>
					<h2 class="font-weight-medium text-center my-2">
						Riesgos de la organización
					</h2>
					<v-list flat subheader three-line class="my-4">
						<v-list-item-group
							multiple
							v-for="item in riesgos"
							:key="item.key"
						>
							<v-list-item
								@click="item.selected = !item.selected"
							>
								<v-list-item-action>
									<v-checkbox
										v-model="item.selected"
										:input-value="item.selected"
									></v-checkbox>
								</v-list-item-action>

								<v-list-item-content>
									<v-list-item-title>{{
										item.titulo
									}}</v-list-item-title>
									<v-list-item-subtitle>{{
										item.descripcion
									}}</v-list-item-subtitle>
								</v-list-item-content>
							</v-list-item>
						</v-list-item-group>
					</v-list>
				</v-container>
			</v-card-text>

			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn color="primary darken-1" @click="dialog = false" text>
					Cerrar
				</v-btn>
				<v-btn color="primary" v-on:click="asociarRiesgos">
					Asociar riesgos
				</v-btn>
			</v-card-actions>

			<alerta-error
				:mensaje="mensajeError"
				:snackbar="snackbar"
				v-on:alertfin="alertaFin"
			></alerta-error>
		</v-card>
	</v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'
import AlertaError from '../Genericos/AlertaError.vue'

interface Riesgo {
	id: number
	selected: boolean
	titulo: string
	descripcion: string
	criticidad: string
}

export default Vue.extend({
	components: {
		AlertaError,
	},

	props: ['id'],
	data() {
		return {
			estaCargando: true,
			formValido: true,
			dialog: false,

			riesgos: [
				{
					id: 1,
					selected: false,
					titulo: 'Corte del servicio de energía eléctrica',
					descripcion:
						'Corte repentino de la electricidad en la totalidad de la organización.',
					criticidad: 'Alta',
				},
				{
					id: 2,
					selected: true,
					titulo: 'Corte del servicio de internet de Netuno',
					descripcion:
						'Corte del servicio de internet de fibra óptica de Netuno.',
					criticidad: 'Mediana',
				},
				{
					id: 3,
					selected: false,
					titulo: 'Corte del servicio de agua',
					descripcion:
						'Corte del servicio del servicio de agua dentro de la organización.',
					criticidad: 'Baja',
				},
			] as Riesgo[],
			criticidad: ['Alto', 'Mediano', 'Bajo'],

			//Variable para seleccionar los elementos
			settings: [],

			//Para el manejo del mensaje
			mensajeError: '',
			snackbar: false,
		}
	},
	computed: {
		/*
      nameErrors () {
        const errors = []
        if (!this.$v.name.$dirty) return errors
        !this.$v.name.maxLength && errors.push('Name must be at most 10 characters long')
        !this.$v.name.required && errors.push('Name is required.')
        return errors
      },
		*/
	},
	methods: {
		asociarRiesgos() {
			console.log('Objeto a enviar: ')
			console.log(this.riesgos)
			console.log('Objeto de settings: ')
			console.log(this.settings)

			/**
			 * Cuando sea exitoso
			 */

			this.estaCargando = false

			console.log('[Oferta creada satisfactoriamente]')

			//Si la oferta fue exitosamente creada, mostramos mensaje de éxito y cerramos el modal
			this.dialog = false

			this.$emit(
				'alertexito',
				'¡Los riesgos han sido asociados satisfactoriamente!'
			)

			/**
			 * Cuando ocurra un error
			 */
			/*
			console.warn('Algo pasó: ')
			this.mensajeError =
				'El nombre de este riesgo ya se encuentra registrado en el sistema'
			this.snackbar = true
			*/
		},
		obtenerRiesgos() {
			console.log('[ID del escenario] ', this.$props.id)

			this.estaCargando = false
		},
		alertaFin() {
			this.snackbar = false
		},
		seleccionarCheckbox(item: boolean) {
			console.log('SELECTED')
			item = !item
		},
	},
})
</script>

<style></style>