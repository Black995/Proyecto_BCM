<template>
    <card title="Notificaciones pendientes">
        <b-row>
            <b-col>
                <div class="text-center">
                    <b-spinner v-if="loading" type="grow"></b-spinner>
                </div>
                <div
                    class="mt-2 flex-column align-items-start"
                    v-for="item in notifications"
                    :key="item.key"
                >
                    <div v-if="item.type == 1" class="alert alert-info">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">
                                <strong>{{ item.title }}</strong>
                            </h5>
                            <small
                                >{{ item.date }} (hace
                                {{ item.days }} días)</small
                            >
                        </div>
                        <div class="d-flex w-100 justify-content-between">
                            <p class="mb-1">{{ item.description }}</p>
                            <button
                                @click="deleteNotification(item.id)"
                                type="button"
                                aria-hidden="true"
                                class="close"
                            >
                                ×
                            </button>
                        </div>
                    </div>
                    <div v-if="item.type == 2" class="alert alert-warning">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">
                                <strong>{{ item.title }}</strong>
                            </h5>
                            <small
                                >{{ item.date }} (hace
                                {{ item.days }} días)</small
                            >
                        </div>
                        <div class="d-flex w-100 justify-content-between">
                            <p class="mb-1">{{ item.description }}</p>
                            <button
                                @click="deleteNotification(item.id)"
                                type="button"
                                aria-hidden="true"
                                class="close"
                            >
                                ×
                            </button>
                        </div>
                    </div>
                    <div v-if="item.type == 3" class="alert alert-danger">
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">
                                <strong>{{ item.title }}</strong>
                            </h5>
                            <small
                                >{{ item.date }} (hace
                                {{ item.days }} días)</small
                            >
                        </div>
                        <div class="d-flex w-100 justify-content-between">
                            <p class="mb-1">{{ item.description }}</p>
                            <button
                                @click="deleteNotification(item.id)"
                                type="button"
                                aria-hidden="true"
                                class="close"
                            >
                                ×
                            </button>
                        </div>
                    </div>
                </div>
            </b-col>
        </b-row>
    </card>
</template>

<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import NotificationTemplate from "./NotificationTemplate";
import {
    getRecoveryTimeText,
    getRecoveryTime,
    setRecoveryTime,
} from "../../helpers/helpers";

export default {
    name: "notification",

    data: () => ({
        loading: false,

        notifications: [],
        notificationId: 0,
    }),
    mounted() {
        this.getNotifications();
    },
    methods: {
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

        async getNotifications() {
            this.loading = true;
            this.notifications = [];

            axios
                .get(`${SERVER_ADDRESS}/api/notifications/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for (var i = 0; i < res.data.length; i++) {
                        //Convertimos en texto la duración
                        res.data[i].date = getRecoveryTimeText(
                            res.data[i].date
                        );
                        this.notifications.push(res.data[i]);
                    }

                    console.log("Notificaciones");
                    console.log(this.notifications);

                    this.loading = false;
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
        deleteNotification(id) {
            for (let i = 0; i < this.notifications.length; i++) {
                if (this.notifications[i].id == id) {
                    this.notifications.splice(i, 1);
                    break;
                }
            }
        },
    },
    async destroyed() {
        console.log("Saliendo de la página de notificaciones");

        axios
            .get(`${SERVER_ADDRESS}/api/notifications/unread_notifications/`, {
                withCredentials: true,
                headers: {
                    Authorization: TOKEN,
                },
            })
            .then((res) => {
                console.log("Cantidad de notificaciones");
                console.log(res);
                console.log(this.$numberNotifications);
                if (res.data <= 9) {
                    this.$changeNumberNotif(res.data);
                    //this.$numberNotifications = res.data;
                } else {
                    this.$changeNumberNotif("+9");
                    //this.$numberNotifications = "+9";
                }
                this.$changeNumberNotif(7);
                console.log(this.$numberNotifications);
            })
            .catch((err) => {
                console.log("err");
                console.log(err);
                try {
                    // Error 400 por unicidad o 500 generico
                    if (err.response.status == 400) {
                        for (let e in err.response.data) {
                            this.errorMessage(e + ": " + err.response.data[e]);
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
};
</script>
