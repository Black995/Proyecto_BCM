<template>
	<v-alert
		border="left"
		close-text="Cerrar"
		type="success"
		dismissible
		@click="dismissAlert"
	>
		{{ message }}
	</v-alert>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
	props: ['message'],
	data() {
		return {}
	},
	methods: {
		dismissAlert() {
			this.$emit('dismisssuccess')
		},
	},
})
</script>

<style></style>