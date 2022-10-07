<template>
    <div class="container-fluid">
        <b-row class="mt-3" align-v="center">
            <b-col>
                <h5>Seleccione uno de los escenarios críticos</h5>
                <div class="text-center">
                    <b-spinner
                        v-if="loadingCrisisScenarios"
                        type="grow"
                    ></b-spinner>
                    <b-form-select
                        v-if="!loadingCrisisScenarios"
                        v-model="crisisScenarioId"
                        :options="crisisScenarios"
                        value-field="id"
                        text-field="name"
                        label="Escenarios críticos"
                        @change="getContingencyPlanBlockNodes"
                    ></b-form-select>
                </div>
            </b-col>
        </b-row>
        <b-row align-v="center" class="mt-3">
            <b-col>
                <div class="text-center">
                    <b-spinner v-if="loadingNodes" type="grow"></b-spinner>
                </div>
            </b-col>
        </b-row>
        <b-row
            v-if="!loadingNodes && loadingFirstNodes"
            align-v="center"
            class="mt-5"
        >
            <b-col>
                <b-row
                    v-if="
                        is_superuser == true ||
                        permissions.includes(
                            'bcm_phase3.add_contingencyplanblock'
                        )
                    "
                >
                    <b-col cols="9">
                        <h5 class="text-center">
                            Arrastre el bloque al nivel de diagrama que
                            corresponda
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
                <b-row v-if="editMainBlock" class="mt-5">
                    <b-col>
                        <div class="card">
                            <div class="card-body">
                                <b-row align-v="center">
                                    <b-col>
                                        <b-form-group
                                            label="Ingrese el título del bloque"
                                            invalid-feedback="Este campo es obligatorio"
                                            :state="blockState.title"
                                        >
                                            <vue-editor
                                                v-model="block.preview.title"
                                                :state="blockState.title"
                                            ></vue-editor>
                                        </b-form-group>
                                        <b-form-group
                                            label="Ingrese la descripción del bloque"
                                            invalid-feedback="Este campo es obligatorio"
                                            :state="blockState.description"
                                        >
                                            <vue-editor
                                                v-model="block.node.description"
                                                :state="blockState.description"
                                            ></vue-editor>
                                        </b-form-group>
                                    </b-col>
                                </b-row>
                            </div>
                        </div>
                    </b-col>
                </b-row>

                <!--b-row v-if="editNodeForm" class="mt-5">
                    <b-col>
                        <div class="card">
                            <div class="card-body">
                                <b-row>
                                    <b-col>
                                        <h5 class="text-center">Editar nodo</h5>
                                    </b-col>
                                </b-row>
                                <b-row align-v="center">
                                    <b-col>
                                        <b-form-group
                                            label="Ingrese el título del nodo"
                                            invalid-feedback="Este campo es obligatorio"
                                            :state="editNodeState.title"
                                        >
                                            <vue-editor
                                                v-model="node.title"
                                                :state="editNodeState.title"
                                            ></vue-editor>
                                        </b-form-group>
                                        <b-form-group
                                            label="Ingrese la descripción del nodo"
                                            invalid-feedback="Este campo es obligatorio"
                                            :state="editNodeState.description"
                                        >
                                            <vue-editor
                                                v-model="node.description"
                                                :state="
                                                    editNodeState.description
                                                "
                                            ></vue-editor>
                                        </b-form-group>
                                    </b-col>
                                </b-row>
                                <b-row>
                                    <b-col>
                                        <div class="w-100">
                                            <b-button
                                                variant="warning"
                                                class="float-right"
                                                @click="saveNode"
                                            >
                                                Editar nodo
                                            </b-button>
                                        </div>
                                    </b-col>
                                </b-row>
                            </div>
                        </div>
                    </b-col>
                </b-row-->
                <b-row
                    v-if="
                        is_superuser == true ||
                        permissions.includes(
                            'bcm_phase3.add_contingencyplanblock'
                        )
                    "
                    align-v="center"
                >
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
                                    />
                                </template>
                            </flowy-new-block>
                        </div>
                    </b-col>
                </b-row>

                <b-row align-v="center" class="mt-5">
                    <b-col>
                        <h5 class="text-center">
                            Plan de contingencia para el Escenario Crítico
                        </h5>
                    </b-col>
                </b-row>
                <b-row class="justify-content-md-center mt-3" align-v="center">
                    <b-col md="auto">
                        <flowy
                            :nodes="nodes"
                            :beforeMove="beforeMove"
                            :beforeAdd="beforeAdd"
                            @add="add"
                            @move="move"
                            @remove="remove"
                            @drag-start="onDragStart"
                        ></flowy>
                    </b-col>
                </b-row>
            </b-col>
        </b-row>
        <b-row
            v-if="
                !loadingNodes &&
                loadingFirstNodes &&
                (is_superuser == true ||
                    permissions.includes(
                        'bcm_phase3.add_contingencyplanblock'
                    ) ||
                    permissions.includes(
                        'bcm_phase3.change_contingencyplanblock'
                    ) ||
                    permissions.includes(
                        'bcm_phase3.delete_contingencyplanblock'
                    ))
            "
            align-v="center"
            class="mt-3"
        >
            <b-col>
                <div class="text-right">
                    <b-button
                        variant="success"
                        size="lg"
                        @click="saveContingencyPlan"
                    >
                        Guardar plan de contingencia
                    </b-button>
                </div>
            </b-col>
        </b-row>

        <!--
            Modal de editar  
        -->
        <b-modal
            id="modal-update"
            title="Editar servicio"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="saveNode">
                <b-form-group
                    label="Ingrese el título del nodo"
                    invalid-feedback="Este campo es obligatorio"
                    :state="editNodeState.title"
                >
                    <vue-editor
                        v-model="node.title"
                        :state="editNodeState.title"
                    ></vue-editor>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción del nodo"
                    invalid-feedback="Este campo es obligatorio"
                    :state="editNodeState.description"
                >
                    <vue-editor
                        v-model="node.description"
                        :state="editNodeState.description"
                    ></vue-editor>
                </b-form-group>
            </form>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="saveNode"
                    >
                        Editar nodo
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar editar  
        -->
        <b-modal
            id="modal-confirm-update"
            title="Confirmar editar nodo"
            centered
        >
            <h4>¿Está seguro de editar este nodo?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="confirmSaveNode"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar eliminar  
        -->
        <b-modal
            id="modal-confirm-delete"
            title="Confirmar eliminar nodo"
            centered
        >
            <h4>
                ¿Está seguro de eliminar este nodo? Tenga en cuenta que si este
                nodo posee <strong>nodos hijos</strong> entonces los nodos hijos
                también serán eliminados
            </h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteNode"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>
    </div>
