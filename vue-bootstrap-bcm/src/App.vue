<template>
    <div>
        <div class="v-application">
            <router-view />
        </div>
    </div>
</template>

<script lang="ts">
import Vue from "vue";

export default Vue.extend({
    name: "App",
});
</script>

<style lang="scss">
@import url("https://fonts.googleapis.com/css2?family=Varta:wght@600&display=swap");

$font-family: "Varta";

html {
    background: #f1f1f1;
}

.v-application {
    font-family: $font-family;
}
</style>