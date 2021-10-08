import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Login from '../views/Login.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
	{
		path: '/',
		name: 'Login',
		component: Login,
	},
	{
		path: '/layout',
		name: 'Layout',

		component: () => import('../layout/Layout.vue'),
		children: [
			/**
			 * Vistas internas de la app
			 */
			{
				path: '/riesgos',
				name: 'Evaluación de Riesgos',
				component: () => import('../views/EvaluacionRiesgos.vue'),
			},
			{
				path: '/partes-interesadas',
				name: 'Partes Interesadas',
				component: () => import('../views/PartesInteresadas.vue'),
			},
			{
				path: '/actividades',
				name: 'Actividades del Negocio',
				component: () => import('../views/ActividadesNegocio.vue'),
			},
		],
	},
]

const router = new VueRouter({
	mode: 'history',
	base: process.env.BASE_URL,
	routes,
})

export default router
