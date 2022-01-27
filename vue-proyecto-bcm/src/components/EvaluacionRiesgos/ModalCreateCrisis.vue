<template>
	<v-dialog v-model="dialog" id="modal-crear">
		<template v-slot:activator="{ on, attrs }">
			<v-btn
				color="secondary"
				style="color: black"
				rounded
				v-bind="attrs"
				v-on="on"
			>
				Agregar escenario crítico
			</v-btn>
		</template>

		<v-card>
			<v-form ref="form" v-model="validForm" lazy-validation>
				<v-card-title class="header-table">
					<v-row justify="space-between" class="pa-1">
						<span class="text-h5"
							>Crear nuevo escenario crítico</span
						>
						<v-btn icon @click="dialog = false">
							<v-icon color="white">mdi-close</v-icon>
						</v-btn>
					</v-row>
				</v-card-title>
				<v-divider></v-divider>
				<v-card-text>
					<v-container>
						<v-text-field
							v-model="crisis.name"
							:counter="50"
							:rules="rules.name"
							label="Ingrese el título del escenario crítico"
						></v-text-field>
						<v-row>
							<v-col cols="12" sm="12" md="12" lg="12" xl="12">
								<v-textarea
									v-model="crisis.description"
									:counter="200"
									label="Ingrese la descripción del escenario crítico"
									hint="La descripción debería tener entre 10 y 200 caracteres"
									:rules="rules.description"
								></v-textarea>
							</v-col>
						</v-row>
					</v-container>
				</v-card-text>
			</v-form>

			<!--v-card-text>
				<v-container>
					<h2 class="font-weight-medium text-center my-2">
						Asocie los riesgos de la organización al escenario
						crítico
					</h2>
					<v-list flat subheader three-line class="my-4">
						<v-list-item-group
							multiple
							v-for="item in risks"
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
										item.name
									}}</v-list-item-title>
									<v-list-item-subtitle>{{
										item.description
									}}</v-list-item-subtitle>
								</v-list-item-content>
							</v-list-item>
						</v-list-item-group>
					</v-list>
				</v-container>
			</v-card-text-->

			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn color="primary darken-1" @click="dialog = false" text>
					Cerrar
				</v-btn>
				<modal-confirm-create-crisis
					:disabled="validForm"
					v-on:crear="Crear"
				></modal-confirm-create-crisis>
			</v-card-actions>

			<alert-error
				:message="mensajeError"
				:snackbar="snackbar"
				v-on:alertend="alertEnd"
			></alert-error>
		</v-card>
	</v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import { SERVER_ADDRESS, TOKEN } from '../../../config/config'

import ModalConfirmCreateCrisis from './ModalConfirmCreateCrisis.vue'
import AlertError from '../Genericos/AlertError.vue'

interface Crisis {
	name: string
	description: string
	//risks: number[]
}

interface Risk {
	id: number
	selected: boolean
	name: string
	description: string
}

export default Vue.extend({
	components: {
		AlertError,
		ModalConfirmCreateCrisis,
	},

	data() {
		return {
			estaCargando: true,
			validForm: false,
			dialog: false,

			crisis: {
				name: '',
				description: '',
				//risks: [],
			} as Crisis,
			risks: [] as Risk[],
			criticidad: ['Alto', 'Mediano', 'Bajo'],

			//Para el manejo del mensaje
			mensajeError: '' as string,
			snackbar: false as boolean,

			rules: {
				name: [
					(v: any) => !!v || 'Este campo es obligatorio',
					(v: any) =>
						(v && v.length <= 50) ||
						'El nombre debe contener como máximo 50 caracteres',
					//Validación de correo
					//v => v === null || v.length === 0 || (/^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/.test(v)) || 'Debe ser un correo electrónico valido'
				],
				description: [
					(v: any) => !!v || 'Este campo es obligatorio',
					(v: any) =>
						(v && v.length >= 10 && v && v.length <= 200) ||
						'La descripción debe contener entre 10 y 200 caracteres',
				],
			},
		}
	},
	methods: {
		/*
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

					for (let i = 0; i < res.data.length; i++) {
						var risk: Risk = {
							id: res.data[i].id,
							name: res.data[i].name,
							description: res.data[i].description,
							selected: false,
						}
						this.risks.push(risk)
					}
					//this.risks = res.data
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
		*/
		async Crear() {
			//Validación de los inputs
			if (
				!(
					this.$refs.form as Vue & { validate: () => boolean }
				).validate()
			)
				return

			/*
			for (let i = 0; i < this.risks.length; i++) {
				if (this.risks[i].selected) {
					this.crisis.risks.push(this.risks[i].id)
				}
			}
			*/

			axios
				.post(
					`${SERVER_ADDRESS}/api/risks/crisis_scenarios/`,
					this.crisis,
					{
						withCredentials: true,
						headers: {
							Authorization: TOKEN,
						},
					}
				)
				.then((res) => {
					this.estaCargando = false

					//Si el escenario crítico fue exitosamente creada, mostramos mensaje de éxito y cerramos el modal
					this.dialog = false

					//Reinicializamos variable del crear
					this.crisis = {
						name: '',
						description: '',
						//risks: [],
					}

					this.$emit(
						'alertexito',
						'¡El riesgo ha sido creado satisfactoriamente!'
					)
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
		selectCheckbox(item: boolean) {
			item = !item
		},
		alertEnd() {
			this.snackbar = false
		},
	},
})
</script>

<style></style>