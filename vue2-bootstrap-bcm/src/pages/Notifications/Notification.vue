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
                    <div
                        v-if="item.notification_type == 1"
                        class="alert alert-info"
                    >
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">
                                <strong>{{ item.notification_title }}</strong>
                            </h5>
                            <p v-if="item.notification_days == 1">
                                {{ item.date_day }} {{ item.date_time }} (hace
                                {{ item.notification_days }} día)
                            </p>
                            <p v-if="item.notification_days != 1">
                                {{ item.date_day }} {{ item.date_time }} (hace
                                {{ item.notification_days }} días)
                            </p>
                        </div>
                        <div class="d-flex w-100 justify-content-between">
                            <p class="mb-1">
                                {{ item.notification_description }}
                            </p>
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
                    <div
                        v-if="item.notification_type == 2"
                        class="alert alert-warning"
                    >
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">
                                <strong>{{ item.notification_title }}</strong>
                            </h5>
                            <p v-if="item.notification_days == 1">
                                {{ item.date_day }} {{ item.date_time }} (hace
                                {{ item.notification_days }} día)
                            </p>
                            <p v-if="item.notification_days != 1">
                                {{ item.date_day }} {{ item.date_time }} (hace
                                {{ item.notification_days }} días)
                            </p>
                        </div>
                        <div class="d-flex w-100 justify-content-between">
                            <p class="mb-1">
                                {{ item.notification_description }}
                            </p>
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
                    <div
                        v-if="item.notification_type == 3"
                        class="alert alert-danger"
                    >
                        <div class="d-flex w-100 justify-content-between">
                            <h5 class="mb-1">
                                <strong>{{ item.notification_title }}</strong>
                            </h5>
                            <p v-if="item.notification_days == 1">
                                {{ item.date_day }} {{ item.date_time }} (hace
                                {{ item.notification_days }} día)
                            </p>
                            <p v-if="item.notification_days != 1">
                                {{ item.date_day }} {{ item.date_time }} (hace
                                {{ item.notification_days }} días)
                            </p>
                        </div>
                        <div class="d-flex w-100 justify-content-between">
                            <p class="mb-1">
                                {{ item.notification_description }}
                            </p>
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
                <div
                    v-if="!loading && notifications.length == 0"
                    class="text-center"
                >
                    <h5>¡No posee notificaciones pendientes!</h5>
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
                .get(`${SERVER_ADDRESS}/api/notifications/notifications/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for (var i = 0; i < res.data.length; i++) {
                        // Separamos la duración en día y hora
                        res.data[i].date_day = res.data[
                            i
                        ].notification_date.slice(0, 10);
                        res.data[i].date_time = res.data[
                            i
                        ].notification_date.slice(11, 16);
                        this.notifications.push(res.data[i]);
                    }

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
            let notificationRead = {
                read: true,
            };
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/notifications/notification/${id}/`,
                    notificationRead,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    for (let i = 0; i < this.notifications.length; i++) {
                        if (this.notifications[i].id == id) {
                            this.notifications.splice(i, 1);
                            break;
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
    async destroyed() {
        axios
            .get(`${SERVER_ADDRESS}/api/notifications/unread_notifications/`, {
                withCredentials: true,
                headers: {
                    Authorization: TOKEN,
                },
            })
            .then((res) => {
                if (res.data <= 9) {
                    this.$store.commit("changenumberNotif", res.data);
                } else {
                    this.$store.commit("changenumberNotif", "+9");
                }
            })
            .catch((err) => {
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
