<template>
    <div class="container-fluid">
        <h2>Servicios usados</h2>
    </div>
</template>
<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import { FilterMatchMode } from "primevue/api";

import Multiselect from "vue-multiselect";
import NotificationTemplate from "../Notifications/NotificationTemplate";

export default {
    name: "ServicesUsed",
    components: {
        Multiselect,
    },
    data: () => ({
        loading: false,
        filterGlobal: null,
    }),
    mounted() {},
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

        /**
         * Filtros que se manejan en Prime Vue
         */
        clearFilter1() {
            this.initFilters1();
        },
        initFilters1() {
            this.filterGlobal = {
                value: null,
                matchMode: FilterMatchMode.CONTAINS,
            };
        },
    },
};
</script>
<style lang="scss">
</style>
