<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <b-row align-v="center">
                    <b-col>
                        <h4 class="text-center">
                            Gráficas del impacto de los incidentes ocurridos por
                            rango de fecha
                        </h4>
                    </b-col>
                </b-row>
                <b-row class="mt-3" align-v="center">
                    <b-col>
                        <b-form-group
                            label="Fecha inicio del filtro"
                            invalid-feedback="Este campo es obligatorio"
                            :state="incidentDateFilterState.start_date"
                        >
                            <b-form-datepicker
                                v-model="incidentDateFilter.start_date"
                                :state="incidentDateFilterState.start_date"
                                locale="es"
                            ></b-form-datepicker>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Fecha fin del filtro"
                            invalid-feedback="Este campo es obligatorio"
                            :state="incidentDateFilterState.end_date"
                        >
                            <b-form-datepicker
                                v-model="incidentDateFilter.end_date"
                                :state="incidentDateFilterState.end_date"
                                locale="es"
                            ></b-form-datepicker>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-button variant="info" block @click="getIncidents">
                            Filtrar
                        </b-button>
                    </b-col>
                </b-row>
                <b-row align-v="center">
                    <b-col>
                        <div class="text-center">
                            <b-spinner
                                v-if="loadingIncidents"
                                type="grow"
                            ></b-spinner>

                            <b-list-group v-if="incidents.length" class="mt-3">
                                <b-list-group-item
                                    class="flex-column align-items-start"
                                    v-for="item in incidents"
                                    :key="item.key"
                                >
                                    <div
                                        class="
                                            d-flex
                                            w-100
                                            justify-content-between
                                        "
                                    >
                                        <h5 class="mb-1">
                                            Escenario crítico:
                                            {{ item.crisis_scenario_name }}
                                        </h5>
                                        <small class="text-muted"
                                            >Frecuencia:
                                            {{
                                                item.crisis_scenario_frequency_name
                                            }}</small
                                        >
                                    </div>
                                    <div
                                        class="
                                            mb-1
                                            d-flex
                                            w-100
                                            justify-content-between
                                        "
                                    >
                                        <div>
                                            Fecha inicio: {{ item.start_date }}
                                        </div>
                                        <div v-if="item.end_date">
                                            Fecha fin: {{ item.end_date }}
                                        </div>
                                        <div v-if="!item.end_date">
                                            Fecha fin: -
                                        </div>
                                    </div>
                                    <div class="mb-1 d-flex w-100">
                                        Observaciones del incidente:
                                        {{ item.description }}
                                    </div>
                                </b-list-group-item>
                            </b-list-group>
                        </div>
                    </b-col>
                </b-row>
                <b-row class="mt-3" align-v="center">
                    <b-col>
                        <h5
                            v-if="
                                loadingServicesOffered &&
                                loadingServicesUsed &&
                                loadingOrgActivities &&
                                loadingStaffsArea
                            "
                            class="text-center"
                        >
                            Criticidad de los servicios de soporte afectados
                        </h5>
                        <div
                            v-if="
                                loadingServicesOffered &&
                                loadingServicesUsed &&
                                loadingOrgActivities &&
                                loadingStaffsArea
                            "
                            id="services-used"
                        >
                            <apexchart
                                type="bar"
                                height="500"
                                :options="chartOptionsServicesUsed"
                                :series="seriesServicesUsed"
                            ></apexchart>
                        </div>
                    </b-col>
                    <b-col>
                        <h5
                            v-if="
                                loadingServicesOffered &&
                                loadingServicesUsed &&
                                loadingOrgActivities &&
                                loadingStaffsArea
                            "
                            class="text-center"
                        >
                            Criticidad de las actividades del negocio afectadas
                        </h5>
                        <div
                            v-if="
                                loadingServicesOffered &&
                                loadingServicesUsed &&
                                loadingOrgActivities &&
                                loadingStaffsArea
                            "
                            id="organization-activities"
                        >
                            <apexchart
                                type="bar"
                                height="500"
                                :options="chartOptionsOrgActivities"
                                :series="seriesOrgActivities"
                            ></apexchart>
                        </div>
                    </b-col>
                </b-row>
                <b-row class="mt-3" align-v="center">
                    <b-col>
                        <h5
                            v-if="
                                loadingServicesOffered &&
                                loadingServicesUsed &&
                                loadingOrgActivities &&
                                loadingStaffsArea
                            "
                            class="text-center"
                        >
                            Criticidad de los servicios de la organización
                            afectados
                        </h5>
                        <!--
                    En caso de colocar la clase que facilite el scroll
                -->
                        <!--div
                    v-if="
                        loadingServicesOffered &&
                        loadingServicesUsed &&
                        loadingOrgActivities &&
                        loadingStaffsArea
                    "
                    id="services-offered"
                    class="chart"
                -->
                        <div
                            v-if="
                                loadingServicesOffered &&
                                loadingServicesUsed &&
                                loadingOrgActivities &&
                                loadingStaffsArea
                            "
                            id="services-offered"
                        >
                            <apexchart
                                type="bar"
                                height="500"
                                :options="chartOptionsServicesOffered"
                                :series="seriesServicesOffered"
                            ></apexchart>
                        </div>
                    </b-col>
                </b-row>
                <b-row class="mt-3" align-v="center">
                    <b-col>
                        <h5
                            v-if="
                                loadingServicesOffered &&
                                loadingServicesUsed &&
                                loadingOrgActivities &&
                                loadingStaffsArea
                            "
                            class="text-center"
                        >
                            Cantidad del personal afectado por área
                        </h5>
                        <div
                            v-if="
                                loadingServicesOffered &&
                                loadingServicesUsed &&
                                loadingOrgActivities &&
                                loadingStaffsArea
                            "
                            id="staffs-area"
                        >
                            <apexchart
                                type="polarArea"
                                height="500"
                                :options="chartOptionsStaffsArea"
                                :series="seriesStaffsArea"
                            ></apexchart>
                        </div>
                    </b-col>
                    <b-col>
                        <h5
                            v-if="
                                loadingServicesOffered &&
                                loadingServicesUsed &&
                                loadingOrgActivities &&
                                loadingStaffsArea &&
                                loadingServicesOnlyMinimumRTO &&
                                loadingServicesMinimunRTO
                            "
                            class="text-center"
                        >
                            Servicios que excedieron el RTO debido a la duración
                            del incidente
                        </h5>
                        <div
                            v-if="
                                loadingServicesOffered &&
                                loadingServicesUsed &&
                                loadingOrgActivities &&
                                loadingStaffsArea &&
                                loadingServicesOnlyMinimumRTO &&
                                loadingServicesMinimunRTO
                            "
                            id="services-minimum-rto"
                        >
                            <apexchart
                                type="pie"
                                height="500"
                                :options="chartOptionsServicesMinimunRTO"
                                :series="seriesServicesMinimunRTO"
                            ></apexchart>
                        </div>
                    </b-col>
                </b-row>
                <b-row class="mt-3" align-v="center">
                    <b-col>
                        <h5
                            v-if="
                                loadingServicesOffered &&
                                loadingServicesUsed &&
                                loadingOrgActivities &&
                                loadingStaffsArea &&
                                loadingServicesOnlyMinimumRTO &&
                                loadingServicesMinimunRTO
                            "
                            class="text-center"
                        >
                            Servicios que excedieron el RTO debido a la duración
                            del incidente
                        </h5>
                        <div
                            v-if="
                                loadingServicesOffered &&
                                loadingServicesUsed &&
                                loadingOrgActivities &&
                                loadingStaffsArea &&
                                loadingServicesOnlyMinimumRTO &&
                                loadingServicesMinimunRTO
                            "
                            id="services-only-minimum-rto"
                        >
                            <apexchart
                                type="bar"
                                height="500"
                                :options="chartOptionsServicesOnlyMinimumRTO"
                                :series="seriesServicesOnlyMinimumRTO"
                            ></apexchart>
                        </div>
                    </b-col>
                </b-row>
            </div>
        </div>
    </div>
