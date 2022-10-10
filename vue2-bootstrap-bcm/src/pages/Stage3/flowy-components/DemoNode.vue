<template>
    <b-card flat bordered class="my-card bg-white q-pa-md">
        <div class="row items-center no-wrap">
            <div class="col">
                <div class="text-h6">{{ title }}</div>
            </div>

            <div class="col-auto">
                <flowy-drag-handle>
                    <b-button variant="light">
                        <b-icon-justify></b-icon-justify>
                    </b-button>
                </flowy-drag-handle>
            </div>
        </div>

        <div class="q-py-md" v-html="description" />
        <b-button variant="primary" @click="remove()">Remove</b-button>
    </b-card>
</template>


<script lang="ts">
import Vue from "vue";

export default Vue.extend({
    name: "demo-node",
    props: ["remove", "node", "title", "description"],
    data: () => ({}),
});
</script>
<style lang="scss">
.flowy-drag-handle button {
    cursor: grab;
}

.flowy-block.draggable-mirror {
    opacity: 0.6;
}
</style>
