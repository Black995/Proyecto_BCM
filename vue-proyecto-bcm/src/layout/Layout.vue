<template>
	<div>
		<v-app-bar dark>
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

		<v-navigation-drawer v-model="drawer" color="black" absolute temporary>
			<v-list-item>
				<v-list-item-avatar>
					<v-img
						src="https://randomuser.me/api/portraits/men/78.jpg"
					></v-img>
				</v-list-item-avatar>

				<v-list-item-content>
					<v-list-item-title style="color: #ffffff"
						>Alan Sosa</v-list-item-title
					>
				</v-list-item-content>
			</v-list-item>

			<v-divider></v-divider>

			<!--v-menu
				:close-on-content-click="false"
				open-on-hover
				bottom
				offset-y
			>
				<template v-slot:activator="{ on }">
					<v-btn color="primary" dark v-on="on"> Dropdown </v-btn>
				</template>
				<v-list>
					<v-list-group
						v-for="item in items"
						:key="item.title"
						v-model="item.active"
						:prepend-icon="item.action"
						no-action
					>
						<template v-slot:activator>
							<v-list-tile>
								<v-list-tile-content>
									<v-list-tile-title>{{
										item.title
									}}</v-list-tile-title>
								</v-list-tile-content>
							</v-list-tile>
						</template>

						<v-list-tile
							v-for="subItem in item.items"
							:key="subItem.title"
						>
							<v-list-tile-content>
								<v-list-tile-title>{{
									subItem.title
								}}</v-list-tile-title>
							</v-list-tile-content>

							<v-list-tile-action>
								<v-icon>{{ subItem.action }}</v-icon>
							</v-list-tile-action>
						</v-list-tile>
					</v-list-group>
				</v-list>
			</v-menu-->

			<!--
				Pruebas sidebar
			-->
			<v-list nav dense>
				<v-list-group
					color="white"
					class="class-group"
					v-for="item in menuOptions"
					:key="item.title"
					v-model="item.active"
					no-action
				>
					<template v-slot:activator>
						<v-list-item-content
							>{{ item.title }}
						</v-list-item-content>
					</template>

					<v-list-item-group>
						<v-list-item
							class="list-navbar"
							active-class="list-navbar-active"
							v-for="(opt, i) in item.items"
							:key="i"
							:to="{ name: opt.toDato }"
							exact-path
							sub-group
						>
							<v-list-item-icon class="list-navbar">
								<v-icon style="color: #ffffff">{{
									opt.icono
								}}</v-icon>
							</v-list-item-icon>
							<v-list-item-title>{{
								opt.opcion
							}}</v-list-item-title>

							<!--v-list-tile-content>
							<v-list-tile-title>{{
								opt.option
							}}</v-list-tile-title>
						</v-list-tile-content>

						<v-list-tile-action>
							<v-icon style="color: #ffffff">{{
								opt.icono
							}}</v-icon>
						</v-list-tile-action-->
						</v-list-item>
					</v-list-item-group>
				</v-list-group>
			</v-list>
			<!--
				Pruebas sidebar
			-->

			<!--v-list nav dense>
				<v-list-item-group>
					<v-list-item
						class="list-navbar"
						active-class="list-navbar-active"
						v-for="(opt, i) in opcionesMenu"
						:key="i"
						:to="{ name: opt.toDato }"
						exact-path
					>
						<v-list-item-icon class="list-navbar">
							<v-icon style="color: #ffffff">{{
								opt.icono
							}}</v-icon>
						</v-list-item-icon>
						<v-list-item-title>{{ opt.opcion }}</v-list-item-title>
					</v-list-item>
				</v-list-item-group>
			</v-list-->

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
		menuOptions: [
			{
				title: 'Fase 1',
				active: true,
				items: [
					{
						opcion: 'Evaluación de Riesgos',
						icono: 'mdi-alert-circle-check',
						toDato: 'Evaluación de Riesgos',
					},
				],
			},
			{
				title: 'Fase 2',
				active: false,
				items: [
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
						opcion: 'Empleados',
						icono: 'mdi-account-hard-hat',
						toDato: 'Empleados',
					},
				],
			},
			{
				title: 'Fase 3',
				active: false,
				items: [
					{
						opcion: 'Incidentes',
						icono: 'mdi-alert',
						toDato: 'Incidentes',
					},
				],
			},
			{
				title: 'Configuración',
				active: false,
				items: [
					{
						opcion: 'Areas',
						icono: 'mdi-lan',
						toDato: 'Areas',
					},
					{
						opcion: 'Escalas',
						icono: 'mdi-scale-balance',
						toDato: 'Escalas',
					},
				],
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


<style lang="scss">
.header-table {
	background: #000000;
	color: #ffffff !important;
}

.main-background {
	background: #f1f1f1;
	background-size: 100%;
}

.list-navbar {
	color: #ffffff !important;
	&:hover {
		background-color: #505050;
		color: #fff;
	}
}

.list-navbar-active {
	background-color: #646464;
	color: #ffffff !important;
}

.class-group {
	color: #ffffff !important;
	background-color: #818181;
}
</style>