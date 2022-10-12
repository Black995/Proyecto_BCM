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
                        <button
                            @click="deleteNotification(item.id)"
                            type="button"
                            aria-hidden="true"
                            class="close"
                        >
                            ×
                        </button>
                        <span>
                            <b> {{ item.title }} </b> {{ item.description }}
                        </span>
                    </div>
                    <div v-if="item.type == 2" class="alert alert-warning">
                        <button
                            @click="deleteNotification(item.id)"
                            type="button"
                            aria-hidden="true"
                            class="close"
                        >
                            ×
                        </button>
                        <span>
                            <b> {{ item.title }} </b> {{ item.description }}
                        </span>
                    </div>
                    <div v-if="item.type == 3" class="alert alert-danger">
                        <button
                            @click="deleteNotification(item.id)"
                            type="button"
                            aria-hidden="true"
                            class="close"
                        >
                            ×
                        </button>
                        <span>
                            <b> {{ item.title }} </b> {{ item.description }}
                        </span>
                    </div>
                </div>
            </b-col>
        </b-row>
    </card>
</template>

<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";

export default {
    name: "notification",

    data: () => ({
        loading: false,

        notifications: [
            {
                id: 1,
                title: "Notificación 1",
                description: "Se le informa que esto es una notificación",
                type: 1,
            },
            {
                id: 2,
                title: "Notificación 2",
                description: "Se le informa que esto es una notificación",
                type: 2,
            },
            {
                id: 3,
                title: "Notificación 3",
                description: "Se le informa que esto es una notificación",
                type: 3,
            },
        ],
        notificationId: 0,
    }),
    mounted() {
        // this.getNotifications();
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
                .get(`${SERVER_ADDRESS}/api/config/areas/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.notifications = res.data;
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
};
</script>
