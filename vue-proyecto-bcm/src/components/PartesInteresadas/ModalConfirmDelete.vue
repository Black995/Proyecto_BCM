<template>
	<v-dialog v-model="dialog" persistent max-width="440">
		<template v-slot:activator="{ on, attrs }">
			<v-icon
				color="red"
				style="color: black"
				title="Eliminar riesgo"
				v-bind="attrs"
				v-on="on"
			>
				mdi-delete-forever
			</v-icon>
		</template>

		<v-card>
			<v-card-title class="text-h5">
				¿Está seguro de eliminar esta parte interesada?
			</v-card-title>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn color="primary darken-1" text @click="dialog = false">
					Cerrar
				</v-btn>
				<v-btn color="primary" text @click="confirmDelete">
					Confirmar
				</v-btn>
			</v-card-actions>
		</v-card>

		<alert-error
			:mensaje="mensajeError"
			:snackbar="snackbar"
			v-on:alertfin="alertaFin"
		></alert-error>
	</v-dialog>
</template>

<script lang="ts">

import Vue from 'vue'
import AlertError from '../Genericos/AlertError.vue'


export default Vue.extend({
    components:{
        AlertError,
    },
    data() {
        return {
            dialog: false,

            //Para el manejo del mensaje de error
			mensajeError: '',
			snackbar: false,
        }
    },
    methods:{
        alertaFin(){
            this.snackbar = false;
        }
    }

})
</script>