<template>
	<v-container class="login" fill-height fill-width fluid>
		<v-row no-gutters justify="center">
			<v-layout align-center justify-center>
				<v-flex xs12 sm8 md4>
					<v-card class="elevation-12">
						<v-toolbar dark color="primary">
							<v-spacer>
								<v-toolbar-title class="text-center"
									>Iniciar sesión</v-toolbar-title
								>
							</v-spacer>

							<!--v-row v-if="mensajeError">
								<v-col class="error--text">
									<v-alert
										text
										color="error"
										dense
										v-if="mensajeError"
									>
										<v-icon color="error">
											mdi-alert
										</v-icon>
										<span
											v-text="mensajeError"
											class="ml-1"
										>
										</span>
									</v-alert>
								</v-col>
							</v-row-->
						</v-toolbar>
						<v-card-text>
							<v-form ref="form">
								<v-row
									text
									align="center"
									justify="center"
									v-if="mensajeError"
								>
									<v-alert
										border="left"
										color="pink darken-1"
										dark
									>
										{{ mensajeError }}
									</v-alert></v-row
								>
								<v-text-field
									v-model="user.email"
									prepend-icon="mdi-account"
									label="Usuario"
									type="email"
								></v-text-field>
								<v-text-field
									v-model="user.password"
									prepend-icon="mdi-shield-lock"
									label="Contraseña"
									type="password"
								></v-text-field>
							</v-form>
						</v-card-text>
						<v-card-actions>
							<v-spacer></v-spacer>
							<v-btn
								color="primary"
								@click="login"
								:loading="loadingForm"
								type="submit"
								>Login</v-btn
							>
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

interface User {
	email: string
	password: string
}

export default Vue.extend({
	data() {
		return {
			estaCargando: true,
			validForm: false,
			loadingForm: false,
			dialog: false,

			user: {
				email: '',
				password: '',
			} as User,

			//Para el manejo del mensaje
			mensajeError: '' as string,
			snackbar: false as boolean,
		}
	},
	methods: {
		async login() {
			//if (this.$refs.form.validate()) {
			this.mensajeError = ''
			this.loadingForm = true

			axios
				.post(`${SERVER_ADDRESS}/api/token/`, this.user)
				.then((res) => {
					if (res.status === 200) {
						/**
						 * Se guarda el token en local storage (provicionalmente)
						 */
						this.$router.push('/riesgos')
						localStorage.setItem('token', res.data.access)
					}
				})
				.catch((error) => {
					try {
						this.loadingForm = false
						//this.$refs.form.reset();
						this.mensajeError =
							error.response.status === 500
								? 'Ha ocurrido un error inesperado en el servidor, por favor inténtalo de nuevo.'
								: 'Correo electrónico o contraseña incorrecta.'
					} catch {
						this.mensajeError =
							'Ha ocurrido un error inesperado en el servidor, por favor inténtalo de nuevo.'
					}
				})
			//}
		},
	},
})
</script>

<style lang="scss">
.login {
	background: #f1f1f1;
}
</style>
