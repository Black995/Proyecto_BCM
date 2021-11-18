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
				Agregar una nueva parte interesada
			</v-btn>
		</template>

		<v-card>
			<v-form ref="formulario" v-model="formValido" lazy-validation>
				<v-card-title class="header-table">
					<v-row justify="space-between mx-auto" class="pa-1">
						<span class="text-h5">Crear nueva parte interesada</span>
						<v-btn icon @click="dialog = false">
							<v-icon color="white">mdi-close</v-icon>
						</v-btn>
					</v-row>
				</v-card-title>
				<v-divider></v-divider>
				<v-card-text>
					<v-container>
						<v-text-field
							v-model="parte.nombre"
							:counter="50"
							:rules="[(v) => !!v || 'Este campo es obligatorio']"
							label="Ingrese el nombre de la parte interesada"
						></v-text-field>

						
						<v-row>
							<v-col cols="12" sm="12" md="12" lg="12" xl="12">
								<v-textarea
									v-model="parte.descripcion"
									label="Ingrese la descripción de la parte interesada"
									hint="La descripción debería tener entre 10 y 200 caracteres"
									:rules="[
										(v) =>
											!!v || 'Este campo es obligatorio',
									]"
								></v-textarea>
							</v-col>
                            <v-col cols="12" sm="12" md="12" lg="12" xl="12">
								<v-textarea
									v-model="parte.tipo"
									label="Ingrese el tipo de la parte interesada"
									hint="El tipo debería tener entre 1 y 10 caracteres"
									:rules="[
										(v) =>
											!!v || 'Este campo es obligatorio',
									]"
								></v-textarea>
							</v-col>
						</v-row>
					</v-container>
				</v-card-text>

				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn
						color="primary darken-1"
						@click="dialog = false"
						text
					>
						Cerrar
					</v-btn>
					<v-btn color="primary" v-on:click="crear">
						Crear parte interesada
					</v-btn>
				</v-card-actions>

				<alerta-error
					:mensaje="mensajeError"
					:snackbar="snackbar"
					v-on:alertfin="alertaFin"
				></alerta-error>
			</v-form>
		</v-card>
	</v-dialog>
</template>

<script lang="ts">
import Vue from 'vue'
import AlertaError from '../Genericos/AlertaError.vue'

interface ParteInteresada {
	nombre: string
	descripcion: string
	tipo: string
}

//import { validationMixin } from 'vuelidate';
//import { required, maxLength, email } from 'vuelidate/lib/valid;

export default Vue.extend({
	components: {
		AlertaError,
	},

	/*
	mixins: [validationMixin],

    validations: {
      name: { required, maxLength: maxLength(10) },
      email: { required, email },
      select: { required },
      checkbox: {
        checked (val) {
          return val
        },
      },
    },
	*/

	data() {
		return {
			estaCargando: true,
			formValido: true,
			dialog: false,

			parte: {
				nombre: '',
				descripcion: '',
				tipo: '',
			} as ParteInteresada,
			

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
		crear() {
			console.log('Objeto a enviar: ')
			console.log(this.parte)

			/**
			 * Cuando sea exitoso
			 */

			this.estaCargando = false

			console.log('[Oferta creada satisfactoriamente]')

			//Si la oferta fue exitosamente creada, mostramos mensaje de éxito y cerramos el modal
			this.dialog = false

			//Reinicializamos variable del crear
			this.parte = {
				nombre: '',
				descripcion: '',
				tipo: '',
			}

			this.$emit(
				'alertexito',
				'¡La parte interesada ha sido creada satisfactoriamente!'
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
		alertaFin() {
			this.snackbar = false
		},
	},
})
</script>

<style></style>