import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";

// Login
import Login from "@/pages/Login/Login.vue";
// Admin pages
import UserProfile from "@/pages/UserProfile.vue";
import Notifications from "@/pages/Notifications.vue";
import Icons from "@/pages/Icons.vue";
import Maps from "@/pages/Maps.vue";
import Typography from "@/pages/Typography.vue";
import TableList from "@/pages/TableList.vue";

// Stages Pages

// Stage 1
import Risks from "@/pages/Stage1/Risks.vue";
import CrisisScenarios from "@/pages/Stage1/CrisisScenarios.vue";


const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login,
  },
  {
    path: "/layout",
    component: DashboardLayout,
    redirect: "/dashboard",
    children: [
      {
        path: "riesgos",
        name: "Riesgos",
        component: Risks
      },
      {
        path: "escenarios-criticos",
        name: "Escenarios Críticos",
        component: CrisisScenarios
      },
      {
        path: "stats",
        name: "stats",
        component: UserProfile
      },
      {
        path: "notifications",
        name: "notifications",
        component: Notifications
      },
      {
        path: "icons",
        name: "icons",
        component: Icons
      },
      {
        path: "maps",
        name: "maps",
        component: Maps
      },
      {
        path: "typography",
        name: "typography",
        component: Typography
      },
      {
        path: "table-list",
        name: "table-list",
        component: TableList
      }
    ]
  },
  { path: "*", component: NotFound }
];

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes;
