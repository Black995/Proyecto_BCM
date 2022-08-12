<template>
    <div class="container-fluid">
        <b-row class="mt-3" align-v="center">
            <b-col>
                <h4>Seleccione una de las incidencias</h4>
                <div class="text-center">
                    <b-spinner v-if="loadingIncidents" type="grow"></b-spinner>
                    <b-form-select
                        v-if="!loadingIncidents"
                        v-model="incidentId"
                        :options="incidents"
                        value-field="id"
                        text-field="name"
                        label="Incidencias"
                        @change="changeIncident"
                    ></b-form-select>
                </div>
            </b-col>
        </b-row>
        <b-row class="mt-3" align-v="center">
            <b-col>
                <h5>Gráfica de ejemplo</h5>
                <apexchart
                    width="500"
                    type="bar"
                    :options="options"
                    :series="series"
                ></apexchart>
            </b-col>
            <b-col> </b-col>
        </b-row>
    </div>
</template>

<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import NotificationTemplate from "../Notifications/NotificationTemplate";
import VueApexCharts from "vue-apexcharts";

export default {
    name: "IncidentHistory",
    components: {
        VueApexCharts,
    },
    data: () => ({
        permissions: [],
        is_superuser: false,

        loadingIncidents: false,

        incidents: [],
        incidentId: 0,

        risks: [],
        servicesOffered: [],
        servicesUsed: [],
        organizationActivities: [],

        /**
         * Variables a utilizar para las gráficas de ApexChart
         */
        options: {
            chart: {
                id: "vuechart-example",
            },
            xaxis: {
                categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998],
            },
        },
        series: [
            {
                name: "series-1",
                data: [30, 40, 45, 50, 49, 60, 70, 91],
            },
        ],
    }),
    mounted() {
        this.getIncidents();
        this.permissions = JSON.parse(localStorage.getItem("permissions"));
        this.is_superuser = localStorage.getItem("is_superuser");
    },
    methods: {
        successMessage(successText) {
            this.$notify({
                component: NotificationTemplate,
                title: successText,
                icon: "ti-check",
                horizontalAlign: "right",
                verticalAlign: "top",
                type: "success",
            });
        },
        errorMessage(errorText) {
            this.$notify({
                component: NotificationTemplate,
                title: errorText,
                icon: "ti-check",
                horizontalAlign: "right",
                verticalAlign: "top",
                type: "danger",
            });
        },
        async getIncidents() {
            this.incidents = [];
            this.loadingIncidents = true;

            axios
                .get(`${SERVER_ADDRESS}/api/phase3/incident-histories/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for (var i = 0; i < res.data.length; i++) {
                        let inc = {
                            id: res.data[i].id,
                            name:
                                res.data[i].crisis_scenario_name +
                                " (Fecha de inicio: " +
                                res.data[i].start_date.slice(0, 10) +
                                " " +
                                res.data[i].start_date.slice(11, 16) +
                                " - Fecha fin: " +
                                res.data[i].end_date.slice(0, 10) +
                                " " +
                                res.data[i].end_date.slice(11, 16) +
                                ")",
                            description: res.data[i].description,
                        };
                        this.incidents.push(inc);
                    }
                    this.loadingIncidents = false;
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

        changeIncident() {
            this.getRisks();
            this.getServicesOffered();
            this.getServicesUsed();
            this.getOrganizationActivities();
        },
        getRisks() {
            this.risks = [];

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase3/incident-history/risks/${this.incidentId}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.risks = res.data.risks_incident;
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
        getServicesOffered() {
            this.servicesOffered = [];

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase3/incident-history/services-offered/${this.incidentId}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    for (var i = 0; i < res.data.risks_incident.length; i++) {
                        for (
                            var j = 0;
                            j <
                            res.data.risks_incident[i].services_offered_risk
                                .length;
                            j++
                        ) {
                            if (
                                !this.servicesOffered.find(
                                    (k) =>
                                        k.id ===
                                        res.data.risks_incident[i]
                                            .services_offered_risk[j].id
                                )
                            ) {
                                this.servicesOffered.push(
                                    res.data.risks_incident[i]
                                        .services_offered_risk[j]
                                );
                            }
                        }
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
        getServicesUsed() {
            this.servicesUsed = [];

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase3/incident-history/services-used/${this.incidentId}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    for (var i = 0; i < res.data.risks_incident.length; i++) {
                        for (
                            var j = 0;
                            j <
                            res.data.risks_incident[i].services_used_risk
                                .length;
                            j++
                        ) {
                            if (
                                !this.servicesUsed.find(
                                    (k) =>
                                        k.id ===
                                        res.data.risks_incident[i]
                                            .services_used_risk[j].id
                                )
                            ) {
                                this.servicesUsed.push(
                                    res.data.risks_incident[i]
                                        .services_used_risk[j]
                                );
                            }
                        }
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
        getOrganizationActivities() {
            this.organizationActivities = [];

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase3/incident-history/organization-activities/${this.incidentId}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    for (var i = 0; i < res.data.risks_incident.length; i++) {
                        for (
                            var j = 0;
                            j <
                            res.data.risks_incident[i]
                                .organization_activities_risk.length;
                            j++
                        ) {
                            if (
                                !this.organizationActivities.find(
                                    (k) =>
                                        k.id ===
                                        res.data.risks_incident[i]
                                            .organization_activities_risk[j].id
                                )
                            ) {
                                this.organizationActivities.push(
                                    res.data.risks_incident[i]
                                        .organization_activities_risk[j]
                                );
                            }
                        }
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
<style lang="scss">
</style>
