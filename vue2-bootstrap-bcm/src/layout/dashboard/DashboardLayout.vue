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
                    v-if="
                        is_superuser == true ||
                        permissions.includes(
                            'bcm_phase2.view_organizationactivity'
                        )
                    "
                    to="/layout/actividades-de-negocio"
                    name="Act. del Negocio"
                    icon="ti-desktop"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase2.view_interestedparty')
                    "
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
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase2.view_ressource')
                    "
                    to="/layout/recursos"
                    name="Recursos"
                    icon="ti-desktop"
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
                <!--sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase3.view_incident_impact')
                    "
                    to="/layout/impacto-incidentes"
                    name="Impacto Incidentes (all)"
                    icon="ti-blackboard"
                /-->
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase3.view_incident_impact')
                    "
                    to="/layout/impacto-incidente"
                    name="Impacto del Incidente"
                    icon="ti-blackboard"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes('bcm_phase3.view_risk_heatmap')
                    "
                    to="/layout/mapa-calor"
                    name="Mapa de Calor Riesgos"
                    icon="ti-map"
                />
                <sidebar-link
                    v-if="
                        is_superuser == true ||
                        permissions.includes(
                            'bcm_phase3.view_contingencyplanblock'
                        )
                    "
                    to="/layout/planes-contingencia"
                    name="Planes de Contingencia"
                    icon="ti-layers"
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
import axios from "axios";
import TopNavbar from "./TopNavbar.vue";
import DashboardContent from "./Content.vue";
import MobileMenu from "./MobileMenu";
import { SERVER_ADDRESS } from "../../../config/config";
export default {
    components: {
        TopNavbar,
        DashboardContent,
        MobileMenu,
    },
    data: () => ({
        permissions: [],
        is_superuser: true,
        activation: null
    }),
    mounted() {
        this.permissions = JSON.parse(localStorage.getItem("permissions"));
        this.is_superuser = localStorage.getItem("is_superuser");
        this.verifyActivation()
    },
    methods: {
        toggleSidebar() {
            if (this.$sidebar.showSidebar) {
                this.$sidebar.displaySidebar(false);
            }
        },
        async verifyActivation(){
            axios
                .get(`${SERVER_ADDRESS}/api/config/get_activation_state/`)
                    .then((res) => {
                        if (res.data.length) {
                            this.activation = res.data[0].state
                            if (!localStorage.getItem("isLoggedin")){
                                this.$router.push("/");
                                
                            }
                        } else {
                            this.activation = false
                            this.$router.push("/");
                            
                        }
                    })
                    .catch((err) => {
                        try {
                            // Error 400 por unicidad o 500 generico
                            if (err.response.status == 400) {
                                for (let e in err.response.data) {
                                    this.errorMessage(
                                        e + ": " + err.response.data[e]
                                    );
                                }
                            } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                                );
                            }
                        } catch {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    });
        },

    },

};
</script>
