<template>
	<v-snackbar v-model="mostrar" :timeout="-1">
		{{ mensaje }}

		<template v-slot:action="{ attrs }">
			<v-btn
				color="pink"
				text
				v-bind="attrs"
				@click="cambiarEstadoSnackbar"
			>
				Close
			</v-btn>
		</template>
	</v-snackbar>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
	props: ['mensaje', 'snackbar'],
	data() {
		return {
			mostrar: false,
		}
	},
	methods: {
		cambiarEstadoSnackbar() {
			this.$emit('alertfin')
		},
	},
	watch: {
		snackbar(nuevoValor) {
			this.mostrar = nuevoValor
		},
	},
})
</script>

<style></style>