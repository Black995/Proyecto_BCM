<template>
	<v-snackbar v-model="mostrar" :timeout="-1">
		{{ message }}

		<template v-slot:action="{ attrs }">
			<v-btn
				color="pink"
				text
				v-bind="attrs"
				@click="changeSnackbarState"
			>
				Close
			</v-btn>
		</template>
	</v-snackbar>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
	props: ['message', 'snackbar'],
	data() {
		return {
			mostrar: false,
		}
	},
	methods: {
		changeSnackbarState() {
			this.$emit('alertend')
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