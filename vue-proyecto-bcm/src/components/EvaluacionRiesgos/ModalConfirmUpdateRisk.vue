<template>
	<v-dialog v-model="dialog" persistent max-width="350">
		<template v-slot:activator="{ on, attrs }">
			<v-btn
				color="primary"
				:disabled="!$props.disabled"
				v-bind="attrs"
				v-on="on"
			>
				Editar riesgo
			</v-btn>
		</template>

		<v-card>
			<v-card-title class="text-h5">
				¿Está seguro de editar este riesgo?
			</v-card-title>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn color="primary darken-1" text @click="dialog = false">
					Cerrar
				</v-btn>
				<v-btn color="primary" text @click="confirmarEditar">
					Confirmar
				</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>


<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
	props: ['disabled'],
	data() {
		return {
			dialog: false,
		}
	},
	methods: {
		confirmarEditar() {
			this.dialog = false

			this.$emit('editar')
		},
	},
})
</script>

