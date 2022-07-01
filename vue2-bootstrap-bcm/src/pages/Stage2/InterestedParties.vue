<template>

</template>

<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import { FilterMatchMode } from "primevue/api";
import Multiselect from "vue-multiselect";
import NotificationTemplate from "../Notifications/NotificationTemplate";
import {
    getRecoveryTimeText,
    getRecoveryTime,
    setRecoveryTime,
} from "../../helpers/helpers";

export default {
    name: "InterestedParties",
    components: {
        Multiselect,
    },
}
</script>

<style lang="scss">
</style>