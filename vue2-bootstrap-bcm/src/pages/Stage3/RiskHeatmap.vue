<template>
    <div class="container-fluid">
        <b-row class="mt-3" align-v="center">
            <b-col>
                <h5 class="text-center">
                    Cantidad de servicios afectados por los riesgos de acuerdo a
                    la criticidad
                </h5>
                <div v-if="loadingServicesOffered" id="services-offered">
                    <apexchart
                        type="heatmap"
                        height="350"
                        :options="chartOptionsServicesOffered"
                        :series="seriesServicesOffered"
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
    name: "RiskHeatmap",
    components: {
        VueApexCharts,
    },
    data: () => ({
        permissions: [],
        is_superuser: false,

        loadingServicesOffered: false,
        risks: [],
        servicesOfferedRisks: [],

        /*
        seriesServicesOffered: [
            {
                name: "Jan",
                data: [5, 9, 29, -4, -3],
            },
            {
                name: "Feb",
                data: [15, 19, 9, -6, 30],
            },
            {
                name: "Mar",
                data: [-15, 7, 29, 1, 11],
            },
        ],
        */
        maxValueServiceOfferedScale: 0,
        seriesServicesOffered: [],
        chartOptionsServicesOffered: {
            chart: {
                id: "services-offered",
                height: 350,
                type: "heatmap",
            },
            labels: [],
            plotOptions: {
                heatmap: {
                    shadeIntensity: 0.5,
                    radius: 0,
                    useFillColorAsStroke: true,
                    colorScale: {
                        ranges: [
                            {
                                from: 0,
                                to: 0,
                                name: "bajo",
                                color: "#00A100",
                            },
                            {
                                from: 1,
                                to: 2,
                                name: "medio",
                                color: "#128FD9",
                            },
                            {
                                from: 3,
                                to: 4,
                                name: "alto",
                                color: "#FFB200",
                            },
                            {
                                from: 5,
                                to: 6,
                                name: "extremo",
                                color: "#FF0000",
                            },
                        ],
                    },
                },
            },
            /*
            yaxis: {
                labels: {
                    formatter: function (value) {
                        return "Criticidad " + value;
                    },
                },
            },
            */
            xaxis: {
                labels: {
                    rotateAlways: true,
                },
            },
            dataLabels: {
                enabled: false,
                /*
                formatter: function (value) {
                    return "Criticidad " + value;
                },
            */
            },
            stroke: {
                width: 1,
            },
            /*
            title: {
                text: "HeatMap Chart with Color Range",
            },
            */
        },
    }),
    mounted() {
        this.permissions = JSON.parse(localStorage.getItem("permissions"));
        this.is_superuser = localStorage.getItem("is_superuser");
        /**
         * Llamamos a los métodos que tienen las escalas de las vistas
         */
        this.getRisks();
        //this.getServiceOfferedScale();
        //this.getServiceUsedScale();
        //this.getOrgActivitiesScale();
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
        async getRisks() {
            this.risks = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase1/risks/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.risks = res.data;
                    for (var i = 0; i < res.data.length; i++) {
                        this.chartOptionsServicesOffered.labels.push(
                            res.data[i].name
                        );
                    }
                    // Ahora llamamos al servicio que se seleccionó
                    this.getServiceOfferedScale();
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
                    let min_value = parseInt(res.data[0].scale_min_value);
                    let max_value = parseInt(res.data[0].scale_max_value);
                    this.maxValueServiceOfferedScale = max_value;

                    for (var i = min_value; i <= max_value; i++) {
                        let obj = {
                            name: i,
                            data: [],
                        };

                        // Le vamos agregando ceros al array de obj.data para que
                        // luego se le vaya sumando a los valores que sean necesarios
                        for (var j = 0; j < this.risks.length; j++) {
                            obj.data.push(0);
                        }

                        this.seriesServicesOffered.push(obj);
                    }

                    //console.log("Lista de series");
                    //console.log(this.seriesServicesOffered);

                    this.getServicesOfferedRisks();
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
        getServicesOfferedRisks() {
            this.loadingServicesOffered = false;
            this.servicesOfferedRisks = [];

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase1/service_offered_risks_list/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    // Doble ciclo para la información del request
                    for (var i = 0; i < res.data.length; i++) {
                        for (
                            var j = 0;
                            j < res.data[i].services_offered_risk.length;
                            j++
                        ) {
                            // Doble ciclo para el array de las series
                            for (
                                var x = 0;
                                x < this.seriesServicesOffered.length;
                                x++
                            ) {
                                if (
                                    this.seriesServicesOffered[x].name ==
                                    res.data[i].services_offered_risk[j]
                                        .criticality
                                ) {
                                    this.seriesServicesOffered[x].data[i]++;
                                }
                            }
                        }
                    }
                    console.log("SERIES SUMADAS");
                    console.log(this.seriesServicesOffered);
                    this.servicesOfferedRisks = res.data;
                    this.loadingServicesOffered = true;
                })
                .catch((err) => {
                    console.log("err");
                    console.log(err);
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
