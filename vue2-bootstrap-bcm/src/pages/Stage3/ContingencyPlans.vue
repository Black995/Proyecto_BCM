<template>
    <div>
        <b-row class="mt-3" align-v="center">
            <b-col>
                <h5>Seleccione una de las incidencias</h5>
                <div class="text-center">
                    <b-spinner v-if="loadingIncidents" type="grow"></b-spinner>
                    <b-form-select
                        v-if="!loadingIncidents"
                        v-model="incidentId"
                        :options="incidents"
                        value-field="id"
                        text-field="name"
                        label="Incidencias"
                    ></b-form-select>
                </div>
            </b-col>
        </b-row>
        <b-row align-v="center" class="mt-5">
            <b-col>
                <b-row>
                    <b-col cols="9">
                        <h5 class="text-center">
                            Arrastre bloques al árbol de nodos debajo usando el
                            botón de hamburguesa
                        </h5>
                    </b-col>
                    <b-col cols="3">
                        <div class="w-100">
                            <b-button
                                variant="warning"
                                class="float-right"
                                @click="editMainBlock = !editMainBlock"
                            >
                                Editar bloque principal
                            </b-button>
                        </div>
                    </b-col>
                </b-row>
                <b-row v-if="editMainBlock" align-v="center">
                    <b-col>
                        <b-form-group
                            label="Ingrese el título del bloque"
                            invalid-feedback="Este campo es obligatorio"
                            :state="blockState.title"
                        >
                            <b-form-input
                                v-model="block.preview.title"
                                :state="blockState.title"
                                required
                            ></b-form-input>
                        </b-form-group>
                        <b-form-group
                            label="Ingrese la descripción del bloque"
                            invalid-feedback="Este campo es obligatorio"
                            :state="blockState.description"
                        >
                            <b-form-textarea
                                v-model="block.node.description"
                                :state="blockState.description"
                                required
                                rows="3"
                            ></b-form-textarea>
                        </b-form-group>
                    </b-col>
                </b-row>

                <b-row align-v="center">
                    <b-col>
                        <div class="d-flex justify-content-center">
                            <!--flowy-new-block
                                v-for="(block, index) in blocks"
                                :key="index"
                                @drag-start="onDragStartNewBlock"
                                @drag-stop="onDragStopNewBlock"
                            -->
                            <flowy-new-block
                                @drag-start="onDragStartNewBlock"
                                @drag-stop="onDragStopNewBlock"
                            >
                                <template v-slot:preview="{}">
                                    <demo-block
                                        :title="block.preview.title"
                                        :description="block.preview.description"
                                    />
                                </template>
                                <template v-slot:node="{}">
                                    <demo-node
                                        :title="block.node.title"
                                        :description="block.node.description"
                                        :custom-attribute="
                                            block.node.canBeAdded
                                        "
                                    />
                                </template>
                            </flowy-new-block>
                        </div>
                    </b-col>
                </b-row>

                <b-row align-v="center">
                    <flowy
                        :nodes="nodes"
                        :beforeMove="beforeMove"
                        :beforeAdd="beforeAdd"
                        @add="add"
                        @move="move"
                        @remove="remove"
                        @drag-start="onDragStart"
                    ></flowy>
                </b-row>
            </b-col>
        </b-row>
    </div>
</template>


<script>
import Vue from "vue";
import _ from "lodash";
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import NotificationTemplate from "../Notifications/NotificationTemplate";
import DemoBlock from "./flowy-components/DemoBlock.vue";
//import DemoNode from "./flowy-components/DemoNode.vue";

const DemoNode = {
    data() {
        return {
            text: "This is component A",
        };
    },
    props: ["remove", "node", "title", "description"],
    template: `
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
  `,
};

Vue.component("demo-node", DemoNode);

