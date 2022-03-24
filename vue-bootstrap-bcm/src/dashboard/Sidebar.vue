<template>
    <!-- Main Sidebar Container -->
    <aside class="main-sidebar sidebar-dark-primary elevation-4">
        <!-- Brand Logo -->
        <a href="index3.html" class="brand-link">
            <img
                src="../assets/img/AdminLTELogo.png"
                alt="AdminLTE Logo"
                class="brand-image img-circle elevation-3"
                style="opacity: 0.8"
            />
            <span class="brand-text font-weight-light">PrototipoApp</span>
        </a>

        <!-- Sidebar -->
        <div class="sidebar">
            <!-- Sidebar Menu -->
            <!--nav class="mt-2">
                <ul
                    class="nav nav-pills nav-sidebar flex-column"
                    data-widget="treeview"
                    role="menu"
                    data-accordion="false"
                >
                    <li class="nav-item has-treeview">
                        <a
                            href="#"
                            routerLinkActive="active"
                            class="nav-link pl-0"
                        >
                            <i class="nav-icon fas fa-landmark"></i>
                            <p>
                                Gobierno y Cultura
                                <i class="right fas fa-angle-left"></i>
                            </p>
                        </a>
                        <ul class="nav nav-treeview">
                            <li class="nav-item">
                                <a
                                    routerLink="/gobierno-cultura/identidad-etica"
                                    routerLinkActive="active"
                                    class="nav-link"
                                >
                                    <i class="far fa-id-badge nav-icon"></i>
                                    <p>Identidad y Ética</p>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a
                                    routerLink="/gobierno-cultura/junta-directiva"
                                    routerLinkActive="active"
                                    class="nav-link"
                                >
                                    <i class="fas fa-sitemap nav-icon"></i>
                                    <p>Junta Directiva</p>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a
                                    routerLink="/gobierno-cultura/responsabilidades"
                                    routerLinkActive="active"
                                    class="nav-link"
                                >
                                    <i class="far fa-hourglass nav-icon"></i>
                                    <p>Responsabilidades</p>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a
                                    routerLink="/gobierno-cultura/areas"
                                    routerLinkActive="active"
                                    class="nav-link"
                                >
                                    <i class="fas fa-city nav-icon"></i>
                                    <p>Áreas</p>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a
                                    routerLink="/gobierno-cultura/manuales-operativos"
                                    routerLinkActive="active"
                                    class="nav-link"
                                >
                                    <i class="fas fa-book nav-icon"></i>
                                    <p>Manuales Operativos</p>
                                </a>
                            </li>
                            <li class="nav-item">
                                <a
                                    routerLink="/gobierno-cultura/documentos-oficiales"
                                    routerLinkActive="active"
                                    class="nav-link"
                                >
                                    <i class="fas fa-gavel nav-icon"></i>
                                    <p>Documentos Oficiales</p>
                                </a>
                            </li>
                        </ul>
                    </li>
                    
                </ul>
            </nav-->

            <nav class="mt-2">
                <ul
                    class="nav nav-pills nav-sidebar flex-column"
                    data-widget="treeview"
                    role="menu"
                    data-accordion="false"
                    v-for="item in menuOptions"
                    :key="item.title"
                >
                    <li class="nav-item has-treeview">
                        <a
                            href="#"
                            routerLinkActive="{ item.active }"
                            class="nav-link pl-0"
                        >
                            <i class="nav-icon fas fa-landmark"></i>
                            <p>
                                {{ item.title }}
                                <i class="right fas fa-angle-left"></i>
                            </p>
                        </a>
                        <ul class="nav nav-treeview">
                            <li
                                class="nav-item"
                                v-for="(opt, i) in item.items"
                                :key="i"
                            >
                                <router-link
                                    :to="{ name: opt.toDato }"
                                    active-class="active"
                                    class="nav-link"
                                >
                                    <i class="far fa-id-badge nav-icon"></i>
                                    <p>{{ opt.opcion }}</p>
                                </router-link>
                            </li>
                        </ul>
                    </li>
                </ul>
            </nav>
            <!-- /.sidebar-menu -->
        </div>
        <!-- /.sidebar -->
    </aside>
</template>

<script>
export default {
    name: "Sidebar",
    data: () => ({
        drawer: false,
        group: null,
        nombreEmpresa: "",
        menuOptions: [
            {
                title: "Módulo 1",
                active: true,
                items: [
                    {
                        opcion: "Riesgos",
                        icono: "mdi-alert-circle-check",
                        toDato: "Risks",
                    },
                    {
                        opcion: "Escenarios Críticos",
                        icono: "mdi-alert-circle-check",
                        toDato: "CrisisScenarios",
                    },
                ],
            },
            {
                title: "Módulo 2",
                active: false,
                items: [
                    {
                        opcion: "Partes Interesadas",
                        icono: "mdi-account-group",
                        toDato: "Partes Interesadas",
                    },
                    {
                        opcion: "Actividades del Negocio",
                        icono: "mdi-sitemap",
                        toDato: "Actividades del Negocio",
                    },
                    {
                        opcion: "Servicios Ofrecidos",
                        icono: "mdi-face-agent",
                        toDato: "Servicios Ofrecidos",
                    },
                    {
                        opcion: "Servicios Usados",
                        icono: "mdi-toolbox",
                        toDato: "Servicios Usados",
                    },
                    /*
                    {
                        opcion: "Empleados",
                        icono: "mdi-account-hard-hat",
                        toDato: "Empleados",
                    },
                    */
                ],
            },
            /*
            {
                title: "Módulo 3",
                active: false,
                items: [
                    {
                        opcion: "Incidentes",
                        icono: "mdi-alert",
                        toDato: "Incidentes",
                    },
                ],
            },
            {
                title: "Configuración",
                active: false,
                items: [
                    {
                        opcion: "Areas",
                        icono: "mdi-lan",
                        toDato: "Areas",
                    },
                    {
                        opcion: "Escalas",
                        icono: "mdi-scale-balance",
                        toDato: "Escalas",
                    },
                ],
            },
            */
        ],
    }),
};
</script>

<style>
</style>