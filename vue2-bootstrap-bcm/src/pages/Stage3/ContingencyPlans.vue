<template>
    <div class="container-fluid">
        <b-row align-v="center">
            <h4>Planes de contingencia</h4>
        </b-row>
        <b-row align-v="center">
            <b-col>
                <b-row align-v="center">
                    <button type="button" @click="addNode">Add</button>
                    <button type="button" @click="$refs.chart.remove()">
                        Del
                    </button>
                    <button type="button" @click="$refs.chart.editCurrent()">
                        Edit
                    </button>
                    <button type="button" @click="$refs.chart.save()">
                        Save
                    </button>
                    <button
                        type="button"
                        v-if="showRemovingConfirmation"
                        @click="confirmRemoving"
                    >
                        Confirm removing
                    </button>
                    <button
                        type="button"
                        v-if="showRemovingConfirmation"
                        @click="showRemovingConfirmation = false"
                    >
                        Reject removing
                    </button>
                </b-row>
                <b-row align-v="center">
                    <flowchart
                        width="1500"
                        height="1000"
                        :nodes="nodes"
                        :connections="connections"
                        :remove-requires-confirmation="true"
                        @editnode="handleEditNode"
                        @dblclick="handleDblClick"
                        @editconnection="handleEditConnection"
                        @removeconfirmationrequired="initRemovingConfirmation"
                        @save="handleChartSave"
                        ref="chart"
                        class="chart"
                    >
                    </flowchart>
                </b-row>
            </b-col>
        </b-row>
    </div>
</template>


<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import NotificationTemplate from "../Notifications/NotificationTemplate";
import FlowChart from "flowchart-vue";

export default {
    name: "ContingencyPlans",
    components: {},
    data: () => ({
        permissions: [],
        is_superuser: false,

        nodes: [
            // Basic fields
            { id: 1, x: 140, y: 270, name: "Start", type: "start" },
            // You can add any generic fields to node, for example: description
            // It will be passed to @save, @editnode
            {
                id: 2,
                x: 540,
                y: 270,
                name: "End",
                type: "end",
            },
            {
                id: 3,
                x: 340,
                y: 270,
                name: "Opción A",
                type: "operation",
                description: "I'm here",
                approvers: [{ name: "Joyce" }, { name: "Alan" }],
            },
            {
                id: 4,
                x: 340,
                y: 360,
                name: "Opción B",
                type: "operation",
                description: "I'm here",
                approvers: [{ name: "Emma" }],
            },
        ],
        connections: [
            {
                source: { id: 1, position: "right" },
                destination: { id: 3, position: "left" },
                id: 1,
                type: "pass",
            },
            {
                source: { id: 1, position: "right" },
                destination: { id: 4, position: "left" },
                id: 1,
                type: "pass",
            },
            {
                source: { id: 3, position: "right" },
                destination: { id: 2, position: "left" },
                id: 2,
                type: "pass",
            },
            {
                source: { id: 4, position: "right" },
                destination: { id: 2, position: "left" },
                id: 2,
                type: "pass",
            },
        ],
        showRemovingConfirmation: false,
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

        handleChartSave(nodes, connections) {
            // axios.post(url, {nodes, connections}).then(resp => {
            //   this.nodes = resp.data.nodes;
            //   this.connections = resp.data.connections;
            //   // Flowchart will refresh after this.nodes and this.connections changed
            // });
        },
        addNode() {
            this.$refs.chart.add({
                id: +new Date(),
                x: 10,
                y: 10,
                name: "New",
                type: "operation",
                approvers: [],
            });
            console.log("Nodes");
            console.log(this.nodes);
            console.log("Connections");
            console.log(this.connections);
        },
        handleEditNode(node) {
            if (node.id === 2) {
                console.log(node.description);
            }
        },
        handleEditConnection(connection) {},
        handleDblClick(position) {
            this.$refs.chart.add({
                id: +new Date(),
                x: position.x,
                y: position.y,
                name: "New",
                type: "operation",
                approvers: [],
            });
        },
        initRemovingConfirmation() {
            this.showRemovingConfirmation = true;
        },
        confirmRemoving() {
            this.$refs.chart.confirmRemove();
            this.showRemovingConfirmation = false;
        },
    },
};
</script>
<style lang="scss">
.chart {
    overflow: auto;
    width: "100%";
}
</style>

