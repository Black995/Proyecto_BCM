<template>
	<div>
		<v-app-bar color="#002060" dark>
			<v-app-bar-nav-icon
				@click.stop="drawer = !drawer"
			></v-app-bar-nav-icon>

			<v-toolbar-title>{{ this.$route.name }}</v-toolbar-title>

			<v-spacer></v-spacer>

			<v-menu offset-y>
				<template v-slot:activator="{ on, attrs }">
					<v-btn
						style="position: relative; left: -15px"
						icon
						v-bind="attrs"
						v-on="on"
					>
						<v-list-item-avatar>
							<v-img
								src="https://randomuser.me/api/portraits/men/78.jpg"
							></v-img>
						</v-list-item-avatar>
					</v-btn>
				</template>
				<v-list>
					<v-list-item :to="{ name: 'Perfil' }" link>
						<v-list-item-icon>
							<v-icon>mdi-account-box</v-icon>
						</v-list-item-icon>
						<v-list-item-title>Editar perfil</v-list-item-title>
					</v-list-item>
					<!--v-list-item @click="closeSession">
						<v-list-item-icon>
							<v-icon>mdi-logout</v-icon>
						</v-list-item-icon>
						<v-list-item-title>Cerrar sesión</v-list-item-title>
					</v-list-item-->
				</v-list>
			</v-menu>
		</v-app-bar>

		<v-navigation-drawer v-model="drawer" absolute temporary>
			<v-list-item>
				<v-list-item-avatar>
					<v-img
						src="https://randomuser.me/api/portraits/men/78.jpg"
					></v-img>
				</v-list-item-avatar>

				<v-list-item-content>
					<v-list-item-title>Alan Sosa</v-list-item-title>
				</v-list-item-content>
			</v-list-item>

			<v-divider></v-divider>

			<v-list nav dense>
				<v-list-item-group>
					<v-list-item
						v-for="(opt, i) in opcionesMenu"
						:key="i"
						:to="{ name: opt.toDato }"
						exact-path
					>
						<v-list-item-icon>
							<v-icon>{{ opt.icono }}</v-icon>
						</v-list-item-icon>
						<v-list-item-title>{{ opt.opcion }}</v-list-item-title>
					</v-list-item>
				</v-list-item-group>
			</v-list>

			<template v-slot:append>
				<div class="pa-2" style="height: 75px; position: relative">
					<v-btn block top @click="closeSession"> Logout </v-btn>
				</div>
			</template>
		</v-navigation-drawer>

		<v-main class="main-background">
			<router-view></router-view>
		</v-main>
	</div>
</template>


<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
	name: 'Layout',
	data: () => ({
		drawer: false,
		group: null,
		nombreEmpresa: '',
		opcionesMenu: [
			{
				opcion: 'Evaluación de Riesgos',
				icono: 'mdi-alert-circle-check',
				toDato: 'Evaluación de Riesgos',
			},
			{
				opcion: 'Partes Interesadas',
				icono: 'mdi-account-group',
				toDato: 'Partes Interesadas',
			},
			{
				opcion: 'Actividades del Negocio',
				icono: 'mdi-sitemap',
				toDato: 'Actividades del Negocio',
			},
			{
				opcion: 'Servicios Ofrecidos',
				icono: 'mdi-face-agent',
				toDato: 'Servicios Ofrecidos',
			},
			{
				opcion: 'Servicios Usados',
				icono: 'mdi-toolbox',
				toDato: 'Servicios Usados',
			},
			{
				opcion: 'Personal de la organización',
				icono: 'mdi-account-hard-hat',
				toDato: 'Personal de la organización',
			},
			{
				opcion: 'Incidentes',
				icono: 'mdi-alert',
				toDato: 'Incidentes',
			},
		],
	}),

	watch: {
		group() {
			this.drawer = false
		},
	},

	methods: {
		//Se eliminan los datos de la caché
		closeSession() {
			localStorage.removeItem('token')
			this.$router.replace({ name: 'Login' })
		},
	},
})
</script>


<style>
.header-table {
	background: #002060;
	color: #ffffff !important;
}

.main-background {
	background: #f1f1f1;
	background-size: 100%;
}
</style>