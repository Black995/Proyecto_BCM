<template>
	<v-container fill-height fill-width class="fondo-primary" fluid>
		<v-row no-gutters justify="center">
			<h3>Iniciar sesión</h3>
		</v-row>
	</v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import axios from 'axios'
import { SERVER_ADDRESS } from '../../config/config'

export default Vue.extend({
	name: 'Login',
	async mounted() {
		axios
			.post(`${SERVER_ADDRESS}/api/token/`, {
				email: 'alansaul25@gmail.com',
				password: '12345',
			})
			.then((res) => {
				/**
				 * Temporalmente se guardará el token en localStorage
				 */
				console.log(res.data.access)
				localStorage.setItem('token', res.data.access)
			})
			.catch(function (error) {
				console.log('Ups! Ha ocurrido un error en el servidor')
				console.log(error.toJSON())
			})
	},
})
</script>