export default {
    name: "ContingencyPlans",
    components: {
        DemoBlock,
        DemoNode,
    },
    data: () => ({
        permissions: [],
        is_superuser: false,

        loadingIncidents: false,

        incidents: [],
        incidentId: 0,

        editMainBlock: false,
        blockState: {
            title: null,
            description: null,
        },

        dragging: false,
        block: {
            preview: {
                title: "Nuevo paso a ingresar",
            },
            node: {
                title: "asd",
                description: "asdaswqbv3b34ojin",
            },
        },
        /*
        {
            preview: {
                title: "Cannot be added",
            },
            node: {
                title: "Time has passed",
                description:
                    "Triggers after a specified <b>amount</b> of time",
                canBeAdded: false,
            },
        },
        */
        nodes: [
            {
                id: "1",
                parentId: -1,
                nodeComponent: "demo-node",
                data: {
                    text: "Parent block",
                    title: "Paso 1",
                    description: "Primer paso del plan de contingencia",
                },
            },
            {
                id: "2",
                parentId: "1",
                nodeComponent: "demo-node",
                data: {
                    text: "Parent block",
                    title: "Paso 1.1",
                    description: "Paso 1.1 del plan de contingencia",
                },
            },
            /*
            {
                id: "3",
                parentId: "1",
                nodeComponent: "demo-node",
                data: {
                    text: "Parent block",
                    title: "New Visitor",
                    description:
                        "<span>When a <b>new visitor</b> goes to <i>Site 1</i></span>",
                },
            },
            */
        ],
    }),
    mounted() {
        this.permissions = JSON.parse(localStorage.getItem("permissions"));
        this.is_superuser = localStorage.getItem("is_superuser");

        // Inicializamos diagrama
        //this.initDiagram();
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

        onDragStartNewBlock(event) {
            console.log("onDragStartNewBlock", event);
            // contains all the props and attributes passed to demo-node
            const { props } = event;
            this.newDraggingBlock = props;
        },
        onDragStopNewBlock(event) {
            console.log("onDragStopNewBlock", event);
            this.newDraggingBlock = null;
        },
        // REQUIRED
        beforeMove({ to, from }) {
            // called before moving node (during drag and after drag)
            // indicator will turn red when we return false
            // from is null when we're not dragging from the current node tree
            console.log("beforeMove", to, from);

            // we cannot drag upper parent nodes in this demo
            if (from && from.parentId === -1) {
                return false;
            }
            // we're adding a new node (not moving an existing one)
            if (from === null) {
                // we've passed this attribute to the demo-node
                if (this.newDraggingBlock["custom-attribute"] === false) {
                    return false;
                }
            }

            return true;
        },
        // REQUIRED
        beforeAdd({ to, from }) {
            // called before moving node (during drag and after drag)
            // indicator will turn red when we return false
            // from is null when we're not dragging from the current node tree
            console.log("beforeAdd", to, from);

            /*
            // Inicializamos variables de estados
            this.blockState.title = null;
            this.blockState.description = null;

            // Exit when the form isn't valid
            if (!this.checkBlockValidity()) {
                return false;
            }
            */

            // we've passed this attribute to the demo-node
            if (this.newDraggingBlock["custom-attribute"] === false) {
                return false;
            }

            console.log("Bloque a ingresar");
            console.log(this.block);

            return true;
        },
        randomInteger() {
            return Math.floor(Math.random() * 10000) + 1;
        },
        generateId(nodes) {
            let id = this.randomInteger();
            // _.find is a lodash function
            while (_.find(nodes, { id }) !== undefined) {
                id = this.randomInteger();
            }
            return id;
        },
        addNode(_event) {
            const id = this.generateId();
            this.nodes.push({
                ..._event.node,
                id,
            });
        },
        remove(event) {
            console.log("remove", event);

            // node we're dragging to
            const { node } = event;

            // we use lodash in this demo to remove node from the array
            const nodeIndex = _.findIndex(this.nodes, { id: node.id });
            this.nodes.splice(nodeIndex, 1);
        },
        move(event) {
            console.log("move", event);

            // node we're dragging to and node we've just dragged
            const { dragged, to } = event;

            // change panentId to id of node we're dragging to
            dragged.parentId = to.id;
        },
        add(event) {
            // every node needs an ID
            const id = this.generateId();

            console.log("ADD NODE");
            console.log(event);
            console.log(event.node);

            // Le asignamos la pre visualización al título
            this.block.node.title = this.block.preview.title;

            // Le agregamos a la variable de evento la información del bloque
            event.node.data.title = this.block.node.title;
            event.node.data.description = this.block.node.description;

            // add to array of nodes
            this.nodes.push({
                id,
                ...event.node,
            });
        },
        onDragStart(event) {
            console.log("onDragStart", event);
            this.dragging = true;
        },

        /**
         * Validar formularios
         */
        checkBlockValidity() {
            let valid = true;
            if (!this.block.preview.title) {
                this.blockState.title = false;
                valid = false;
            }
            if (!this.block.node.description) {
                this.blockState.description = false;
                valid = false;
            }

            return valid;
        },
    },
};
</script>
<style lang="scss">
.chart {
    overflow: auto;
    width: "100%";
}

.gojs-diagram {
    position: relative;
    width: 100%;
    height: 100%;
}

#myDiagramDiv {
    width: 100%;
    height: 500px;
}

.flowy-drag-handle button {
    cursor: grab;
}

.flowy-block.draggable-mirror {
    opacity: 0.6;
}
</style>

