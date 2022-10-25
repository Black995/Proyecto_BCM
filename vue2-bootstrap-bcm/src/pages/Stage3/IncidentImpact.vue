<template>
    <div class="container-fluid">
        <b-row align-v="center">
            <b-col
                ><b-row class="text-center">
                    <b-col>
                        <h4>Gráficas del impacto del incidente</h4>
                    </b-col> </b-row
                ><b-row class="text-right">
                    <b-col>
                        <b-button variant="outline-primary" @click="clearFilter"
                            >Limpiar filtro de las gráficas
                            <b-icon icon="filter"></b-icon></b-button
                    ></b-col> </b-row
                ><b-row v-if="timeNow" class="text-center">
                    <b-col>
                        <h5>
                            <strong>Nota:</strong> como el incidente no posee
                            fecha fin, se utilizó la fecha actual (<strong
                                >tiempo transcurrido:</strong
                            >
                            {{ hoursNow }} horas, {{ minutesNow }} minutos)
                        </h5>
                    </b-col>
                </b-row>
                <b-row v-if="incidentEnded" class="text-center">
                    <b-col>
                        <h5>
                            <strong>Tiempo transcurrido:</strong>
                            {{ hoursNow }} horas, {{ minutesNow }} minutos
                        </h5>
                    </b-col>
                </b-row>
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
                    Filtrar incidentes
                </b-button>
            </b-col>
        </b-row>
        <b-row class="mt-3" align-v="center">
            <b-col>
                <h5>Seleccione una de las incidencias</h5>
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
                <h5
                    v-if="
                        loadingServicesOffered &&
                        loadingServicesUsed &&
                        loadingOrgActivities
                    "
                    class="text-center"
                >
                    Criticidad de los servicios de soporte afectados
                </h5>
                <div
                    v-if="
                        loadingServicesOffered &&
                        loadingServicesUsed &&
                        loadingOrgActivities
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
                        loadingOrgActivities
                    "
                    class="text-center"
                >
                    Criticidad de las actividades del negocio afectadas
                </h5>
                <div
                    v-if="
                        loadingServicesOffered &&
                        loadingServicesUsed &&
                        loadingOrgActivities
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
                        loadingOrgActivities
                    "
                    class="text-center"
                >
                    Criticidad de los servicios de la organización afectados
                </h5>
                <h6
                    v-if="
                        loadingServicesOffered &&
                        loadingServicesUsed &&
                        loadingOrgActivities
                    "
                    class="text-center"
                >
                    <strong>Nota:</strong> seleccione uno de los servicios para
                    poder visualizar el personal afectado por área y los
                    recursos afectados por servicio
                </h6>
                <div
                    v-if="
                        loadingServicesOffered &&
                        loadingServicesUsed &&
                        loadingOrgActivities
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
                        loadingRessources
                    "
                    class="text-center"
                >
                    Cantidad de recursos afectados
                </h5>
                <div
                    v-if="
                        loadingServicesOffered &&
                        loadingServicesUsed &&
                        loadingOrgActivities &&
                        loadingRessources
                    "
                    id="ressources"
                >
                    <apexchart
                        ref="ressources"
                        type="donut"
                        height="500"
                        :options="chartOptionsRessources"
                        :series="seriesRessources"
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
                        loadingServicesOnlyMinimumRTO &&
                        loadingServicesMinimunRTO
                    "
                    class="text-center"
                >
                    Servicios que excedieron el RTO debido a la duración de la
                    incidencia
                </h5>
                <div
                    v-if="
                        loadingServicesOffered &&
                        loadingServicesUsed &&
                        loadingOrgActivities &&
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
                        loadingServicesOnlyMinimumRTO &&
                        loadingServicesMinimunRTO
                    "
                    class="text-center"
                >
                    Servicios que excedieron el RTO debido a la duración de la
                    incidencia
                </h5>
                <div
                    v-if="
                        loadingServicesOffered &&
                        loadingServicesUsed &&
                        loadingOrgActivities &&
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
            <b-col>
                <h5
                    v-if="
                        loadingServicesOffered &&
                        loadingServicesUsed &&
                        loadingOrgActivities &&
                        loadingServicesOnlyMinimumRTO &&
                        loadingServicesMinimunRTO
                    "
                    class="text-center"
                >
                    Servicios que NO excedieron el RTO debido a la duración de
                    la incidencia
                </h5>
                <div
                    v-if="
                        loadingServicesOffered &&
                        loadingServicesUsed &&
                        loadingOrgActivities &&
                        loadingServicesOnlyMinimumRTO &&
                        loadingServicesMinimunRTO
                    "
                    id="services-not-exceed-minimum-rto"
                >
                    <apexchart
                        type="bar"
                        height="500"
                        :options="chartOptionsServicesNotExceedMinimumRTO"
                        :series="seriesServicesNotExceedMinimumRTO"
                    ></apexchart>
                </div>
            </b-col>
        </b-row>
        <b-row class="mt-3" align-v="center">
            <b-col>
                <h5
                    v-if="servicesUsedAffectedByServicesOnlyMinimumRTO.length"
                    class="text-center"
                >
                    Servicios de soporte afectados por los servicios de la
                    organización que excedieron el RTO debido a la duración de
                    la incidencia
                </h5>
                <b-list-group
                    v-if="servicesUsedAffectedByServicesOnlyMinimumRTO.length"
                    class="mt-3"
                >
                    <b-list-group-item
                        class="flex-column align-items-start"
                        v-for="item in servicesUsedAffectedByServicesOnlyMinimumRTO"
                        :key="item.key"
                    >
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">
                                {{ item.name }}
                            </h5>
                            <small class="text-muted"
                                >Tipo de servicio: {{ item.type_name }}
                            </small>
                        </div>
                        <div class="mb-1 d-flex w-100 justify-content-between">
                            <div>
                                Criticidad: {{ item.criticality }}/{{
                                    item.scale_max_value
                                }}
                            </div>
                            <div v-if="item.spending">
                                Costo promedio: {{ item.spending }}$
                            </div>
                            <div v-if="!item.spending">
                                Costo promedio: no aplica
                            </div>
                        </div>
                        <div class="mb-1 d-flex w-100 justify-content-between">
                            <div v-if="item.type == 1">
                                <strong
                                    >Acuerdo de nivel de servicio (SLA): </strong
                                >{{ item.agreement_comment }}
                            </div>
                            <div v-if="item.type == 2">
                                <strong
                                    >Acuerdo de nivel operativo (OLA): </strong
                                >{{ item.agreement_comment }}
                            </div>
                        </div>
                    </b-list-group-item>
                </b-list-group>
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
        apexchart: VueApexCharts,
    },
    data: () => ({
        permissions: [],
        is_superuser: false,

        loadingIncidents: false,
        incidentDateFilter: {
            start_date: "",
            end_date: "",
        },
        incidentDateFilterState: {
            start_date: null,
            end_date: null,
        },

        incidents: [],
        incidentId: 0,

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
        hoursNow: 0,
        minutesNow: 0,
        timeIncident: "",
        servicesByRTO: [],

        timeNow: "",
        incidentEnded: false,

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
        loadingRessources: false,
        seriesRessources: [],
        chartOptionsRessources: {
            chart: {
                id: "ressources",
                height: 200,
                width: 400,
                type: "donut",
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
                text: "No se encontraron recursos asignados para el servicio seleccionado",
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
                name: "RTO",
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
            /**
             * Tooltip -> y
             * permite cambiar el texto en negritas del cuadrito flotante de la gráfica
             */
            tooltip: {
                y: {
                    formatter: function (val) {
                        let hours = 0;
                        let minutes = 0;
                        while (val >= 3600000) {
                            val = val - 3600000;
                            hours++;
                        }
                        while (val >= 60000) {
                            val = val - 60000;
                            minutes++;
                        }

                        let text = "";
                        if (hours != 0) {
                            text = hours + " horas, " + minutes + " minutos";
                        } else {
                            text = minutes + " minutos";
                        }
                        return text;
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
                        let hours = 0;
                        let minutes = 0;
                        while (val >= 3600000) {
                            val = val - 3600000;
                            hours++;
                        }
                        while (val >= 60000) {
                            val = val - 60000;
                            minutes++;
                        }

                        let text = "";
                        if (hours != 0) {
                            text = hours + " horas, " + minutes + " minutos";
                        } else {
                            text = minutes + " minutos";
                        }
                        return text;
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
        seriesServicesNotExceedMinimumRTO: [
            {
                name: "RTO",
                data: [],
            },
        ],
        chartOptionsServicesNotExceedMinimumRTO: {
            chart: {
                id: "services-not-exceed-minimum-rto",
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
            /**
             * Tooltip -> y
             * permite cambiar el texto en negritas del cuadrito flotante de la gráfica
             */
            tooltip: {
                y: {
                    formatter: function (val) {
                        let hours = 0;
                        let minutes = 0;
                        while (val >= 3600000) {
                            val = val - 3600000;
                            hours++;
                        }
                        while (val >= 60000) {
                            val = val - 60000;
                            minutes++;
                        }

                        let text = "";
                        if (hours != 0) {
                            text = hours + " horas, " + minutes + " minutos";
                        } else {
                            text = minutes + " minutos";
                        }
                        return text;
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
                        let hours = 0;
                        let minutes = 0;
                        while (val >= 3600000) {
                            val = val - 3600000;
                            hours++;
                        }
                        while (val >= 60000) {
                            val = val - 60000;
                            minutes++;
                        }

                        let text = "";
                        if (hours != 0) {
                            text = hours + " horas, " + minutes + " minutos";
                        } else {
                            text = minutes + " minutos";
                        }
                        return text;
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
                text: "No se encontraron servicios de la organización que NO excedieran el RTO",
                align: "center",
                verticalAlign: "middle",
                style: {
                    fontSize: "14px",
                },
            },
        },
        servicesUsedAffectedByServicesOnlyMinimumRTO: [],
    }),
    computed: {
        chartOptionsServicesOffered: function () {
            return {
                chart: {
                    id: "services-offered",
                    type: "bar",
                    height: 200,
                    width: 400,
                    events: {
                        dataPointSelection: (event, chartContext, config) => {
                            this.selectServiceOffered(config.dataPointIndex);
                        },
                    },
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
                icon: "ti-close",
                horizontalAlign: "right",
                verticalAlign: "top",
                type: "danger",
            });
        },
        timeNowHoursMinutes(val) {
            this.hoursNow = 0;
            this.minutesNow = 0;
            while (val >= 3600000) {
                val = val - 3600000;
                this.hoursNow++;
            }
            while (val >= 60000) {
                val = val - 60000;
                this.minutesNow++;
            }
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
            this.countRessources(service.id);
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
                this.incidents = [];
                this.loadingIncidents = true;

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
                            let name = "";
                            if (res.data[i].end_date) {
                                name =
                                    res.data[i].crisis_scenario_name +
                                    " (Fecha de inicio: " +
                                    res.data[i].start_date.slice(0, 10) +
                                    " " +
                                    res.data[i].start_date.slice(11, 16) +
                                    " - Fecha fin: " +
                                    res.data[i].end_date.slice(0, 10) +
                                    " " +
                                    res.data[i].end_date.slice(11, 16) +
                                    ")";
                            } else {
                                name =
                                    res.data[i].crisis_scenario_name +
                                    " (Fecha de inicio: " +
                                    res.data[i].start_date.slice(0, 10) +
                                    " " +
                                    res.data[i].start_date.slice(11, 16) +
                                    " - Fecha fin: - )";
                            }
                            let inc = {
                                id: res.data[i].id,
                                name: name,
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
        clearFilter() {
            this.countStaffsArea();
            this.chartOptionsRessources.labels = [""];
            this.seriesRessources = [0];
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

            this.chartOptionsStaffsArea.labels = [];
            this.seriesStaffsArea = [];

            // Ordenamos el array de json por orden alfabético del nombre del área
            this.staffsArea.sort(function (a, b) {
                return a.staff_area_name < b.staff_area_name
                    ? -1
                    : a.staff_area_name > b.staff_area_name
                    ? 1
                    : 0;
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

            // Ordenamos el array de json por orden alfabético del nombre del área
            this.staffsArea.sort(function (a, b) {
                return a.staff_area_name < b.staff_area_name
                    ? -1
                    : a.staff_area_name > b.staff_area_name
                    ? 1
                    : 0;
            });

            for (var i = 0; i < this.staffsArea.length; i++) {
                this.chartOptionsStaffsArea.labels.push(
                    this.staffsArea[i].staff_area_name
                );
                this.seriesStaffsArea.push(this.staffsArea[i].occurrence);
            }

            this.loadingStaffsArea = true;
        },
        /**
         * Manejar lógica de recursos por servicio
         */
        countRessources(serviceId) {
            this.loadingRessources = false;
            let ressources = [];

            for (var i = 0; i < this.servicesOffered.length; i++) {
                if (this.servicesOffered[i].id == serviceId) {
                    this.chartOptionsRessources.labels = [];
                    this.seriesRessources = [];

                    for (
                        var j = 0;
                        j < this.servicesOffered[i].ressources_service.length;
                        j++
                    ) {
                        let objRessource = {
                            label: this.servicesOffered[i].ressources_service[j]
                                .ressource_name,
                            serie: this.servicesOffered[i].ressources_service[j]
                                .amount,
                        };
                        ressources.push(objRessource);
                    }
                    break;
                }
            }

            // Ordenamos el array de json por orden alfabético del nombre del área
            ressources.sort(function (a, b) {
                return a.label < b.label ? -1 : a.label > b.label ? 1 : 0;
            });
            for (var i = 0; i < ressources.length; i++) {
                this.chartOptionsRessources.labels.push(ressources[i].label);
                this.seriesRessources.push(ressources[i].serie);
            }

            // Si no hay elementos que mostrar en el chart entonces se muestra vacío
            if (!ressources.length) {
                this.chartOptionsRessources.labels = [""];
                this.seriesRessources = [0];
            }

            this.loadingRessources = true;
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
            this.loadingServicesMinimunRTO = false;
            this.loadingServicesOnlyMinimumRTO = false;
            // this.loadingRessources = false;
            this.incidentDurationTime = 0;
            this.timeNow = "";
            this.incidentEnded = false;
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
            this.chartOptionsServicesNotExceedMinimumRTO.xaxis.categories = [];
            this.seriesServicesNotExceedMinimumRTO[0].data = [];
            this.servicesUsedAffectedByServicesOnlyMinimumRTO = [];
            // Reiniciamos mínimo y máximo de las gráficas que manejan RTO
            this.chartOptionsServicesOnlyMinimumRTO.yaxis.min = 0;
            this.chartOptionsServicesOnlyMinimumRTO.yaxis.max = 0;
            this.chartOptionsServicesNotExceedMinimumRTO.yaxis.min = 0;
            this.chartOptionsServicesNotExceedMinimumRTO.yaxis.max = 0;

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
                    let start_date_incident = new Date(
                        res.data.start_date
                    ).getTime();
                    let end_date_incident;

                    if (res.data.end_date) {
                        end_date_incident = new Date(
                            res.data.end_date
                        ).getTime();
                        this.incidentEnded = true;
                    } else {
                        end_date_incident = Date.now();
                        this.timeNow = Date.now();
                    }

                    console.log("HORA INICIO INCIDENTE");
                    console.log(start_date_incident);
                    console.log(res.data.start_date);
                    console.log("HORA FIN DEL INCIDENTE");
                    console.log(Date(Date.now()).toString());
                    console.log(this.timeNow);

                    // Duración del incidente en milisegundos
                    this.incidentDurationTime =
                        end_date_incident - start_date_incident;

                    this.timeNowHoursMinutes(this.incidentDurationTime);
                    // Mínimo tiempo de duración para los servicios que exceden el RTO
                    this.chartOptionsServicesNotExceedMinimumRTO.yaxis.min =
                        this.incidentDurationTime;

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
                                 * Cálculo del RTO del servicio con la duración de
                                 * la incidencia
                                 *
                                 * SÓLO SE APLICA SI EXISTE LA FECHA FINAL DE LA INCIDENCIA
                                 */
                                let exceed_recovery_time = false;
                                let recovery_time_service = 0;
                                if (this.incidentDurationTime) {
                                    let hours = parseInt(
                                        res.data.risks_incident[
                                            i
                                        ].services_offered_risk[
                                            j
                                        ].recovery_time.slice(0, 2)
                                    );
                                    let minutes = parseInt(
                                        res.data.risks_incident[
                                            i
                                        ].services_offered_risk[
                                            j
                                        ].recovery_time.slice(3, 5)
                                    );
                                    recovery_time_service =
                                        hours * 3600000 + minutes * 60000;
                                    if (
                                        recovery_time_service <=
                                        this.incidentDurationTime
                                    ) {
                                        exceed_recovery_time = true;
                                    }
                                    let serviceByRTO = {
                                        id: res.data.risks_incident[i]
                                            .services_offered_risk[j].id,
                                        area_name:
                                            res.data.risks_incident[i]
                                                .services_offered_risk[j]
                                                .area_name,
                                        name: res.data.risks_incident[i]
                                            .services_offered_risk[j].name,
                                        type_name:
                                            res.data.risks_incident[i]
                                                .services_offered_risk[j]
                                                .type_name,
                                        recovery_time: recovery_time_service,
                                        exceed_recovery_time:
                                            exceed_recovery_time,
                                    };
                                    this.servicesByRTO.push(serviceByRTO);
                                }
                                /**
                                 * Variables para la gráfica de servicios de la org.
                                 */
                                this.chartOptionsServicesOffered.xaxis.categories.push(
                                    res.data.risks_incident[i]
                                        .services_offered_risk[j].name
                                );
                                this.seriesServicesOffered[0].data.push(
                                    res.data.risks_incident[i]
                                        .services_offered_risk[j].criticality
                                );
                                /*
                                this.chartOptionsServicesOffered.chart.width =
                                    this.chartOptionsServicesOffered.chart
                                        .width + 100;
                                */
                                /**
                                 * Variables para la gráfica de servicios que exceden el RTO
                                 */
                                if (exceed_recovery_time) {
                                    this.chartOptionsServicesOnlyMinimumRTO.xaxis.categories.push(
                                        res.data.risks_incident[i]
                                            .services_offered_risk[j].name
                                    );
                                    this.seriesServicesOnlyMinimumRTO[0].data.push(
                                        recovery_time_service
                                    );

                                    /**
                                     * Máximo valor es el tiempo del RTO excedido
                                     */
                                    this.chartOptionsServicesOnlyMinimumRTO.yaxis.max =
                                        this.incidentDurationTime;

                                    /**
                                     * Se agregan los servicios de soporte afectados por servicios de la org.
                                     */
                                    for (
                                        var t = 0;
                                        t <
                                        res.data.risks_incident[i]
                                            .services_offered_risk[j]
                                            .service_offered_service_used
                                            .length;
                                        t++
                                    ) {
                                        // En caso de que no esté el objeto en el array
                                        if (
                                            !this.servicesUsedAffectedByServicesOnlyMinimumRTO.find(
                                                (x) =>
                                                    x.id ===
                                                    res.data.risks_incident[i]
                                                        .services_offered_risk[
                                                        j
                                                    ]
                                                        .service_offered_service_used[
                                                        t
                                                    ].id
                                            )
                                        ) {
                                            this.servicesUsedAffectedByServicesOnlyMinimumRTO.push(
                                                res.data.risks_incident[i]
                                                    .services_offered_risk[j]
                                                    .service_offered_service_used[
                                                    t
                                                ]
                                            );
                                        }
                                    }
                                } else {
                                    /**
                                     * Para el caso de los servicios que no excedieron RTO
                                     */
                                    this.chartOptionsServicesNotExceedMinimumRTO.xaxis.categories.push(
                                        res.data.risks_incident[i]
                                            .services_offered_risk[j].name
                                    );
                                    this.seriesServicesNotExceedMinimumRTO[0].data.push(
                                        recovery_time_service
                                    );
                                    /**
                                     * Mientras más valores vamos insertando en el tiempo,
                                     * Vamos actualizando el RTO más alto
                                     */
                                    if (
                                        this
                                            .chartOptionsServicesNotExceedMinimumRTO
                                            .yaxis.max < recovery_time_service
                                    ) {
                                        this.chartOptionsServicesNotExceedMinimumRTO.yaxis.max =
                                            recovery_time_service;
                                    }
                                }
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
                                // Array de staffs para tenerlos todos por servicio
                                this.staffsComplete.push(
                                    res.data.risks_incident[i]
                                        .services_offered_risk[j]
                                        .staffs_service[k]
                                );

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

                    //console.log("Servicios de la organización:");
                    //console.log(this.servicesOffered);
                    //console.log("Staffs:");
                    //console.log(this.staffs);
                    //console.log("RTO de los servicios");
                    //console.log(this.servicesByRTO);

                    this.countStaffsArea();
                    this.loadingServicesOffered = true;

                    if (this.incidentDurationTime) {
                        this.countServicesMinimumRTO();
                        this.loadingServicesOnlyMinimumRTO = true;
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
.chart {
    overflow: auto;
    width: "100%";
}
</style>
