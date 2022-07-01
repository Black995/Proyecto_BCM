<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="activities"
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
                                'cost',
                                'recovery_time',
                                'criticality',
                            ]"
                            :filters="filterGlobal"
                        >
                            <template #header>
                                <b-row class="justify-content-between">
                                    <b-col sm="4">
                                        <b-button
                                            title="Crear actividad de negocio"
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
                            
                            <Column field="cost" header="Costo">
                                <template #body="slotProps">
                                    {{ slotProps.data.cost }}$
                                </template>
                            </Column>
                            <Column
                                field="recovery_time"
                                header="Tiempo de recuperación"
                            ></Column>
                            <Column field="criticality" header="Criticidad">
                                <template #body="slotProps">
                                    <div v-if="!slotProps.data.scale_max_value">
                                        {{ slotProps.data.criticality }}
                                    </div>
                                    <div v-if="slotProps.data.scale_max_value">
                                        {{ slotProps.data.criticality }}/{{
                                            slotProps.data.scale_max_value
                                        }}
                                    </div>
                                </template>    
                            </Column>
                            <Column field="id" header="Opciones">
                                
                            </Column>
                            <template #empty>
                                No hay actividades encontradas.
                            </template>

                        </DataTable>
                    </div>
                </div>
            </div>
        </div>
        <div class="row"></div>

        <!--
            Modal de crear  
        -->
        <b-modal
            v-model="show_modal_create"
            id="modal-create"
            title="Crear activida del negocio"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-form-group
                    label="Ingrese el nombre de la actividad"
                    invalid-feedback="Este campo es obligatorio"
                    :state="activityState.name"
                >
                    <b-form-input
                        v-model="activity.name"
                        :state="activityState.name"
                        required
                    >
                    </b-form-input>
                </b-form-group>
            
            </form>
        
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
    name: "BussinesActivities",
    components: {
        Multiselect,
    },
    data: () => ({
        loading: false,
        filterGlobal:{
            global: { value:null, matchMode: FilterMatchMode.CONTAINS},
        },

        show_modal_create: false,

        activities: [],
        activityId: 0,
        type: "",
        headquarters: [],

        activity: {
            name:"",
            description: "",
            cost: 0,
            recovery_time:"",
            criticality: 0,
            scale:0,
            
        },
        activityState:{
            nam: null,
            description: null,
            cost:null,

        },
        duration: {
            days: 0,
            hours: 0,
            minutes: 0,
        },
        hours: [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
            19, 20, 21, 22, 23,
        ],
        minutes: [0, 15, 30, 45],

        // Variable en la que se maneja la escala de la vista
        scaleView: {
            id: 0,
            name: "",
            scale: 0,
            scale_name: "",
            scale_min_value: 0,
            scale_max_value: 0,
        },
    }),
    mounted() {
        this.getBussinesActivities()
        this.getScaleView()
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
        async getBussinesActivities(){
            this.activities = []
            axios
                .get(`${SERVER_ADDRESS}/api/phase2/organizationActivities/`,{
                    withCredentials:true,
                    headers:{
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    console.log(res.data)
                    for(var i = 0; i < res.data.length; i++){
                        res.data[i].recovery_time = getRecoveryTimeText(
                            res.data[i].recovery_time
                        )
                        this.activities.push(res.data[i])
                    }
                    this.loading = false

                })
                .catch((err)=>{
                    try{
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(err.response.data);
                        } else {
                            // Servidor no disponible
                            this.errorMessage(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                        }
                    }
                    catch {
                        // Servidor no disponible
                        this.errorMessage(
                            "Ups! Ha ocurrido un error en el servidor"
                        );
                    }
                })
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
        async getScaleView() {
            axios
                .get(`${SERVER_ADDRESS}/api/config/scales/view/`, {
                    params: { name: "Actividades de la Organización" },
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.scaleView = res.data[0];
                    this.scaleView.scale_min_value = parseInt(
                        this.scaleView.scale_min_value
                    );
                    this.scaleView.scale_max_value = parseInt(
                        this.scaleView.scale_max_value
                    );
                    this.service.criticality = res.data[0].scale_min_value;
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(err.response.data);
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
        checkFormValidity(){
            let valid = true
            if (!this.activity.name){
                valid = false
                this.activityState.name = false
            }
            if(!this.activity.description){
                valid = false
                this.activityState.description = false
            }
            if(this.activity.cost = 0){
                valid = false
                this.activityState.cost = false
            }

        },
        handleSubmitCreate(){

        },
        async getHeadquarters(){
            this.headquarters = []
        
            axios
                .get(`${SERVER_ADDRESS}/api/config/headquarters/`,{
                    withCredentials:true,
                    headers:{
                        Authorization: TOKEN
                    },
                })
                .then((res)=>{
                    this.headquarters = res.data
                })
                .catch((err)=>{
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(err.response.data);
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
        resetModal(){
            this.activity.name = ""
            this.activity.description= ""
            this.activity.cost= 0
            this.activity.recovery_time=""
            this.activity.criticality= 0
            this.activity.scale=0
        }

    }
}
</script>

<style lang="scss">
</style>