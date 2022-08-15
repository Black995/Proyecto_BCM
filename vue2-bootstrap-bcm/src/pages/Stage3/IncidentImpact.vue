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
                <h5 v-if="loadingServicesOffered" class="text-center">
                    Criticidad de los servicios de la organización afectados
                </h5>
                <div v-if="loadingServicesOffered" id="services-offered">
                    <apexchart
                        type="bar"
                        height="500"
                        :options="chartOptionsServicesOffered"
                        :series="seriesServicesOffered"
                    ></apexchart>
                </div>
            </b-col>
            <b-col>
                <h5 v-if="loadingServicesUsed" class="text-center">
                    Criticidad de los servicios de soporte afectados
                </h5>
                <div v-if="loadingServicesUsed" id="services-used">
                    <apexchart
                        type="bar"
                        height="500"
                        :options="chartOptionsServicesUsed"
                        :series="seriesServicesUsed"
                    ></apexchart>
                </div>
            </b-col>
        </b-row>
        <b-row class="mt-3" align-v="center">
            <b-col>
                <h5 v-if="loadingOrgActivities" class="text-center">
                    Criticidad de las actividades del negocio afectadas
                </h5>
                <div v-if="loadingOrgActivities" id="organization-activities">
                    <apexchart
                        type="bar"
                        height="500"
                        :options="chartOptionsOrgActivities"
                        :series="seriesOrgActivities"
                    ></apexchart>
                </div>
            </b-col>
            <b-col>
                <h5 v-if="loadingStaffsArea" class="text-center">
                    Cantidad del personal afectado por área
                </h5>
                <div v-if="loadingStaffsArea" id="staffs-area">
                    <apexchart
                        type="polarArea"
                        height="500"
                        :options="chartOptionsStaffsArea"
                        :series="seriesStaffsArea"
                    ></apexchart>
                </div>
            </b-col>
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
        staffs: [],
        staffsArea: [],

        /**
         * Variables a utilizar para las gráficas de ApexChart
         */
        loadingServicesOffered: false,
        seriesServicesOffered: [
            {
                name: "Criticidad",
                data: [],
            },
        ],
        chartOptionsServicesOffered: {
            chart: {
                id: "services-offered",
                type: "bar",
                height: 100,
                width: 200,
            },
            plotOptions: {
                bar: {
                    borderRadius: 10,
                    dataLabels: {
                        position: "top", // top, center, bottom
                    },
                },
            },
            xaxis: {
                categories: [],
                position: "top",
                axisBorder: {
                    show: false,
                },
                axisTicks: {
                    show: false,
                },
                crosshairs: {
                    fill: {
                        type: "gradient",
                        gradient: {
                            colorFrom: "#D8E3F0",
                            colorTo: "#BED1E6",
                            stops: [0, 100],
                            opacityFrom: 0.4,
                            opacityTo: 0.5,
                        },
                    },
                },
                tooltip: {
                    enabled: true,
                },
            },
            yaxis: {
                min: 0,
                max: 0,
                labels: {
                    rotate: 0,
                    rotateAlways: false,
                    formatter: function (val) {
                        return val.toFixed(0);
                    },
                },
                decimalsInFloat: 0,
            },
            responsive: [
                {
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 350,
                        },
                        legend: {
                            position: "bottom",
                        },
                    },
                },
            ],
            /*
            title: {
                text: "Criticidad de los servicios de la organización",
                floating: true,
                //offsetY: 330,
                align: "center",
                style: {
                    color: "#718AFF",
                },
            },
            */
        },
        loadingServicesUsed: false,
        seriesServicesUsed: [
            {
                name: "Criticidad",
                data: [],
            },
        ],
        chartOptionsServicesUsed: {
            chart: {
                id: "services-used",
                type: "bar",
                height: 200,
                width: 400,
            },
            plotOptions: {
                bar: {
                    borderRadius: 10,
                    dataLabels: {
                        position: "top", // top, center, bottom
                    },
                },
            },
            xaxis: {
                categories: [],
                position: "top",
                axisBorder: {
                    show: false,
                },
                axisTicks: {
                    show: false,
                },
                crosshairs: {
                    fill: {
                        type: "gradient",
                        gradient: {
                            colorFrom: "#D8E3F0",
                            colorTo: "#BED1E6",
                            stops: [0, 100],
                            opacityFrom: 0.4,
                            opacityTo: 0.5,
                        },
                    },
                },
                tooltip: {
                    enabled: true,
                },
            },
            yaxis: {
                min: 0,
                max: 0,
                labels: {
                    rotate: 0,
                    rotateAlways: false,
                    formatter: function (val) {
                        return val.toFixed(0);
                    },
                },
                decimalsInFloat: 0,
            },
            responsive: [
                {
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 350,
                        },
                        legend: {
                            position: "bottom",
                        },
                    },
                },
            ],
        },
        loadingOrgActivities: false,
        seriesOrgActivities: [
            {
                name: "Criticidad",
                data: [],
            },
        ],
        chartOptionsOrgActivities: {
            chart: {
                id: "organization-activities",
                type: "bar",
                height: 200,
                width: 400,
            },
            plotOptions: {
                bar: {
                    borderRadius: 10,
                    dataLabels: {
                        position: "top", // top, center, bottom
                    },
                },
            },
            xaxis: {
                categories: [],
                position: "top",
                axisBorder: {
                    show: false,
                },
                axisTicks: {
                    show: false,
                },
                crosshairs: {
                    fill: {
                        type: "gradient",
                        gradient: {
                            colorFrom: "#D8E3F0",
                            colorTo: "#BED1E6",
                            stops: [0, 100],
                            opacityFrom: 0.4,
                            opacityTo: 0.5,
                        },
                    },
                },
                tooltip: {
                    enabled: true,
                },
            },
            yaxis: {
                min: 0,
                max: 0,
                labels: {
                    rotate: 0,
                    rotateAlways: false,
                    formatter: function (val) {
                        return val.toFixed(0);
                    },
                },
                decimalsInFloat: 0,
            },
            responsive: [
                {
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 350,
                        },
                        legend: {
                            position: "bottom",
                        },
                    },
                },
            ],
        },
        loadingStaffsArea: false,
        seriesStaffsArea: [],
        chartOptionsStaffsArea: {
            chart: {
                id: "staffs-area",
                height: 200,
                width: 400,
                type: "radialBar",
            },
            stroke: {
                colors: ["#fff"],
            },
            fill: {
                opacity: 0.8,
            },
            yaxis: {
                labels: {
                    rotate: 0,
                    rotateAlways: false,
                    formatter: function (val) {
                        return val.toFixed(0);
                    },
                },
                decimalsInFloat: 0,
            },
            labels: [],
            responsive: [
                {
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 350,
                        },
                        legend: {
                            position: "bottom",
                        },
                    },
                },
            ],
        },
    }),
    mounted() {
        this.getIncidents();
        this.permissions = JSON.parse(localStorage.getItem("permissions"));
        this.is_superuser = localStorage.getItem("is_superuser");
        /**
         * Llamamos a los métodos que tienen las escalas de las vistas
         */
        this.getServiceOfferedScale();
        this.getServiceUsedScale();
        this.getOrgActivitiesScale();
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
        async getServiceOfferedScale() {
            axios
                .get(`${SERVER_ADDRESS}/api/config/scales/view/`, {
                    params: { name: "Servicios de la Organización" },
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.chartOptionsServicesOffered.yaxis.min = parseInt(
                        res.data[0].scale_min_value
                    );
                    this.chartOptionsServicesOffered.yaxis.max = parseInt(
                        res.data[0].scale_max_value
                    );
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
        async getServiceUsedScale() {
            axios
                .get(`${SERVER_ADDRESS}/api/config/scales/view/`, {
                    params: { name: "Servicios de Soporte" },
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.chartOptionsServicesUsed.yaxis.min = parseInt(
                        res.data[0].scale_min_value
                    );
                    this.chartOptionsServicesUsed.yaxis.max = parseInt(
                        res.data[0].scale_max_value
                    );
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
        async getOrgActivitiesScale() {
            axios
                .get(`${SERVER_ADDRESS}/api/config/scales/view/`, {
                    params: { name: "Actividades de la Organización" },
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.chartOptionsOrgActivities.yaxis.min = parseInt(
                        res.data[0].scale_min_value
                    );
                    this.chartOptionsOrgActivities.yaxis.max = parseInt(
                        res.data[0].scale_max_value
                    );
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
            this.getServicesOfferedStaff();
            this.getServicesUsed();
            this.getOrganizationActivities();
        },
        countStaffsArea() {
            console.log("Función para contar personal por área");
            this.staffsArea = [];

            this.staffs.forEach((x) => {
                // Checking if there is any object in arr2
                // which contains the key value
                if (
                    this.staffsArea.some((val) => {
                        return val.staff_area_name == x.staff_area_name;
                    })
                ) {
                    // If yes! then increase the occurrence by 1
                    this.staffsArea.forEach((k) => {
                        if (k.staff_area_name === x.staff_area_name) {
                            k["occurrence"]++;
                        }
                    });
                } else {
                    // If not! Then create a new object initialize
                    // it with the present iteration key's value and
                    // set the occurrence to 1
                    let a = {};
                    a = {
                        staff_area_name: x.staff_area_name,
                        occurrence: 1,
                    };
                    this.staffsArea.push(a);
                }
            });

            console.log("Cantidad de staffs por área");
            console.log(this.staffsArea);

            for (var i = 0; i < this.staffsArea.length; i++) {
                this.chartOptionsStaffsArea.labels.push(
                    this.staffsArea[i].staff_area_name
                );
                this.seriesStaffsArea.push(this.staffsArea[i].occurrence);
            }
            console.log("Elementos para la gráfica del personal");
            console.log(this.seriesStaffsArea);
            console.log(this.chartOptionsStaffsArea.labels);
            this.loadingStaffsArea = true;
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
        getServicesOfferedStaff() {
            this.loadingServicesOffered = false;
            this.loadingStaffsArea = false;
            this.servicesOffered = [];
            this.staffs = [];
            this.chartOptionsServicesOffered.xaxis.categories = [];
            this.seriesServicesOffered[0].data = [];
            this.chartOptionsStaffsArea.labels = [];
            this.seriesStaffsArea = [];

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
                            // Servicios de la org.
                            if (
                                !this.servicesOffered.find(
                                    (x) =>
                                        x.id ===
                                        res.data.risks_incident[i]
                                            .services_offered_risk[j].id
                                )
                            ) {
                                this.servicesOffered.push(
                                    res.data.risks_incident[i]
                                        .services_offered_risk[j]
                                );
                                /**
                                 * Variables para la gráfica
                                 */
                                this.chartOptionsServicesOffered.xaxis.categories.push(
                                    res.data.risks_incident[i]
                                        .services_offered_risk[j].name
                                );
                                this.seriesServicesOffered[0].data.push(
                                    res.data.risks_incident[i]
                                        .services_offered_risk[j].criticality
                                );
                            }
                            // Staffs
                            for (
                                var k = 0;
                                k <
                                res.data.risks_incident[i]
                                    .services_offered_risk[j].staffs_service
                                    .length;
                                k++
                            ) {
                                // En caso de que no esté el objeto en el array
                                if (
                                    !this.staffs.find(
                                        (x) =>
                                            x.staff ===
                                            res.data.risks_incident[i]
                                                .services_offered_risk[j]
                                                .staffs_service[k].staff
                                    )
                                ) {
                                    this.staffs.push(
                                        res.data.risks_incident[i]
                                            .services_offered_risk[j]
                                            .staffs_service[k]
                                    );
                                }
                                // En caso de que sí esté el objeto en el array,
                                // entonces verificamos si aparece como relevante
                                else {
                                    if (
                                        !this.staffs.find(
                                            (x) =>
                                                x.staff ===
                                                    res.data.risks_incident[i]
                                                        .services_offered_risk[
                                                        j
                                                    ].staffs_service[k].staff &&
                                                res.data.risks_incident[i]
                                                    .services_offered_risk[j]
                                                    .staffs_service[k]
                                                    .relevant === true
                                        )
                                    ) {
                                        for (var z = 0; z < this.staffs; z++) {
                                            if (
                                                this.staffs[z].staff ==
                                                res.data.risks_incident[i]
                                                    .services_offered_risk[j]
                                                    .staffs_service[k].staff
                                            ) {
                                                this.staffs[z] = objArr.slice(
                                                    0,
                                                    z
                                                );
                                                this.staffs.push(
                                                    res.data.risks_incident[i]
                                                        .services_offered_risk[
                                                        j
                                                    ].staffs_service[k]
                                                );
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                    //console.log("Servicios de la organización:");
                    //console.log(this.servicesOffered);
                    //console.log("Staffs:");
                    //console.log(this.staffs);
                    this.countStaffsArea();
                    this.loadingServicesOffered = true;
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
            this.chartOptionsServicesUsed.xaxis.categories = [];
            this.seriesServicesUsed[0].data = [];
            this.loadingServicesUsed = false;

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
                                /**
                                 * Variables para la gráfica
                                 */
                                this.chartOptionsServicesUsed.xaxis.categories.push(
                                    res.data.risks_incident[i]
                                        .services_used_risk[j].name
                                );
                                this.seriesServicesUsed[0].data.push(
                                    res.data.risks_incident[i]
                                        .services_used_risk[j].criticality
                                );
                            }
                        }
                    }
                    //console.log("Servicios de soporte:");
                    //console.log(this.servicesUsed);
                    this.loadingServicesUsed = true;
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
            this.chartOptionsOrgActivities.xaxis.categories = [];
            this.seriesOrgActivities[0].data = [];
            this.loadingOrgActivities = false;

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
                                /**
                                 * Variables para la gráfica
                                 */
                                this.chartOptionsOrgActivities.xaxis.categories.push(
                                    res.data.risks_incident[i]
                                        .organization_activities_risk[j].name
                                );
                                this.seriesOrgActivities[0].data.push(
                                    res.data.risks_incident[i]
                                        .organization_activities_risk[j]
                                        .criticality
                                );
                            }
                        }
                    }
                    //console.log("Actividades de la organización:");
                    //console.log(this.organizationActivities);
                    this.loadingOrgActivities = true;
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
