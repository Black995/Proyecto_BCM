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
                        :height="heightServicesOfferedHeatmap"
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
        heightServicesOfferedHeatmap: 50,
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
                                color: "#18a350",
                            },
                            {
                                from: 1,
                                to: 2,
                                name: "medio",
                                color: "#F4D03F",
                            },
                            {
                                from: 3,
                                to: 4,
                                name: "alto",
                                color: "#f38d30",
                            },
                            {
                                from: 5,
                                to: 6,
                                name: "extremo",
                                color: "#df3447",
                            },
                        ],
                    },
                },
            },
            xaxis: {
                labels: {
                    formatter: function (value) {
                        return "Criticidad " + value;
                    },
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
                icon: "ti-close",
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

                    // A la altura del mapa de calor le sumamos 50 por cada riesgo
                    this.heightServicesOfferedHeatmap =
                        this.heightServicesOfferedHeatmap +
                        this.risks.length * 50;

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
                        this.chartOptionsServicesOffered.labels.push(i);
                    }

                    for (var i = 0; i < this.risks.length; i++) {
                        let obj = {
                            name: this.risks[i].name,
                            data: [],
                        };

                        // Le vamos agregando ceros al array de obj.data para que
                        // luego se le vaya sumando a los valores que sean necesarios
                        for (var j = min_value; j <= max_value; j++) {
                            obj.data.push(0);
                        }

                        this.seriesServicesOffered.push(obj);
                    }

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
                    for (var i = 0; i < res.data.length; i++) {
                        // Doble ciclo para el array de las series
                        for (
                            var x = 0;
                            x < this.seriesServicesOffered.length;
                            x++
                        ) {
                            if (
                                this.seriesServicesOffered[x].name ==
                                res.data[i].name
                            ) {
                                for (
                                    var j = 0;
                                    j <
                                    res.data[i].services_offered_risk.length;
                                    j++
                                ) {
                                    for (
                                        var y = 0;
                                        y <
                                        this.chartOptionsServicesOffered.labels
                                            .length;
                                        y++
                                    ) {
                                        if (
                                            this.chartOptionsServicesOffered
                                                .labels[y] ==
                                            res.data[i].services_offered_risk[j]
                                                .criticality
                                        ) {
                                            this.seriesServicesOffered[x].data[
                                                y
                                            ]++;
                                            break;
                                        }
                                    }
                                }
                            }
                        }
                    }
                    //console.log("SERIES SUMADAS");
                    //console.log(this.seriesServicesOffered);

                    this.getHeatmapColorSeparation(
                        this.seriesServicesOffered,
                        1
                    );

                    this.servicesOfferedRisks = res.data;
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
        getHeatmapColorSeparation(series, type) {
            /**
             * Types:
             * 1 -> Services Offered
             * 2 -> Services Used
             * 3 -> Organizacion Activities
             */

            // Variable a utilizar para definir la máxima cantidad de elementos que puede
            // existir en un cuadro
            let max_quantity = 0;
            for (var i = 0; i < series.length; i++) {
                for (var j = 0; j < series[i].data.length; j++) {
                    if (series[i].data[j] > max_quantity) {
                        max_quantity = series[i].data[j];
                    }
                }
            }

            /**
             * Separamos en 4 partes las cantidad de elementos para los colores de las filas
             */
            let base_1_4 = Math.round(max_quantity / 4);
            let base_1_2 = Math.round(max_quantity / 2);
            let base_3_4 = Math.round((max_quantity * 3) / 4);

            if (type == 1) {
                this.chartOptionsServicesOffered.plotOptions.heatmap.colorScale.ranges[0].from = 0;
                this.chartOptionsServicesOffered.plotOptions.heatmap.colorScale.ranges[0].to =
                    base_1_4 - 1;
                this.chartOptionsServicesOffered.plotOptions.heatmap.colorScale.ranges[1].from =
                    base_1_4;
                this.chartOptionsServicesOffered.plotOptions.heatmap.colorScale.ranges[1].to =
                    base_1_2 - 1;
                this.chartOptionsServicesOffered.plotOptions.heatmap.colorScale.ranges[2].from =
                    base_1_2;
                this.chartOptionsServicesOffered.plotOptions.heatmap.colorScale.ranges[2].to =
                    base_3_4 - 1;
                this.chartOptionsServicesOffered.plotOptions.heatmap.colorScale.ranges[3].from =
                    base_3_4;
                this.chartOptionsServicesOffered.plotOptions.heatmap.colorScale.ranges[3].to =
                    max_quantity;
                this.loadingServicesOffered = true;
            }
        },
    },
};
</script>
<style lang="scss">
</style>