</template>


<script>
import Vue from "vue";
import _ from "lodash";
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";
import NotificationTemplate from "../Notifications/NotificationTemplate";
import DemoBlock from "./flowy-components/DemoBlock.vue";
import { VueEditor } from "vue2-editor";
//import DemoNode from "./flowy-components/DemoNode.vue";

const DemoNode = {
    data() {
        return {
            text: "This is component A",
        };
    },
    props: ["remove", "node", "title", "description"],
    methods: {
        editNode() {
            this.$props.node.action = "edit";
            this.remove();
        },
        deleteNode() {
            console.log("Permisos");
            console.log(this.$props);
            console.log(this.$props.permissions);
            this.$props.node.action = "delete";
            this.remove();
        },
    },
    template: `
    <b-card flat bordered class="my-card bg-white">
        <div class="row items-center no-wrap">
            <div class="col">
                <div v-html="title" class="text-h6" />
                {{ this.$props.permissions }}
            </div>

            <div class="col-auto">
                <flowy-drag-handle>
                    <b-button variant="light">
                        <b-icon-justify></b-icon-justify>
                    </b-button>
                </flowy-drag-handle>
            </div>
        </div>

        <div v-html="description" />
        <div class="d-flex justify-content-around">
            <b-col><b-button variant="warning" v-if="(this.$props.node.canBeEdited)" @click="editNode()">Editar</b-button></b-col>
            <b-col><b-button variant="danger" v-if="(this.$props.node.parentId != -1) && (this.$props.node.canBeDeleted)" @click="deleteNode()">Eliminar</b-button></b-col>
        </div>
    </b-card>
  `,
};