</template>


<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import NotificationTemplate from "../Notifications/NotificationTemplate";

export default {
    name: "IncidentImpactAll",

    data: () => ({
        permissions: [],
        is_superuser: false,

        incidents: [],
        loadingIncidents: false,
        incidentDateFilter: {
            start_date: "",
            end_date: "",
        },
        incidentDateFilterState: {
            start_date: null,
            end_date: null,
        },

        risks: [],
        servicesOffered: [],
        servicesUsed: [],
        organizationActivities: [],
        staffs: [],
        staffsComplete: [],
        staffsArea: [],
        // Variables para guardar la duración del incidente y para guardar el servicio
        // de la organización y si excedió dicho RTO
        incidentDurationTime: 0,
        servicesByRTO: [],

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
                    colors: {
                        ranges: [
                            {
                                from: 1,
                                to: 999,
                                color: "#08e494",
                            },
                        ],
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
            noData: {
                text: "No se encontraron servicios de soporte",
                align: "center",
                verticalAlign: "middle",
                style: {
                    fontSize: "14px",
                },
            },
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
                    colors: {
                        ranges: [
                            {
                                from: 1,
                                to: 999,
                                color: "#ffc464",
                            },
                        ],
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
            noData: {
                text: "No se encontraron actividades de la organización",
                align: "center",
                verticalAlign: "middle",
                style: {
                    fontSize: "14px",
                },
            },
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
            noData: {
                text: "No se encontró personal asignado a los servicios de la organización",
                align: "center",
                verticalAlign: "middle",
                style: {
                    fontSize: "14px",
                },
            },
        },
        loadingServicesMinimunRTO: false,
        seriesServicesMinimunRTO: [],
        chartOptionsServicesMinimunRTO: {
            chart: {
                id: "services-minimum-rto",
                //height: 200,
                width: 400,
                type: "pie",
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
            noData: {
                text: "No se encontraron servicios de la organización",
                align: "center",
                verticalAlign: "middle",
                style: {
                    fontSize: "14px",
                },
            },
        },
        loadingServicesOnlyMinimumRTO: false,
        seriesServicesOnlyMinimumRTO: [
            {
                name: "Criticidad",
                data: [],
            },
        ],
        chartOptionsServicesOnlyMinimumRTO: {
            chart: {
                id: "services-only-minimum-rto",
                type: "bar",
                height: 200,
                width: 400,
            },
            plotOptions: {
                bar: {
                    borderRadius: 10,
                    horizontal: true,
                    dataLabels: {
                        position: "top", // top, center, bottom
                    },
                },
            },
            dataLabels: {
                enabled: false,
            },
            xaxis: {
                categories: [],
                //position: "top",
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
                labels: {
                    rotate: 0,
                    rotateAlways: false,
                    formatter: function (val) {
                        return val.toFixed(0);
                    },
                },
                tooltip: {
                    enabled: true,
                },
            },
            yaxis: {
                min: 0,
                max: 0,
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
            noData: {
                text: "No se encontraron servicios de la organización que excedieran el RTO",
                align: "center",
                verticalAlign: "middle",
                style: {
                    fontSize: "14px",
                },
            },
        },
    }),
    computed: {
        chartOptionsServicesOffered: function () {
            return {
                chart: {
                    id: "services-offered",
                    type: "bar",
                    height: 100,
                    width: 0,
                    events: {
                        dataPointSelection: (event, chartContext, config) => {
                            this.selectServiceOffered(config.dataPointIndex);
                        },
                    },
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
                noData: {
                    text: "No se encontraron servicios de la organización",
                    align: "center",
                    verticalAlign: "middle",
                    style: {
                        fontSize: "14px",
                    },
                },
            };
        },
    },
    mounted() {
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
                icon: "ti-close",
                horizontalAlign: "right",
                verticalAlign: "top",
                type: "danger",
            });
        },

        selectServiceOffered(index) {
            let service = this.servicesOffered.find(
                (x) =>
                    x.criticality ===
                        this.seriesServicesOffered[0].data[index] &&
                    x.name ===
                        this.chartOptionsServicesOffered.xaxis.categories[index]
            );

            this.countStaffsAreaByService(service.id);
        },
        checkFormValidityFilters() {
            let valid = true;
            if (
                !this.incidentDateFilter.start_date &&
                this.incidentDateFilter.end_date
            ) {
                this.incidentDateFilterState.start_date = false;
                valid = false;
            }
            if (
                this.incidentDateFilter.start_date &&
                !this.incidentDateFilter.end_date
            ) {
                this.incidentDateFilterState.end_date = false;
                valid = false;
            }
            if (
                this.incidentDateFilter.start_date &&
                this.incidentDateFilter.end_date &&
                this.incidentDateFilter.start_date >
                    this.incidentDateFilter.end_date
            ) {
                this.errorMessage(
                    "La fecha inicio no puede ser superior a la fecha fin"
                );
                valid = false;
            }
            return valid;
        },
        async getIncidents() {
            this.incidentDateFilterState.start_date = null;
            this.incidentDateFilterState.end_date = null;
            this.loadingIncidents = true;

            // Exit when the filter isn't valid
            if (!this.checkFormValidityFilters()) {
                this.loadingIncidents = false;
                return;
            } else {
                this.loading = true;
                this.incidents = [];

                axios
                    .get(`${SERVER_ADDRESS}/api/phase3/incident-histories/`, {
                        params: {
                            start_date: this.incidentDateFilter.start_date,
                            end_date: this.incidentDateFilter.end_date,
                        },
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    })
                    .then((res) => {
                        for (var i = 0; i < res.data.length; i++) {
                            let end_date = "";
                            let end_hour = "";
                            if (res.data[i].end_date) {
                                end_date = res.data[i].end_date.slice(0, 10);
                                end_hour = res.data[i].end_date.slice(11, 16);
                            }
                            let inc = {
                                id: res.data[i].id,
                                start_date: res.data[i].start_date.slice(0, 10),
                                start_hour: res.data[i].start_date.slice(
                                    11,
                                    16
                                ),
                                end_date: end_date,
                                end_hour: end_hour,
                                description: res.data[i].description,
                                crisis_scenario_name:
                                    res.data[i].crisis_scenario_name,
                                crisis_scenario_frequency_name:
                                    res.data[i].crisis_scenario_frequency_name,
                            };
                            this.incidents.push(inc);
                        }
                        this.loadingIncidents = false;

                        // Se procede a llamar a los demás requests para las gráficas
                        this.getServicesOfferedStaff();
                        this.getServicesUsed();
                        this.getOrganizationActivities();
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
            }
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
                    this.chartOptionsServicesOnlyMinimumRTO.yaxis.min =
                        parseInt(res.data[0].scale_min_value);
                    this.chartOptionsServicesOnlyMinimumRTO.yaxis.max =
                        parseInt(res.data[0].scale_max_value);
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
        countStaffsArea() {
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

            for (var i = 0; i < this.staffsArea.length; i++) {
                this.chartOptionsStaffsArea.labels.push(
                    this.staffsArea[i].staff_area_name
                );
                this.seriesStaffsArea.push(this.staffsArea[i].occurrence);
            }
            this.loadingStaffsArea = true;
        },
        countStaffsAreaByService(serviceId) {
            this.loadingStaffsArea = false;
            this.staffsArea = [];

            if (serviceId) {
                this.staffsComplete.forEach((x) => {
                    // Checking if there is any object in arr2
                    // which contains the key value
                    if (
                        this.staffsArea.some((val) => {
                            return (
                                val.staff_area_name == x.staff_area_name &&
                                serviceId == x.service_offered
                            );
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
                        if (serviceId == x.service_offered) {
                            let a = {};
                            a = {
                                staff_area_name: x.staff_area_name,
                                occurrence: 1,
                            };
                            this.staffsArea.push(a);
                        }
                    }
                });
            } else {
                this.staffsComplete.forEach((x) => {
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
            }

            this.chartOptionsStaffsArea.labels = [];
            this.seriesStaffsArea = [];

            for (var i = 0; i < this.staffsArea.length; i++) {
                this.chartOptionsStaffsArea.labels.push(
                    this.staffsArea[i].staff_area_name
                );
                this.seriesStaffsArea.push(this.staffsArea[i].occurrence);
            }
            this.loadingStaffsArea = true;
        },
        countServicesMinimumRTO() {
            let countExceedRTO = 0;
            let countNotExceedRTO = 0;

            for (var i = 0; i < this.servicesByRTO.length; i++) {
                if (this.servicesByRTO[i].exceed_recovery_time) {
                    countExceedRTO++;
                } else {
                    countNotExceedRTO++;
                }
            }
            this.seriesServicesMinimunRTO.push(countExceedRTO);
            this.seriesServicesMinimunRTO.push(countNotExceedRTO);

            this.chartOptionsServicesMinimunRTO.labels.push(
                "Servicios que exceden el RTO"
            );
            this.chartOptionsServicesMinimunRTO.labels.push(
                "Servicios que NO exceden el RTO"
            );

            this.loadingServicesMinimunRTO = true;
        },
        getRisks() {
            this.risks = [];

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase3/incident-history/risks/all/`,
                    {
                        params: {
                            start_date: this.incidentDateFilter.start_date,
                            end_date: this.incidentDateFilter.end_date,
                        },
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
            this.loadingServicesMinimunRTO = false;
            this.loadingServicesOnlyMinimumRTO = false;
            this.servicesOffered = [];
            this.staffs = [];
            this.servicesByRTO = [];
            this.chartOptionsServicesOffered.xaxis.categories = [];
            this.seriesServicesOffered[0].data = [];
            this.chartOptionsStaffsArea.labels = [];
            this.seriesStaffsArea = [];
            this.seriesServicesMinimunRTO = [];
            this.chartOptionsServicesMinimunRTO.labels = [];
            this.chartOptionsServicesOnlyMinimumRTO.xaxis.categories = [];
            this.seriesServicesOnlyMinimumRTO[0].data = [];

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase3/incident-history/services-offered/all/`,
                    {
                        params: {
                            start_date: this.incidentDateFilter.start_date,
                            end_date: this.incidentDateFilter.end_date,
                        },
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    for (var t = 0; t < res.data.length; t++) {
                        if (res.data[t].end_date) {
                            let start_date_incident = new Date(
                                res.data[t].start_date
                            ).getTime();
                            let end_date_incident = new Date(
                                res.data[t].end_date
                            ).getTime();
                            // Duración del incidente en milisegundos
                            this.incidentDurationTime =
                                end_date_incident - start_date_incident;
                        }

                        for (
                            var i = 0;
                            i < res.data[t].risks_incident.length;
                            i++
                        ) {
                            for (
                                var j = 0;
                                j <
                                res.data[t].risks_incident[i]
                                    .services_offered_risk.length;
                                j++
                            ) {
                                // Servicios de la org.
                                if (
                                    !this.servicesOffered.find(
                                        (x) =>
                                            x.id ===
                                            res.data[t].risks_incident[i]
                                                .services_offered_risk[j].id
                                    )
                                ) {
                                    this.servicesOffered.push(
                                        res.data[t].risks_incident[i]
                                            .services_offered_risk[j]
                                    );
                                    /**
                                     * Cálculo del RTO del servicio con la duración del
                                     * incidente
                                     *
                                     * SÓLO SE APLICA SI EXISTE LA FECHA FINAL DE LA INCIDENTE
                                     */
                                    let exceed_recovery_time = false;
                                    if (res.data[t].end_date) {
                                        let hours = parseInt(
                                            res.data[t].risks_incident[
                                                i
                                            ].services_offered_risk[
                                                j
                                            ].recovery_time.slice(0, 2)
                                        );
                                        let minutes = parseInt(
                                            res.data[t].risks_incident[
                                                i
                                            ].services_offered_risk[
                                                j
                                            ].recovery_time.slice(3, 5)
                                        );
                                        let recovery_time_service =
                                            hours * 3600000 + minutes * 60000;
                                        if (
                                            this.incidentDurationTime <=
                                            recovery_time_service
                                        ) {
                                            exceed_recovery_time = true;
                                        }
                                        let serviceByRTO = {
                                            id: res.data[t].risks_incident[i]
                                                .services_offered_risk[j].id,
                                            area_name:
                                                res.data[t].risks_incident[i]
                                                    .services_offered_risk[j]
                                                    .area_name,
                                            name: res.data[t].risks_incident[i]
                                                .services_offered_risk[j].name,
                                            type_name:
                                                res.data[t].risks_incident[i]
                                                    .services_offered_risk[j]
                                                    .type_name,
                                            recovery_time:
                                                recovery_time_service,
                                            exceed_recovery_time:
                                                exceed_recovery_time,
                                        };
                                        this.servicesByRTO.push(serviceByRTO);
                                    }
                                    /**
                                     * Variables para la gráfica de servicios de la org.
                                     */
                                    this.chartOptionsServicesOffered.xaxis.categories.push(
                                        res.data[t].risks_incident[i]
                                            .services_offered_risk[j].name
                                    );
                                    this.chartOptionsServicesOffered.chart.width =
                                        this.chartOptionsServicesOffered.chart
                                            .width + 100;
                                    this.seriesServicesOffered[0].data.push(
                                        res.data[t].risks_incident[i]
                                            .services_offered_risk[j]
                                            .criticality
                                    );
                                    /**
                                     * Variables para la gráfica de servicios que exceden el RTO
                                     */
                                    if (exceed_recovery_time) {
                                        this.chartOptionsServicesOnlyMinimumRTO.xaxis.categories.push(
                                            res.data[t].risks_incident[i]
                                                .services_offered_risk[j].name
                                        );
                                        this.seriesServicesOnlyMinimumRTO[0].data.push(
                                            res.data[t].risks_incident[i]
                                                .services_offered_risk[j]
                                                .criticality
                                        );
                                    }
                                }
                                // Staffs
                                for (
                                    var k = 0;
                                    k <
                                    res.data[t].risks_incident[i]
                                        .services_offered_risk[j].staffs_service
                                        .length;
                                    k++
                                ) {
                                    // Array de staffs para tenerlos todos por servicio
                                    this.staffsComplete.push(
                                        res.data[t].risks_incident[i]
                                            .services_offered_risk[j]
                                            .staffs_service[k]
                                    );

                                    // En caso de que no esté el objeto en el array
                                    if (
                                        !this.staffs.find(
                                            (x) =>
                                                x.staff ===
                                                res.data[t].risks_incident[i]
                                                    .services_offered_risk[j]
                                                    .staffs_service[k].staff
                                        )
                                    ) {
                                        this.staffs.push(
                                            res.data[t].risks_incident[i]
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
                                                        res.data[t]
                                                            .risks_incident[i]
                                                            .services_offered_risk[
                                                            j
                                                        ].staffs_service[k]
                                                            .staff &&
                                                    res.data[t].risks_incident[
                                                        i
                                                    ].services_offered_risk[j]
                                                        .staffs_service[k]
                                                        .relevant === true
                                            )
                                        ) {
                                            for (
                                                var z = 0;
                                                z < this.staffs;
                                                z++
                                            ) {
                                                if (
                                                    this.staffs[z].staff ==
                                                    res.data[t].risks_incident[
                                                        i
                                                    ].services_offered_risk[j]
                                                        .staffs_service[k].staff
                                                ) {
                                                    this.staffs[z] =
                                                        objArr.slice(0, z);
                                                    this.staffs.push(
                                                        res.data[t]
                                                            .risks_incident[i]
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
                    }

                    //Eliminar repetidos de la lista completa de staff
                    const uniqueIds = [];

                    const staffsNoRepeated = this.staffsComplete.filter(
                        (element) => {
                            const isDuplicate = uniqueIds.includes(element.id);

                            if (!isDuplicate) {
                                uniqueIds.push(element.id);

                                return true;
                            }

                            return false;
                        }
                    );
                    this.staffsComplete = staffsNoRepeated;
                    /*
                    console.log("Servicios de la organización:");
                    console.log(this.servicesOffered);
                    console.log("Staffs:");
                    console.log(this.staffs);
                    console.log("RTO de los servicios");
                    console.log(this.servicesByRTO);
                    */
                    this.countStaffsArea();
                    this.loadingServicesOffered = true;

                    this.countServicesMinimumRTO();
                    this.loadingServicesOnlyMinimumRTO = true;
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
                    `${SERVER_ADDRESS}/api/phase3/incident-history/services-used/all/`,
                    {
                        params: {
                            start_date: this.incidentDateFilter.start_date,
                            end_date: this.incidentDateFilter.end_date,
                        },
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    for (var t = 0; t < res.data.length; t++) {
                        for (
                            var i = 0;
                            i < res.data[t].risks_incident.length;
                            i++
                        ) {
                            for (
                                var j = 0;
                                j <
                                res.data[t].risks_incident[i].services_used_risk
                                    .length;
                                j++
                            ) {
                                if (
                                    !this.servicesUsed.find(
                                        (k) =>
                                            k.id ===
                                            res.data[t].risks_incident[i]
                                                .services_used_risk[j].id
                                    )
                                ) {
                                    this.servicesUsed.push(
                                        res.data[t].risks_incident[i]
                                            .services_used_risk[j]
                                    );
                                    /**
                                     * Variables para la gráfica
                                     */
                                    this.chartOptionsServicesUsed.xaxis.categories.push(
                                        res.data[t].risks_incident[i]
                                            .services_used_risk[j].name
                                    );
                                    this.seriesServicesUsed[0].data.push(
                                        res.data[t].risks_incident[i]
                                            .services_used_risk[j].criticality
                                    );
                                }
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
                    `${SERVER_ADDRESS}/api/phase3/incident-history/organization-activities/all/`,
                    {
                        params: {
                            start_date: this.incidentDateFilter.start_date,
                            end_date: this.incidentDateFilter.end_date,
                        },
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    for (var t = 0; t < res.data.length; t++) {
                        for (
                            var i = 0;
                            i < res.data[t].risks_incident.length;
                            i++
                        ) {
                            for (
                                var j = 0;
                                j <
                                res.data[t].risks_incident[i]
                                    .organization_activities_risk.length;
                                j++
                            ) {
                                if (
                                    !this.organizationActivities.find(
                                        (k) =>
                                            k.id ===
                                            res.data[t].risks_incident[i]
                                                .organization_activities_risk[j]
                                                .id
                                    )
                                ) {
                                    this.organizationActivities.push(
                                        res.data[t].risks_incident[i]
                                            .organization_activities_risk[j]
                                    );
                                    /**
                                     * Variables para la gráfica
                                     */
                                    this.chartOptionsOrgActivities.xaxis.categories.push(
                                        res.data[t].risks_incident[i]
                                            .organization_activities_risk[j]
                                            .name
                                    );
                                    this.seriesOrgActivities[0].data.push(
                                        res.data[t].risks_incident[i]
                                            .organization_activities_risk[j]
                                            .criticality
                                    );
                                }
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
