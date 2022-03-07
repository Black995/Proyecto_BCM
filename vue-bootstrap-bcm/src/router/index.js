import { createRouter, createWebHistory } from 'vue-router'

//Vue.use(VueRouter);

const routes = [
    {
        path: '/',
        name: 'Login',
        component: () => import('../login/Login.vue'),
    },
    {
        path: '/dashboard',
        name: 'Dashboard',

        component: () => import('../dashboard/Dashboard.vue'),
        children: [
            /**
             * Vistas internas de la app
             */

            //Módulo del perfil
            /*
            {
                path: '/perfil',
                name: 'Perfil',
                component: () => import('../views/Profile.vue'),
            },
            */

            //Módulo de la fase 1
            {
                path: '/riesgos',
                name: 'Risks',
                component: () => import('../dashboard/Risks.vue'),
            },
            {
                path: '/escenarios-criticos',
                name: 'CrisisScenarios',
                component: () => import('../dashboard/CrisisScenarios.vue'),
            },
            /*
                //Módulo de la fase 2
                {
                    path: '/partes-interesadas',
                    name: 'Partes Interesadas',
                    component: () => import('../views/InterestedParties.vue'),
                },
                {
                    path: '/actividades',
                    name: 'Actividades del Negocio',
                    component: () => import('../views/BusinessActivity.vue'),
                },
                {
                    path: '/servicios-ofrecidos',
                    name: 'Servicios Ofrecidos',
                    component: () => import('../views/ServicesOffered.vue'),
                },
                {
                    path: '/servicios-usadoss',
                    name: 'Servicios Usados',
                    component: () => import('../views/ServicesUsed.vue'),
                },
                {
                    path: '/empleados',
                    name: 'Empleados',
                    component: () => import('../views/Employees.vue'),
                },
         
                //Módulo de la fase 3
                {
                    path: '/incidentes',
                    name: 'Incidentes',
                    component: () => import('../views/Incidents.vue'),
                },
            	
                //Módulo de configuración
                {
                    path: '/areas',
                    name: 'Areas',
                    component: () => import('../views/Areas.vue'),
                },
                {
                    path: '/escalas',
                    name: 'Escalas',
                    component: () => import('../views/Scales.vue'),
                },
                */
        ],
    },
]

/*
const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    routes,
});
*/

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router;
