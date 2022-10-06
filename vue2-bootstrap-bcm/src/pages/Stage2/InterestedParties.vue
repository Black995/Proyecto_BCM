<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="parties"
                            responsiveLayout="scroll"
                            :paginator="true"
                            :rows="10"
                            :rowsPerPageOptions="[10, 20]"
                            :resizableColumns="true"
                            :autoLayout="true"
                            :responsive="true"
                            :reorderableColumns="true"
                            :loading="loading"
                            :globalFilterFields="['name', 'type_name']"
                            :filters="filterGlobal"
                        >
                            <template #header>
                                <b-row class="justify-content-between">
                                    <b-col sm="4">
                                        <b-button
                                            title="Crear parte interesada"
                                            variant="success"
                                            @click="show_modal_create = true"
                                        >
                                            <font-awesome-icon
                                                icon="fa-solid fa-plus"
                                            />
                                        </b-button>
                                    </b-col>
                                    <b-col sm="4">
                                        <span class="p-input-icon-left">
                                            <i class="pi pi-search" />

                                            <InputText
                                                v-model="
                                                    filterGlobal['global'].value
                                                "
                                                placeholder="Buscar..."
                                            />
                                        </span>
                                    </b-col>
                                </b-row>
                            </template>
                            <Column field="name" header="Nombre"></Column>
                            <Column field="type_name" header="Tipo"></Column>
                            <Column field="id" header="Opciones">
                                <template #body="slotProps">
                                    <b-button
                                        tittle="Detalle de la parte interesada"
                                        pill
                                        variant="info"
                                        @click="
                                            show_modal_detail(slotProps.data.id)
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-search"
                                        />
                                    </b-button>
                                    <b-button
                                        tittle="Editar parte interesada"
                                        pill
                                        variant="warning"
                                        @click="
                                            show_modal_update(slotProps.data.id)
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-pen-to-square"
                                        />
                                    </b-button>
                                    <b-button
                                        title="Eliminar parte intersada"
                                        pill
                                        variant="danger"
                                        @click="
                                            show_modal_delete(slotProps.data.id)
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-trash"
                                        />
                                    </b-button>
                                </template>
                            </Column>
                            <Column
                                field="id_2"
                                header="Asociar servicios de Org."
                            >
                                <template #body="slotProps">
                                    <div class="text-center">
                                        <b-button
                                            pill
                                            title="Asociar servicios de la organización"
                                            variant="primary"
                                            @click="
                                                show_modal_association_services(
                                                    slotProps.data.id,
                                                    slotProps.data.name
                                                )
                                            "
                                        >
                                            <font-awesome-icon
                                                icon="fa-solid fa-computer"
                                            />
                                        </b-button>
                                    </div>
                                </template>
                            </Column>
                            <Column
                                field="id_3"
                                header="Asociar servicios de soporte"
                            >
                                <template #body="slotProps">
                                    <div class="text-center">
                                        <b-button
                                            pill
                                            title="Asociar servicios de soporte"
                                            variant="primary"
                                            @click="
                                                show_modal_association_support_services(
                                                    slotProps.data.id,
                                                    slotProps.data.name
                                                )
                                            "
                                        >
                                            <font-awesome-icon
                                                icon="fa-solid fa-computer"
                                            />
                                        </b-button>
                                    </div>
                                </template>
                            </Column>
                            <template #empty>
                                No hay servicios encontradas.
                            </template>
                        </DataTable>
                    </div>
                </div>
            </div>
        </div>
        <div class="row"></div>

        <!--
            Modal del detalle
        -->
        <b-modal
            id="modal-detail"
            title="Detalle de la parte interesada"
            ref="modal"
            size="lg"
            centered
        >
            <h3 class="text-center font-weight-bold">
                {{ partyDetail.name }}
            </h3>
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <strong>Tipo: </strong> {{ partyDetail.type_name }}
                </li>

                <li class="list-group-item">
                    <strong>Descripción: </strong> {{ partyDetail.description }}
                </li>
            </ul>
            <h4 class="mt-5 text-center font-weight-bold">
                Servicios de la organización asociados a esta parte interesada
            </h4>
            <b-list-group-item
                class="mt-2 flex-column align-items-start"
                v-for="item in partyDetail._services_offered"
                :key="item.key"
            >
                <h5 class="mb-1">{{ item.name }}</h5>
                <p class="mb-1">Tipo: {{ item.type_name }}</p>
            </b-list-group-item>
            <h3
                class="mt-3 text-center"
                v-if="!partyDetail._services_offered.length"
            >
                No existen servicios de la organización asociados a esta parte
                interesada
            </h3>
            <h4 class="mt-5 text-center font-weight-bold">
                Servicios de soporte asociados a esta parte interesada
            </h4>
            <b-list-group-item
                class="mt-2 flex-column align-items-start"
                v-for="item in partyDetail._services_used"
                :key="item.key"
            >
                <h5 class="mb-1">{{ item.name }}</h5>
                <p class="mb-1">Tipo:</p>
                {{ item.type_name }}
            </b-list-group-item>
            <h3
                class="mt-3 text-center"
                v-if="!partyDetail._services_used.length"
            >
                No existen servicios de soporte asociados a esta parte
                interesada
            </h3>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="info"
                        class="float-right"
                        @click="$bvModal.hide('modal-detail')"
                    >
                        Cerrar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de crear  
        -->
        <b-modal
            v-model="show_modal_create"
            id="modal-create"
            title="Crear parte interesada"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-form-group
                    label="Ingrese el nombre de la parte interesada"
                    invalid-feedback="Este campo es obligatorio"
                    :state="partyState.name"
                >
                    <b-form-input
                        v-model="party.name"
                        :state="partyState.name"
                        required
                    >
                    </b-form-input>
                </b-form-group>
                <b-form-group
                    label="Seleccione el tipo"
                    invalid-feedback="Este campo es obligatorio"
                    :state="partyState.type"
                >
                    <b-form-select
                        v-model="party.type"
                        :options="types"
                        value-field="value"
                        text-field="name"
                        :state="partyState.type"
                        required
                    ></b-form-select>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción de la parte interesada"
                    invalid-feedback="Este campo es obligatorio"
                    :state="partyState.description"
                >
                    <b-form-textarea
                        v-model="party.description"
                        :state="partyState.description"
                        required
                        rows="3"
                    ></b-form-textarea>
                </b-form-group>
            </form>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitCreate"
                    >
                        Crear servicio de la organización
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear  
        -->
        <b-modal
            id="modal-confirm-create"
            title="Confirmar crear parte interesada"
            centered
        >
            <h4>¿Está seguro de crear esta parte interesada?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createParty"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de editar  
        -->
        <b-modal
            id="modal-update"
            title="Editar parte interesada"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-form-group
                    label="Ingrese el título de la parte interesada"
                    invalid-feedback="Este campo es obligatorio"
                    :state="partyState.name"
                >
                    <b-form-input
                        v-model="party.name"
                        :state="partyState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    label="Seleccione el tipo"
                    invalid-feedback="Este campo es obligatorio"
                    :state="partyState.type"
                >
                    <b-form-select
                        v-model="party.type"
                        :options="types"
                        value-field="value"
                        text-field="name"
                        :state="partyState.type"
                        required
                    ></b-form-select>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción de la parte interesada"
                    invalid-feedback="Este campo es obligatorio"
                    :state="partyState.description"
                >
                    <b-form-textarea
                        v-model="party.description"
                        :state="partyState.description"
                        required
                        rows="3"
                    ></b-form-textarea>
                </b-form-group>
            </form>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitUpdate"
                    >
                        Editar parte interesada
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar editar  
        -->
        <b-modal
            id="modal-confirm-update"
            title="Confirmar editar parte interesada"
            centered
        >
            <h4>¿Está seguro de editar esta parte interesada?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="updateParty"
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
            title="Confirmar eliminar parte interesada"
            centered
        >
            <h4>¿Está seguro de eliminar esta parte interesada?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteParty"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de asociar servicios de la organización con partes interesadas
        -->
        <b-modal
            id="modal-associate-services"
            title="Asociar servicios de la organización con la parte interesada"
            size="lg"
            centered
        >
            <multiselect
                v-model="selectedServicesOffered"
                placeholder="Buscar servicios de la organización"
                label="name"
                track-by="id"
                :options="servicesOffered"
                :multiple="true"
            ></multiselect>

            <b-list-group v-if="selectedServicesOffered.length" class="mt-3">
                <b-list-group-item
                    href="#"
                    class="flex-column align-items-start"
                    v-for="item in selectedServicesOffered"
                    :key="item.key"
                >
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">{{ item.name }}</h5>
                        <!--small class="text-muted">3 days ago</small-->
                    </div>
                    <div class="mb-1 d-flex w-100 justify-content-between">
                        <div>Area: {{ item.area_name }}</div>
                        <div>Tipo: {{ item.type_name }}</div>
                        <div v-if="!item.scale_max_value">
                            Criticidad: {{ item.criticality }}
                        </div>
                        <div v-if="item.scale_max_value">
                            Criticidad: {{ item.criticality }}/{{
                                item.scale_max_value
                            }}
                        </div>
                    </div>
                </b-list-group-item>
            </b-list-group>

            <h3 class="mt-3 text-center" v-if="!selectedServicesOffered.length">
                No existen servicios de la organización asociados a esta parte
                interesada
            </h3>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="primary"
                        class="float-right"
                        @click="show_modal_confirm_association_services"
                    >
                        Asociar servicios de la organización
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar asociar servicios  
        -->
        <b-modal
            id="modal-confirm-associate-services"
            title="Confirmar asociar servicios de la organización"
            centered
        >
            <h4>
                ¿Está seguro de asociar estos servicios de la organización a la
                parte interesada?
            </h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="primary"
                        class="float-right"
                        @click="associateServices"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <b-modal
            id="modal-associate-support-services"
            title="Asociar servicios de la organización con la parte interesada"
            size="lg"
            centered
        >
            <multiselect
                v-model="selectedServicesUsed"
                placeholder="Buscar servicios de la organización"
                label="name"
                track-by="id"
                :options="servicesUsed"
                :multiple="true"
            ></multiselect>

            <b-list-group v-if="selectedServicesUsed.length" class="mt-3">
                <b-list-group-item
                    href="#"
                    class="flex-column align-items-start"
                    v-for="item in selectedServicesUsed"
                    :key="item.key"
                >
                    <div class="d-flex w-100 justify-content-between">
                        <h5 class="mb-1">{{ item.name }}</h5>
                        <!--small class="text-muted">3 days ago</small-->
                    </div>
                    <div class="mb-1 d-flex w-100 justify-content-between">
                        <div>Area: {{ item.area_name }}</div>
                        <div>Tipo: {{ item.type_name }}</div>
                        <div v-if="!item.scale_max_value">
                            Criticidad: {{ item.criticality }}
                        </div>
                        <div v-if="item.scale_max_value">
                            Criticidad: {{ item.criticality }}/{{
                                item.scale_max_value
                            }}
                        </div>
                    </div>
                </b-list-group-item>
            </b-list-group>

            <h3 class="mt-3 text-center" v-if="!selectedServicesUsed.length">
                No existen servicios de soporte asociados a esta parte
                interesada
            </h3>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="primary"
                        class="float-right"
                        @click="show_modal_confirm_association_support_services"
                    >
                        Asociar servicios de soporte
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar asociar servicios  
        -->
        <b-modal
            id="modal-confirm-associate-support-services"
            title="Confirmar asociar servicios de la organización"
            centered
        >
            <h4>
                ¿Está seguro de asociar estos servicios de la soporte a la parte
                interesada?
            </h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="primary"
                        class="float-right"
                        @click="associateSupportServices"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>
    </div>
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
    data: () => ({
        loading: false,
        filterGlobal: {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        },
        permissions: [],
        is_superuser: false,

        show_modal_create: false,

        parties: [],
        partyId: 0,
        partyName: "",
        type: "",

        party: {
            name: "",
            description: "",
            type: 0,
            type_name: "",
        },

        partyDetail: {
            name: "",
            description: "",
            type_name: "",
            _services_offered: [],
            _services_used: [],
        },

        partyState: {
            name: null,
            description: null,
            type: null,
        },
        types: [
            {
                value: 1,
                name: "Proveedor",
            },
            {
                value: 3,
                name: "Cliente",
            },
            {
                value: 4,
                name: "Stakeholder",
            },
        ],

        servicesOffered: [],
        selectedServicesOffered: [],

        servicesUsed: [],
        selectedServicesUsed: [],
    }),
    mounted() {
        this.getParties();
        this.getServicesOffered();
        this.getServicesUsed();
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
                global: { value: null, matchMode: FilterMatchMode.CONTAINS },
            };
        },
        checkFormValidity() {
            let valid = true;
            console.log(this.party.name);
            if (!this.party.name) {
                console.log(1);
                (valid = false), (this.partyState.name = false);
            }
            if (this.party.type == 0) {
                console.log(2);
                valid = false;
                this.partyState.type = false;
            }
            if (!this.party.description) {
                console.log(3);
                valid = false;
                this.partyState.description = false;
            }
            return valid;
        },
        resetModal() {
            this.party.name = "";
            this.party.type = 0;
            this.party.description = "";
            this.party.type_name = "";
            this.partyState.name = null;
            this.partyState.type = null;
            this.partyState.description = null;
        },
        handleSubmitCreate() {
            this.partyState.name = null;
            this.partyState.type = null;
            this.partyState.description = null;

            if (!this.checkFormValidity()) {
                console.log("entrando");
                return;
            }

            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create");
            });
        },
        createParty() {
            axios
                .post(
                    `${SERVER_ADDRESS}/api/phase2/interestedParties/`,
                    this.party,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.successMessage(
                        "¡La parte interesada ha sido creada con exito!"
                    );

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    this.getParties();
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
        handleSubmitUpdate() {
            this.partyState.name = null;
            this.partyState.type = null;
            this.partyState.description = null;

            if (!this.checkFormValidity()) {
                console.log("entrando");
                return;
            }

            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-update");
            });
        },
        async getParties() {
            this.loading = true;
            this.parties = [];
            axios
                .get(`${SERVER_ADDRESS}/api/phase2/interestedParties/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for (var i = 0; i < res.data.length; i++) {
                        this.parties.push(res.data[i]);
                    }
                    console.log(this.parties);
                    this.loading = false;
                });
        },
        show_modal_update(id) {
            (this.partyId = id),
                axios
                    .get(
                        `${SERVER_ADDRESS}/api/phase2/interestedParty/${this.partyId}/`,
                        {
                            withCredentials: true,
                            headers: {
                                Authorization: TOKEN,
                            },
                        }
                    )
                    .then((res) => {
                        this.party = res.data;
                        this.$nextTick(() => {
                            this.$bvModal.show("modal-update");
                        });
                    });
        },
        updateParty() {
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/interestedParty/${this.partyId}/`,
                    this.party,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.successMessage(
                        "¡La parte interesada ha sido actualizado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });

                    this.getParties();
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
        async show_modal_detail(id) {
            this.partyDetail = {
                id: 0,
                name: "",
                description: "",
                type: 0,
                type_name: "",
                _services_offered: [],
                _services_used: [],
            };
            axios
                .get(`${SERVER_ADDRESS}/api/phase2/interestedParty/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    console.log(res.data);
                    this.partyDetail = res.data;
                    console.log(this.partyDetail._services_offered);
                    this.$bvModal.show("modal-detail");
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
        show_modal_delete(id) {
            this.partyId = id;

            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
        async deleteParty() {
            axios
                .delete(
                    `${SERVER_ADDRESS}/api/phase2/interestedParty/${this.partyId}/`,
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
                        "¡LA parte interesada ha sido eliminada exitosamente!"
                    );
                    this.getParties();

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-delete");
                    });
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
        async show_modal_association_services(id) {
            this.partyId = id;
            this.selectedServicesOffered = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/interestedParty/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for (
                        let i = 0;
                        i < res.data._services_offered.length;
                        i++
                    ) {
                        this.selectedServicesOffered.push(
                            res.data._services_offered[i]
                        );
                    }

                    this.$nextTick(() => {
                        this.$bvModal.show("modal-associate-services");
                    });
                });
        },
        show_modal_confirm_association_services() {
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-associate-services");
            });
        },
        async getServicesOffered() {
            this.servicesOffered = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/services/offered/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.servicesOffered = res.data;
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

        async associateServices() {
            let servicesIds = [];
            for (let i = 0; i < this.selectedServicesOffered.length; i++) {
                servicesIds.push(this.selectedServicesOffered[i].id);
            }
            let ids = {
                services_offered: servicesIds,
            };
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/interestedParty/${this.partyId}/`,
                    ids,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.successMessage(
                        "¡Los servicios fueron asociados a la parte interesada exitosamente!"
                    );

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-associate-services");
                        this.$bvModal.hide("modal-associate-services");
                    });
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
        async show_modal_association_support_services(id) {
            this.partyId = id;
            this.selectedServicesUsed = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/interestedParty/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for (let i = 0; i < res.data._services_used.length; i++) {
                        this.selectedServicesUsed.push(
                            res.data._services_used[i]
                        );
                    }

                    this.$nextTick(() => {
                        this.$bvModal.show("modal-associate-support-services");
                    });
                });
        },
        async getServicesUsed() {
            this.servicesUsed = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/services/used/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.servicesUsed = res.data;
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
        show_modal_confirm_association_support_services() {
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-associate-support-services");
            });
        },
        async associateSupportServices() {
            let servicesIds = [];
            for (let i = 0; i < this.selectedServicesUsed.length; i++) {
                servicesIds.push(this.selectedServicesUsed[i].id);
            }
            let ids = {
                services_used: servicesIds,
            };
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/interestedParty/${this.partyId}/`,
                    ids,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.successMessage(
                        "¡Los servicios fueron asociados a la parte interesada exitosamente!"
                    );

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-associate-services");
                        this.$bvModal.hide("modal-associate-services");
                    });
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
    },
};
</script>

<style lang="scss">
</style>