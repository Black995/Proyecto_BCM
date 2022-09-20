<template>
    <b-card
        flat
        bordered
        class="q-px-md q-py-sm row items-center justify-between"
    >
        <div class="text-subtitle1">{{ title }}</div>
        <flowy-drag-handle>
            <b-button variant="light">
                <b-icon-justify></b-icon-justify>
            </b-button>
        </flowy-drag-handle>
    </b-card>
</template>


<script lang="ts">
import Vue from "vue";

export default Vue.extend({
    name: "demo-block",
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
