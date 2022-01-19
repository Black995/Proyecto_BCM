<template>
	<v-container class="login" fill-height fill-width fluid>
		<v-row no-gutters justify="center">
			<!--h3>Iniciar sesión</h3-->
			<v-layout align-center justify-center>
				<v-flex xs12 sm8 md4>
					<v-card class="elevation-12">
						<v-toolbar dark color="primary">
							<v-spacer>
								<v-toolbar-title class="text-center"
									>Iniciar sesión</v-toolbar-title
								>
							</v-spacer>
						</v-toolbar>
						<v-card-text>
							<v-form>
								<v-text-field
									prepend-icon="mdi-account"
									name="login"
									label="Usuario"
									type="text"
								></v-text-field>
								<v-text-field
									prepend-icon="mdi-shield-lock"
									name="password"
									label="Contraseña"
									type="password"
								></v-text-field>
							</v-form>
						</v-card-text>
						<v-card-actions>
							<v-spacer></v-spacer>
							<v-btn color="primary" to="/riesgos">Login</v-btn>
						</v-card-actions>
					</v-card>
				</v-flex>
			</v-layout>
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

<style lang="scss">
.login {
	background: #f1f1f1;
}
</style>
