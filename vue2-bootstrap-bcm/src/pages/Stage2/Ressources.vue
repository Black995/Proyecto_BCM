amount: 
<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="ressources"
                            responsiveLayout="scroll"
                            :paginator="true"
                            :rows="10"
                            :rowsPerPageOptions="[10, 20]"
                            :resizableColumns="true"
                            :autoLayout="true"
                            :responsive="true"
                            :reorderableColumns="true"
                            :loading="loading"
                            :globalFilterFields="[
                                'name',
                                'amout',
                            ]"
                            :filters="filterGlobal"
                        >
                            <template #header>
                                <b-row class="justify-content-between">
                                    <b-col sm="4">
                                        <b-button
                                            title="Crear recurso"
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
                            <Column field="amount" header="Cantidad">
                                <template #body="slotProps">
                                        <div v-if="slotProps.data.amount >= 0">
                                            {{ slotProps.data.amount }}
                                        </div>
                                    </template>
                            </Column>
                            <Column field="id" header="Opciones">
                                <template #body="slotProps">
                                    <b-button
                                        title="Detalle del recurso"
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
                                        title="Editar recurso"
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
                                        title="Eliminar recurso"
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
                            <Column field="id_2" header="Asociar servicio">
                                <template #body="slotProps">
                                    <div class="text-center">
                                        <b-button
                                            
                                            pill
                                            title="Asociar servicios a este recurso"
                                            variant="primary"
                                            @click="
                                                show_modal_association_services(
                                                    slotProps.data.id,
                                                    slotProps.data.amount,
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
                                No hay recursos registrados.
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
            title="Detalle del recurso"
            ref="modal"
            size="lg"
            centered
        >
            <h3 class="text-center font-weight-bold">
                {{ ressourceDetail.name }}
            </h3>
            <ul class="list-group list-group-flush">
                <li class="list-group-item">
                    <strong>Descripción: </strong>
                    {{ ressourceDetail.description }}
                </li>
                <li class="list-group-item">
                    <strong>Cantidad: </strong> {{ ressourceDetail.amount }}
                </li>
            </ul>
            <h4 class="mt-5 text-center font-weight-bold">
                Servicios de la organización que dependen de este recurso
            </h4>
            <b-list-group-item
                class="mt2 flex-column align-items-start"
                v-for="item in servicesOfferedDetail"
                :key="item.key"
            >
            <div class="d-flex w-100 justify-content-between">
                <h5 class="mb-1">{{ item.service_name }}</h5>
            </div>
            <div class="mb-1 d-flex w-100 justify-content-between">
                <div>Area: {{ item.service_area }}</div>
                <div>Tipo: {{ item.service_type }}</div>
                <div>Ganancia: {{ item.service_profit }}</div>
                <div>Cant. asignada: {{ item.amount }}</div>
            </div>

            </b-list-group-item>
            <h3
                class="mt-3 text-center"
                v-if="!servicesOfferedDetail.length"
            >
                No existen servicios de la organización asociados a esta
                actividad
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
            title="Crear recurso"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-form-group
                    label="Ingrese el nombre del recurso"
                    invalid-feedback="Este campo es obligatorio"
                    :state="ressourceState.name"
                >
                    <b-form-input
                        v-model="ressource.name"
                        :state="ressourceState.name"
                        required
                    >
                    </b-form-input>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción del recurso"
                    invalid-feedback="Este campo es obligatorio"
                    :state="ressourceState.description"
                >
                    <b-form-textarea
                        v-model="ressource.description"
                        :state="ressourceState.description"
                        required
                        rows="3"
                    ></b-form-textarea>   
                </b-form-group>
                <b-form-group
                    label="Ingrese la cantidad"
                    invalid-feedback="La cantidad no puede ser negativo"
                >
                    <b-form-input
                        type="number"
                        v-model.number="ressource.amount"
                        required
                    ></b-form-input>
                </b-form-group>
            </form> 
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitCreate"
                    >
                        Crear recurso
                    </b-button>
                </div>
            </template>
        </b-modal>
        <!--
            Modal de confirmar crear  
        -->
        <b-modal
            id="modal-confirm-create"
            title="Confirmar crear recurso"
            centered
        >
            <h4>¿Está seguro de crear este recurso?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createRessource"
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
            title="Editar servicio de la organización"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-form-group
                    label="Ingrese el nombre del recurso"
                    invalid-feedback="Este campo es obligatorio"
                    :state="ressourceState.name"
                >
                    <b-form-input
                        v-model="ressource.name"
                        :state="ressourceState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-form-group
                    label="Ingrese la descripción del recurso"
                    invalid-feedback="Este campo es obligatorio"
                    :state="ressourceState.description"
                >
                    <b-form-textarea
                        v-model="ressource.description"
                        :state="ressourceState.description"
                        required
                        rows="3"
                    ></b-form-textarea>   
                </b-form-group>
                <b-form-group
                    label="Ingrese la cantidad"
                    invalid-feedback="La cantidad no puede ser negativo"
                >
                    <b-form-input
                        type="number"
                        v-model.number="ressource.amount"
                        required
                    ></b-form-input>
                </b-form-group>
            </form>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitUpdate"
                    >
                        Editar servicio
                    </b-button>
                </div>
            </template>
        </b-modal>

        <b-modal
            id="modal-confirm-update"
            title="Confirmar crear recurso"
            centered
        >
            <h4>¿Está seguro de editar este recurso?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="updateRessource"
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
            title="Confirmar eliminar recurso"
            centered
        >
            <h4>¿Está seguro de eliminar este recurso?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteRessource"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>
        <!--
            Modal de asociar recurso con servicios de la organización  
        -->
        <b-modal
            id="modal-associate-services"
            title="Servicios de la organización que usan este recurso"
            ref="modal"
            size="lg"
            centered
        >
            <multiselect
                v-model="selectedServicesOffered"
                placeholder="Buscar servicio de la organización"
                label="service_name"
                track-by="service_id"
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
                        <h5 class="mb-1">{{ item.service_name }}</h5>
                        <!--small class="text-muted">3 days ago</small-->
                    </div>
                    <div class="mb-1 d-flex w-100 justify-content-between">
                        <div>Area: {{ item.service_area }}</div>
                        <div>Tipo: {{ item.service_type }}</div>
                        <div v-if="!item.scale_max_value">
                            Criticidad: {{ item.criticality }}
                        </div>
                        <div v-if="item.scale_max_value">
                            Criticidad: {{ item.criticality }}/{{
                                item.scale_max_value
                            }}
                        </div>
                        <div> Cant. asignada: {{ item.amount }}</div>
                    </div>
                </b-list-group-item>
            </b-list-group>
            <h3 class="mt-3 text-center" v-if="!selectedServicesOffered.length">
                No existen servicios de la organización asociados a este
                recurso
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
            Modal ingresar cantidad de recurso
        -->
        <b-modal
            id="modal-amount-ressources"
            title="Cantidad del recurso a asignar"
            ref="modal"
            centered

        > 
            <h3 class="text-center font-weight-bold">
                {{ ressourceName }}
            </h3>
            <h5 class="text-center font-weight-bold"> 
                Cantidad disponible: {{ ressourceAmount }}
            </h5>
            <form ref="form" @submit.stop.prevent="showAmount">
                <b-list-group-item
                    href="#"
                    class="flex-column align-items-start"
                    v-for="item in selectedServicesOffered"
                    :key="item.key"
                >
                    <div class="d-flex w-100 justify-content-between">
                        <h4 class="mb-1">{{ item.service_name }}</h4>
                    
                    </div>
                
                    <b-form-group
                        label="Ingrese la cantidad"
                        invalid-feedback="La cantidad no puede ser negativa o mayor a la cantidad disponible"
                        :state="item.amountState"
                    >
                        <b-form-input
                            type="number"
                            v-model.number="item.amount"
                            :state="item.amountState"
                            required
                        ></b-form-input>
                    </b-form-group>
                </b-list-group-item>
            </form>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="showAmount"
                    >
                        Confirmar
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
                ¿Está seguro de asociar estos servicios de la organización al recurso?
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
    name: "Ressources",
    components: {
        Multiselect,
    },
    data: () => ({
        loading: false,
        filterGlobal: {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        },

        show_modal_create: false,

        ressources: [],
        ressourceId: 0,
        ressourceName: "",
        ressourceAmount: 0,
        amount: 0,
        ressource: {
            name:"",
            amount:0,
        },
        ressourceDetail: {
            name:"",
            description: 0,
            amount: 0,
        },

        ressourceState: {
            name: null,
            description: null,
            amount: null,
        },
        services: [],
        servicesOffered: [],
        selectedServicesOffered: [],
        

        servicesOfferedDetail: [],

        serviceAmountState: null

    }),
    mounted() {
        this.getRessources()
        this.getServicesOffered()
    },
    methods:{
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
        async getRessources() {
            this.loading = true,
            this.ressources = []

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/ressources/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    }
                })
                .then((res)=>{
                    this.ressources = []
                    this.ressources = res.data
                    this.loading = false
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
            if (!this.ressource.name){
                valid = false
                this.ressourceState.name = false
            }
            if (!this.ressource.description){
                valid = false
                this.ressourceState.description = false
            }
            if (this.ressource.amount < 0){
                valid = false
                this.ressourceState.amount = false
            }
            return valid
        },
        handleSubmitCreate() {
            this.ressourceState.name = null
            this.ressourceState.description = null
            this.ressourceState.amount = null

            if (!this.checkFormValidity()){
                return
            }
            
            this.$nextTick(() =>{
                this.$bvModal.show("modal-confirm-create")
            })
        },
        createRessource(){

            axios
                .post(
                    `${SERVER_ADDRESS}/api/phase2/ressources/`,
                    this.ressource,
                    {
                        withCredentials:true,
                        headers: {
                            Authorization: TOKEN
                        }
                    }
                )
                .then((res) => {
                    this.successMessage(
                        "¡La actividad ha sido creada exitosamente!"
                    );

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    this.getRessources()
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
        resetModal(){
            this.ressource.name = ""
            this.ressourceState.name = null
            this.ressource.description = ""
            this.ressourceState.description = null
            this.ressource.amount = 0
            this.ressourceState.amount = null
        },
        async show_modal_detail(id){
            this.ressourceDetail = {
                name:"",
                desciption: "",
                amount: 0,
            }
            axios
                .get(`${SERVER_ADDRESS}/api/phase2/ressources/${id}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        }
                    }   
                )
                .then((res) => {
                    this.ressourceDetail = res.data
                    this.getServiceDetail(id)
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
        async getServiceDetail(id){
            this.servicesOfferedDetail = []

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/ressources_service_offered/`, {
                    params: { ressource_id : id },
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.servicesOfferedDetail = res.data
                    this.$bvModal.show("modal-detail")
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
        show_modal_update(id){
            this.ressourceId = id

            axios 
                .get(`${SERVER_ADDRESS}/api/phase2/ressources/${id}/`,{
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN
                    }

                })
                .then((res) => {
                    this.ressource = res.data
                    this.$bvModal.show("modal-update")
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
        handleSubmitUpdate(){
            this.ressourceState.name = null
            this.ressourceState.description = null
            this.ressourceState.amount = null

            if (!this.checkFormValidity()){
                return
            }
            
            this.$nextTick(() =>{
                this.$bvModal.show("modal-confirm-update")
            })
        },
        async updateRessource(){
            axios
                .patch(`${SERVER_ADDRESS}/api/phase2/ressources/${this.ressourceId}/`,
                    this.ressource,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN
                        }
                    }
                )
                .then((res) => {
                    this.successMessage(
                        "¡El recurso ha sido actualizado exitosamente!"
                    );

                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });
                    
                    this.getRessources()
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
                })
        },
        show_modal_delete(id) {
            this.ressourceId = id
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete")
            })
            
        },
        async deleteRessource(){
            axios
                .delete(`${SERVER_ADDRESS}/api/phase2/ressources/${this.ressourceId}/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN
                        }
                    }
                )
                .then((res) => {
                     // Mensaje de éxito
                     this.successMessage(
                        "¡El recurso ha sido eliminado exitosamente!"
                    );
                    this.getRessources()

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
        async getServicesOffered() {
            this.servicesOffered = [];
            this.selectedServicesOffered = []
            this.services = []
            axios
                .get(`${SERVER_ADDRESS}/api/phase2/services/offered/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for(let i = 0; i< res.data.length; i++){
                        let service = {
                            service_id: res.data[i].id,
                            service_name: res.data[i].name,
                            service_area: res.data[i].area_name,
                            service_type: res.data[i].type_name,
                            criticality: res.data[i].criticality,
                            scale_max_value: res.data[i].scale_max_value,
                            amount: 0
                        }
                        this.servicesOffered.push(service)
                    }

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
        async show_modal_association_services(id, amount, name){

            this.ressourceId = id
            this.ressourceAmount = amount
            this.ressourceName = name
            this.getServicesOffered()
            
            axios
                .get(`${SERVER_ADDRESS}/api/phase2/ressources_service_offered/`,{
                    params: { ressource_id: this.ressourceId },
                    withCredentials:true,
                    headers: {
                        Authorization: TOKEN,
                    }
                })
                .then((res) => {
                    this.selectedServicesOffered = []
                    for(var i = 0; i < res.data.length; i++){
                        let service = {
                            amount: res.data[i].amount,
                            criticality:res.data[i].criticality, 
                            id: res.data[i].id, 
                            scale_max_value:res.data[i].scale_max_value, 
                            service_area: res.data[i].service_area,
                            service_id: res.data[i].service_id,
                            service_name: res.data[i].service_name,
                            service_profit: res.data[i].service_profit,
                            service_type: res.data[i].service_type,
                            amountState: null,
                        }
                        this.selectedServicesOffered.push(service)
                    }
                    this.$nextTick(() => {
                        this.$bvModal.show("modal-associate-services");
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
        show_modal_confirm_association_services() {
            for(var i = 0; i< this.selectedServicesOffered.length; i++){
                this.selectedServicesOffered[i].amountState = null
            }
            this.$nextTick(() => {
                this.$bvModal.show("modal-amount-ressources");
            });
        },
        async showAmount(){
            
            this.services = []
            
            let valid = true
            for (let i = 0; i< this.selectedServicesOffered.length; i++){
                
                let service = {
                    service_offered: this.selectedServicesOffered[i].service_id,
                    amount: this.selectedServicesOffered[i].amount 
                }
                if( (this.ressourceAmount < service.amount) || (service.amount < 0)){
                    valid = false
                    this.selectedServicesOffered[i].amountState = false
                }   

                this.services.push(service)
            }
            if (!valid){
                return
            }
            this.$bvModal.show("modal-confirm-associate-services")
            
        },
        
        async associateServices(){
            
            let ids = {
                services_json: this.services
            }
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/ressources_service_offered1/${this.ressourceId}/`,
                    ids,
                    {
                        withCredentials:true,
                        headers: {
                            Authorization: TOKEN
                        }
                    }
                )
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡El recurso fue asignado al servicio de la organización exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-associate-services");
                        this.$bvModal.hide("modal-associate-services");
                        this.$bvModal.hide("modal-amount-ressources")
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

    }
    
}

</script>