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
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase1.view_risk') ||
                        permissions.includes('bcm_phase1.view_crisisscenario')
                    "
                    to="#1"
                    class="disabled"
                    name="Fase 1"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase1.view_risk')
                    "
                    to="/layout/riesgos"
                    name="Riesgos"
                    icon="ti-stats-down"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase1.view_crisisscenario')
                    "
                    to="/layout/escenarios-criticos"
                    name="Escenarios Críticos"
                    icon="ti-panel"
                />
                <!--
                    Encabezado Fase 2
                -->
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase2.view_staff') ||
                        permissions.includes(
                            'bcm_phase2.view_serviceoffered'
                        ) ||
                        permissions.includes('bcm_phase2.view_serviceused')
                    "
                    to="#2"
                    name="Fase 2"
                />
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
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase2.view_staff')
                    "
                    to="/layout/personal"
                    name="Personal de la Org."
                    icon="ti-layout-accordion-list"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase2.view_serviceoffered')
                    "
                    to="/layout/servicios-ofrecidos"
                    name="Servicios de la Org."
                    icon="ti-desktop"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase2.view_serviceused')
                    "
                    to="/layout/servicios-usados"
                    name="Servicios de Soporte"
                    icon="ti-dropbox"
                />
                <!--
                    Encabezado Fase 3
                -->
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase3.view_incidenthistory')
                    "
                    to="#1"
                    class="disabled"
                    name="Fase 3"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase3.view_incidenthistory')
                    "
                    to="/layout/historico-incidentes"
                    name="Histórico de Incidentes"
                    icon="ti-exchange-vertical"
                />
                <!--
                    Encabezado Configuración
                -->
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('configuration.view_area') ||
                        permissions.includes('configuration.view_position') ||
                        permissions.includes(
                            'configuration.view_organization'
                        ) ||
                        permissions.includes('configuration.view_scale') ||
                        permissions.includes('configuration.view_scaleview') |
                            permissions.includes('auth.view_group') ||
                        permissions.includes(
                            'configuration.view_headquarter'
                        ) ||
                        permissions.includes('users.view_user')
                    "
                    to="#3"
                    name="Configuración"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('configuration.view_area')
                    "
                    to="/layout/areas"
                    name="Areas de la Org."
                    icon="ti-menu-alt"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('configuration.view_position')
                    "
                    to="/layout/cargos"
                    name="Cargos"
                    icon="ti-bar-chart"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('configuration.view_organization')
                    "
                    to="/layout/empresa"
                    name="Empresa"
                    icon="ti-briefcase"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('configuration.view_scale') ||
                        permissions.includes('configuration.view_scaleview')
                    "
                    to="/layout/escalas"
                    name="Escalas"
                    icon="ti-ruler-alt"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('auth.view_group')
                    "
                    to="/layout/roles"
                    name="Roles"
                    icon="ti-layers-alt"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('configuration.view_headquarter')
                    "
                    to="/layout/sedes"
                    name="Sedes"
                    icon="ti-map"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('users.view_user')
                    "
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
        this.permissions = JSON.parse(localStorage.getItem("permissions"));
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
