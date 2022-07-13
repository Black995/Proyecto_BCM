<template>
    <div class="wrapper">
        <side-bar>
            <template slot="links">
                <!--
                    Encabezado Fase 1
                -->
                <sidebar-link
                    to="/layout/perfil"
                    name="Perfil"
                    icon="ti-user"
                />
                <sidebar-link to="#1" class="disabled" name="Fase 1" />
                <sidebar-link
                    to="/layout/riesgos"
                    name="Riesgos"
                    icon="ti-stats-down"
                />
                <sidebar-link
                    to="/layout/escenarios-criticos"
                    name="Escenarios Críticos"
                    icon="ti-panel"
                />
                <!--
                    Encabezado Fase 2
                -->
                <sidebar-link to="#2" name="Fase 2" />
                <sidebar-link
                    to="/layout/actividades-de-negocio"
                    name="Act. del Negocio"
                    icon="ti-desktop"
                />
                <sidebar-link
                    to="/layout/partes-interesadas"
                    name="Partes Interesadas"
                    icon="ti-desktop"
                />
                <sidebar-link
                    to="/layout/personal"
                    name="Personal de la Org."
                    icon="ti-layout-accordion-list"
                />
                <sidebar-link
                    to="/layout/servicios-ofrecidos"
                    name="Servicios de la Org."
                    icon="ti-desktop"
                />
                <sidebar-link
                    to="/layout/servicios-usados"
                    name="Servicios de Soporte"
                    icon="ti-dropbox"
                />
                <!--
                    Encabezado Configuración
                -->
                <sidebar-link to="#3" name="Configuración" />
                <sidebar-link
                    to="/layout/areas"
                    name="Areas de la Org."
                    icon="ti-menu-alt"
                />
                <sidebar-link
                    to="/layout/cargos"
                    name="Cargos"
                    icon="ti-bar-chart"
                />
                <sidebar-link
                    to="/layout/empresa"
                    name="Empresa"
                    icon="ti-briefcase"
                />
                <sidebar-link
                    to="/layout/escalas"
                    name="Escalas"
                    icon="ti-ruler-alt"
                />
                <sidebar-link
                    to="/layout/roles"
                    name="Roles"
                    icon="ti-layers-alt"
                />
                <sidebar-link to="/layout/sedes" name="Sedes" icon="ti-map" />
                <sidebar-link
                    to="/layout/usuarios"
                    name="Usuarios"
                    icon="ti-user"
                />
                <!--sidebar-link
                    to="/layout/stats"
                    name="User Profile"
                    icon="ti-user"
                />
                <sidebar-link
                    to="/layout/table-list"
                    name="Table List"
                    icon="ti-view-list-alt"
                />
                <sidebar-link
                    to="/layout/typography"
                    name="Typography"
                    icon="ti-text"
                />
                <sidebar-link
                    to="/layout/icons"
                    name="Icons"
                    icon="ti-pencil-alt2"
                />
                <sidebar-link to="/layout/maps" name="Map" icon="ti-map" />
                <sidebar-link
                    to="/layout/notifications"
                    name="Notifications"
                    icon="ti-bell"
                /-->
            </template>
            <mobile-menu>
                <li class="nav-item">
                    <a class="nav-link">
                        <i class="ti-panel"></i>
                        <p>Stats</p>
                    </a>
                </li>
                <drop-down
                    class="nav-item"
                    title="5 Notifications"
                    title-classes="nav-link"
                    icon="ti-bell"
                >
                    <a class="dropdown-item">Notification 1</a>
                    <a class="dropdown-item">Notification 2</a>
                    <a class="dropdown-item">Notification 3</a>
                    <a class="dropdown-item">Notification 4</a>
                    <a class="dropdown-item">Another notification</a>
                </drop-down>
                <li class="nav-item">
                    <a class="nav-link">
                        <i class="ti-settings"></i>
                        <p>Settings</p>
                    </a>
                </li>
                <li class="divider"></li>
            </mobile-menu>
        </side-bar>
        <div class="main-panel">
            <top-navbar></top-navbar>

            <dashboard-content @click.native="toggleSidebar">
            </dashboard-content>
        </div>
    </div>
</template>
<style lang="scss">
</style>
<script>
import TopNavbar from "./TopNavbar.vue";
import DashboardContent from "./Content.vue";
import MobileMenu from "./MobileMenu";
export default {
    components: {
        TopNavbar,
        DashboardContent,
        MobileMenu,
    },
    data: () => ({
        permissions: [],
        is_superuser: false,
    }),
    mounted() {
        this.permissions = localStorage.getItem("permissions");
        this.is_superuser = localStorage.getItem("is_superuser");
    },
    methods: {
        toggleSidebar() {
            if (this.$sidebar.showSidebar) {
                this.$sidebar.displaySidebar(false);
            }
        },
    },
};
</script>