Vue.component("demo-node", DemoNode);

export default {
    name: "ContingencyPlans",
    components: {
        DemoBlock,
        DemoNode,
        VueEditor,
    },
    data: () => ({
        permissions: [],
        is_superuser: false,

        loadingCrisisScenarios: false,

        crisisScenarios: [],
        crisisScenarioId: 0,

        editMainBlock: false,
        blockState: {
            title: null,
            description: null,
        },

        node: {
            title: "",
            description: "",
        },
        nodeIndex: 0,
        nodeIndexDelete: 0,
        editNodeState: {
            title: null,
            description: null,
        },

        dragging: false,
        block: {
            preview: {
                title: "<p><strong>Nuevo paso a ingresar</strong></p>",
            },
            node: {
                title: "",
                description: ".",
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
        loadingNodes: false,
        loadingFirstNodes: false,
        nodes: [],
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
    }),
    mounted() {
        this.getCrisisScenarios();
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

        async getCrisisScenarios() {
            this.crisisScenarios = [];
            this.loadingCrisisScenarios = true;

            axios
                .get(`${SERVER_ADDRESS}/api/phase1/crisis_scenarios_list/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.crisisScenarios = res.data;
                    this.loadingCrisisScenarios = false;
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
        async getContingencyPlanBlockNodes() {
            this.nodes = [];
            this.loadingNodes = true;
            this.loadingFirstNodes = true;

            axios
                .get(`${SERVER_ADDRESS}/api/phase3/contingency-plan-detail/`, {
                    params: { crisis_scenario: this.crisisScenarioId },
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    let canBeEdited = false;
                    let canBeDeleted = false;
                    if (
                        this.permissions.includes(
                            "bcm_phase3.change_contingencyplanblock"
                        )
                    ) {
                        canBeEdited = true;
                    }
                    if (
                        this.permissions.includes(
                            "bcm_phase3.delete_contingencyplanblock"
                        )
                    ) {
                        canBeDeleted = true;
                    }

                    if (res.data.length) {
                        for (var i = 0; i < res.data.length; i++) {
                            let nodeObj = {
                                id: res.data[i].block_id,
                                parentId: res.data[i].parent_block_id,
                                nodeComponent: "demo-node",
                                canBeEdited: canBeEdited,
                                canBeDeleted: canBeDeleted,
                                data: {
                                    text: res.data[i].title,
                                    title: res.data[i].title,
                                    description: res.data[i].description,
                                },
                            };
                            this.nodes.push(nodeObj);
                        }
                    } else {
                        let nodeObj = {
                            id: 1,
                            parentId: -1,
                            nodeComponent: "demo-node",
                            data: {
                                text: "Ejemplo de plan de contingencia",
                                title: "Ejemplo de plan de contingencia",
                                description:
                                    "Este escenario crítico todavía no posee un plan de contingencia",
                            },
                        };
                        this.nodes.push(nodeObj);
                    }
                    this.loadingNodes = false;
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
        saveContingencyPlan() {
            let contingencyObj = {
                contingency_plan_list: [],
            };

            for (var i = 0; i < this.nodes.length; i++) {
                let nodeObj = {
                    block_id: this.nodes[i].id,
                    parent_block_id: this.nodes[i].parentId,
                    title: this.nodes[i].data.title,
                    description: this.nodes[i].data.description,
                };
                contingencyObj.contingency_plan_list.push(nodeObj);
            }

            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase3/contingency-plans-create/${this.crisisScenarioId}/`,
                    contingencyObj,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡El plan de contingencia ha sido guardado exitosamente!"
                    );
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

        /**
         * Métodos para manejar el diagrama
         */
        onDragStartNewBlock(event) {
            // console.log("onDragStartNewBlock", event);
            // contains all the props and attributes passed to demo-node
            const { props } = event;
            this.newDraggingBlock = props;
        },
        onDragStopNewBlock(event) {
            // console.log("onDragStopNewBlock", event);
            this.newDraggingBlock = null;
        },
        // REQUIRED
        beforeMove({ to, from }) {
            // called before moving node (during drag and after drag)
            // indicator will turn red when we return false
            // from is null when we're not dragging from the current node tree
            // console.log("beforeMove", to, from);

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
            // console.log("beforeAdd", to, from);

            // Inicializamos variables de estados
            this.blockState.title = null;
            this.blockState.description = null;

            // Exit when the form isn't valid
            if (!this.checkBlockValidity()) {
                return false;
            }

            // we've passed this attribute to the demo-node
            if (this.newDraggingBlock["custom-attribute"] === false) {
                return false;
            }

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
        move(event) {
            // console.log("move", event);

            // node we're dragging to and node we've just dragged
            const { dragged, to } = event;

            // change panentId to id of node we're dragging to
            dragged.parentId = to.id;
        },
        add(event) {
            // every node needs an ID
            const id = this.generateId();

            // Le asignamos la pre visualización al título
            this.block.node.title = this.block.preview.title;

            // Le agregamos a la variable de evento la información del bloque
            event.node.data.title = this.block.node.title;
            event.node.data.description = this.block.node.description;

            if (
                this.permissions.includes(
                    "bcm_phase3.change_contingencyplanblock"
                )
            ) {
                event.node.canBeEdited = true;
            } else {
                event.node.canBeEdited = false;
            }
            if (
                this.permissions.includes(
                    "bcm_phase3.delete_contingencyplanblock"
                )
            ) {
                event.node.canBeDeleted = true;
            } else {
                event.node.canBeDeleted = false;
            }

            // add to array of nodes
            this.nodes.push({
                id,
                ...event.node,
            });
        },
        onDragStart(event) {
            // console.log("onDragStart", event);
            this.dragging = true;
        },
        remove(event) {
            // console.log("remove", event);

            // node we're dragging to
            const { node } = event;

            // we use lodash in this demo to remove node from the array
            const nodeIndex = _.findIndex(this.nodes, { id: node.id });

            if (event.node.action == "edit") {
                this.nodeIndex = nodeIndex;
                this.editNode();
            }
            if (event.node.action == "delete") {
                this.nodeIndexDelete = nodeIndex;
                this.$nextTick(() => {
                    this.$bvModal.show("modal-confirm-delete");
                });
            }
        },
        editNode() {
            this.editMainBlock = false;

            let nodeFound;
            for (var i = 0; i < this.nodes.length; i++) {
                if (i == this.nodeIndex) {
                    nodeFound = this.nodes[i];
                    break;
                }
            }

            this.node.title = nodeFound.data.title;
            this.node.description = nodeFound.data.description;
            this.editNodeState = {
                title: null,
                description: null,
            };

            this.$nextTick(() => {
                this.$bvModal.show("modal-update");
            });
        },
        deleteNode() {
            this.nodes.splice(this.nodeIndexDelete, 1);

            // Mensaje de éxito
            this.successMessage(
                "¡El nodo o grupo de nodos ha sido eliminado exitosamente!"
            );
            this.$nextTick(() => {
                this.$bvModal.hide("modal-confirm-delete");
            });
        },
        saveNode() {
            this.editNodeState.title = null;
            this.editNodeState.description = null;

            // Exit when the form isn't valid
            if (!this.checkNodeValidity()) {
                return;
            }

            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-update");
            });
        },
        confirmSaveNode() {
            for (var i = 0; i < this.nodes.length; i++) {
                if (i == this.nodeIndex) {
                    this.nodes[i].data.title = this.node.title;
                    this.nodes[i].data.description = this.node.description;
                    break;
                }
            }

            // Mensaje de éxito
            this.successMessage("¡El nodo ha sido editado exitosamente!");

            this.$nextTick(() => {
                this.$bvModal.hide("modal-confirm-update");
                this.$bvModal.hide("modal-update");
            });
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
        checkNodeValidity() {
            let valid = true;
            if (!this.node.title) {
                this.editNodeState.title = false;
                valid = false;
            }
            if (!this.node.description) {
                this.editNodeState.description = false;
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

