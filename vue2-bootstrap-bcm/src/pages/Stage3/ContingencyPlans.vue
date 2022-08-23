<template>
    <div class="container-fluid">
        <h4>Planes de contingencia</h4>
    </div>
</template>


<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import { FilterMatchMode } from "primevue/api";
import NotificationTemplate from "../Notifications/NotificationTemplate";

export default {
    name: "IncidentHistory",
    components: {},
    data: () => ({
        permissions: [],
        is_superuser: false,
    }),
    mounted() {
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
                icon: "ti-close",
                horizontalAlign: "right",
                verticalAlign: "top",
                type: "danger",
            });
        },
    },
};
</script>
<style lang="scss">
</style>

