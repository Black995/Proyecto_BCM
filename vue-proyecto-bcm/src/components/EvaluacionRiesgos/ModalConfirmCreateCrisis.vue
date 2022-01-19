<template>
	<v-dialog v-model="dialog" persistent max-width="350">
		<template v-slot:activator="{ on, attrs }">
			<v-btn color="primary" v-bind="attrs" v-on="on">
				Crear escenario crítico
			</v-btn>
		</template>

		<v-card>
			<v-card-title class="text-h5">
				¿Está seguro de crear este escenario crítico?
			</v-card-title>
			<v-card-actions>
				<v-spacer></v-spacer>
				<v-btn color="primary darken-1" text @click="dialog = false">
					Cerrar
				</v-btn>
				<v-btn color="primary" text @click="confirmarCrear">
					Confirmar
				</v-btn>
			</v-card-actions>
		</v-card>
	</v-dialog>
</template>


<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
	data() {
		return {
			dialog: false,
		}
	},
	methods: {
		confirmarCrear() {
			this.dialog = false

			this.$emit('crear')
		},
	},
})
</script>

