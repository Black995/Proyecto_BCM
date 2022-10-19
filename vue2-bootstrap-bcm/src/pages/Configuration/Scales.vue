<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <h4 class="display-4">Escalas</h4>
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="scales"
                            responsiveLayout="scroll"
                            :paginator="true"
                            :rows="5"
                            :rowsPerPageOptions="[5, 10]"
                            :resizableColumns="true"
                            :autoLayout="true"
                            :responsive="true"
                            :reorderableColumns="true"
                            :loading="loading1"
                            :globalFilterFields="[
                                'name',
                                'min_value',
                                'max_value',
                            ]"
                            :filters="filterGlobal1"
                        >
                            <template #header>
                                <b-row class="justify-content-between">
                                    <b-col sm="4">
                                        <b-button
                                            v-if="
                                                is_superuser == true ||
                                                permissions.includes(
                                                    'configuration.add_scale'
                                                )
                                            "
                                            title="Crear escala"
                                            variant="success"
                                            @click="
                                                show_modal_create_scale = true
                                            "
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
                                                    filterGlobal1['global']
                                                        .value
                                                "
                                                placeholder="Buscar..."
                                            />
                                        </span>
                                    </b-col>
                                </b-row>
                            </template>
                            <Column field="name" header="Nombre"></Column>
                            <Column
                                field="min_value"
                                header="Valor mínimo"
                            ></Column>
                            <Column
                                field="max_value"
                                header="Valor máximo"
                            ></Column>
                            <Column field="id" header="Opciones">
                                <template #body="slotProps">
                                    <b-button
                                        v-if="
                                            is_superuser == true ||
                                            permissions.includes(
                                                'configuration.change_scale'
                                            )
                                        "
                                        title="Editar escala"
                                        pill
                                        variant="warning"
                                        @click="
                                            show_modal_update_scale(
                                                slotProps.data.id
                                            )
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-pen-to-square"
                                        />
                                    </b-button>
                                    <b-button
                                        v-if="
                                            is_superuser == true ||
                                            permissions.includes(
                                                'configuration.delete_scale'
                                            )
                                        "
                                        title="Eliminar escala"
                                        pill
                                        variant="danger"
                                        @click="
                                            show_modal_delete_scale(
                                                slotProps.data.id
                                            )
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-trash"
                                        />
                                    </b-button>
                                </template>
                            </Column>

                            <template #empty>
                                No hay escalas encontradas.
                            </template>
                        </DataTable>
                    </div>
                    <!-- /.card-body -->
                </div>
                <!-- /.card -->

                <h4 class="mt-3 display-4">Escalas de las Vistas</h4>
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="scalesView"
                            responsiveLayout="scroll"
                            :paginator="true"
                            :rows="10"
                            :resizableColumns="true"
                            :autoLayout="true"
                            :responsive="true"
                            :reorderableColumns="true"
                            :loading="loading2"
                            :globalFilterFields="['name', 'scale_name']"
                            :filters="filterGlobal2"
                        >
                            <template #header>
                                <b-row class="justify-content-between">
                                    <b-col sm="4">
                                        <b-button
                                            v-if="
                                                is_superuser == true ||
                                                permissions.includes(
                                                    'configuration.add_scaleview'
                                                )
                                            "
                                            title="Crear escala"
                                            variant="success"
                                            @click="
                                                show_modal_create_scale_view()
                                            "
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
                                                    filterGlobal2['global']
                                                        .value
                                                "
                                                placeholder="Buscar..."
                                            />
                                        </span>
                                    </b-col>
                                </b-row>
                            </template>
                            <Column
                                field="name"
                                header="Nombre de la vista"
                            ></Column>
                            <Column
                                field="scale_name"
                                header="Nombre de la escala"
                            ></Column>
                            <Column
                                field="minimum_recovery_time"
                                header="Máximo RTO tolerable"
                            ></Column>
                            <Column
                                field="minimum_scale_value"
                                header="Criticidad de referencia para el RTO"
                            ></Column>
                            <Column field="id" header="Opciones">
                                <template #body="slotProps">
                                    <b-button
                                        v-if="
                                            is_superuser == true ||
                                            permissions.includes(
                                                'configuration.change_scaleview'
                                            )
                                        "
                                        title="Editar escala"
                                        pill
                                        variant="warning"
                                        @click="
                                            show_modal_update_scale_view(
                                                slotProps.data.id
                                            )
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-pen-to-square"
                                        />
                                    </b-button>
                                    <b-button
                                        v-if="
                                            slotProps.data.name != 'default' &&
                                            (is_superuser == true ||
                                                permissions.includes(
                                                    'configuration.delete_scaleview'
                                                ))
                                        "
                                        title="Eliminar escala"
                                        pill
                                        variant="danger"
                                        @click="
                                            show_modal_delete_scale_view(
                                                slotProps.data.id
                                            )
                                        "
                                    >
                                        <font-awesome-icon
                                            icon="fa-solid fa-trash"
                                        />
                                    </b-button>
                                </template>
                            </Column>

                            <template #empty>
                                No hay escalas encontradas.
                            </template>
                        </DataTable>
                    </div>
                    <!-- /.card-body -->
                </div>
                <!-- /.card -->
            </div>
            <!-- /.col -->
        </div>
        <div class="row"></div>

        <!--
            Modal de crear escala
        -->
        <b-modal
            v-model="show_modal_create_scale"
            id="modal-create-scale"
            title="Crear escala"
            ref="modal"
            size="lg"
            centered
            @show="resetModalScale"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreateScale">
                <b-form-group
                    label="Ingrese el título de la escala"
                    label-for="name-input-create"
                    invalid-feedback="Este campo es obligatorio"
                    :state="scaleState.name"
                >
                    <b-form-input
                        id="name-input"
                        v-model="scale.name"
                        :state="scaleState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Ingrese la escala mínima"
                            invalid-feedback="La escala mínima no puede ser negativa ni cero"
                            :state="scaleState.min_value"
                        >
                            <b-form-input
                                type="number"
                                v-model.number="scale.min_value"
                                :state="scaleState.min_value"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese la escala máxima"
                            invalid-feedback="La escala máxima no puede ser negativa ni cero"
                            :state="scaleState.max_value"
                        >
                            <b-form-input
                                type="number"
                                v-model.number="scale.max_value"
                                :state="scaleState.max_value"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitCreateScale"
                    >
                        Crear escala
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear escala
        -->
        <b-modal
            id="modal-confirm-create-scale"
            title="Confirmar crear escala"
            centered
        >
            <h4>¿Está seguro de crear esta escala?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createScale"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de actualizar escala
        -->
        <b-modal
            id="modal-update-scale"
            title="Editar escala"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdateScale">
                <b-form-group
                    label="Ingrese el título de la escala"
                    label-for="name-input-update"
                    invalid-feedback="Este campo es obligatorio"
                    :state="scaleState.name"
                >
                    <b-form-input
                        id="name-input"
                        v-model="scale.name"
                        :state="scaleState.name"
                        required
                    ></b-form-input>
                </b-form-group>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Ingrese la escala mínima"
                            invalid-feedback="La escala mínima no puede ser negativa ni cero"
                            :state="scaleState.min_value"
                        >
                            <b-form-input
                                type="number"
                                v-model.number="scale.min_value"
                                :state="scaleState.min_value"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese la escala máxima"
                            invalid-feedback="La escala máxima no puede ser negativa ni cero"
                            :state="scaleState.max_value"
                        >
                            <b-form-input
                                type="number"
                                v-model.number="scale.max_value"
                                :state="scaleState.max_value"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitUpdateScale"
                    >
                        Editar escala
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar actualizar escala
        -->
        <b-modal
            id="modal-confirm-update-scale"
            title="Confirmar actualizar escala"
            centered
        >
            <h4>¿Está seguro de actualizar esta escala?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="updateScale"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar eliminar escala
        -->
        <b-modal
            id="modal-confirm-delete-scale"
            title="Confirmar eliminar escala"
            centered
        >
            <h4>¿Está seguro de eliminar esta escala?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteScale"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de crear escala de la vista
        -->
        <b-modal
            id="modal-create-scale-view"
            title="Crear escala de la vista"
            ref="modal"
            size="lg"
            centered
            @show="resetModalScaleView"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreateScaleView">
                <b-form-group
                    label="Ingrese el título de la escala de la vista"
                    label-for="name-input-create"
                    invalid-feedback="Este campo es obligatorio"
                    :state="scaleViewState.name"
                >
                    <b-form-select
                        v-model="scaleView.name"
                        :options="viewsNameList"
                        value-field="name"
                        text-field="name"
                        :state="scaleViewState.name"
                        required
                    ></b-form-select>
                </b-form-group>
                <b-form-group
                    label="Seleccione la escala asociada a esta vista"
                    invalid-feedback="Este campo es obligatorio"
                    :state="scaleViewState.scale"
                >
                    <b-form-select
                        v-model="scaleView.scale"
                        :options="scales"
                        value-field="id"
                        text-field="name"
                        :state="scaleViewState.scale"
                        required
                    ></b-form-select>
                </b-form-group>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitCreateScaleView"
                    >
                        Crear escala de la vista
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear escala de la vista
        -->
        <b-modal
            id="modal-confirm-create-scale-view"
            title="Confirmar crear escala de la vista"
            centered
        >
            <h4>¿Está seguro de crear esta escala de la vista?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createScaleView"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de actualizar escala de la vista
        -->
        <b-modal
            id="modal-update-scale-view"
            title="Editar escala de la vista"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdateScaleView">
                <p>
                    <strong>Nombre de la vista: </strong> {{ scaleView.name }}
                </p>
                <b-form-group
                    label="Seleccione la escala asociada a esta vista"
                    invalid-feedback="Este campo es obligatorio"
                    :state="scaleViewState.scale"
                >
                    <b-form-select
                        v-model="scaleView.scale"
                        :options="scales"
                        value-field="id"
                        text-field="name"
                        :state="scaleViewState.scale"
                        required
                    ></b-form-select>
                </b-form-group>
                <!--
                    Hasta los momentos, estas son las 2 vistas que funcionan con RTO y escala
                -->
                <b-row
                    align-v="center"
                    v-if="
                        scaleView.name == 'Actividades de la Organización' ||
                        scaleView.name == 'Servicios de la Organización'
                    "
                >
                    <b-col>
                        <b-form-group
                            label="Máximo tiempo de recuperación (RTO) tolerable"
                            invalid-feedback="Este campo es obligatorio"
                            :state="scaleViewState.minimum_recovery_time"
                        >
                            <b-row cols="1" cols-sm="3" cols-md="3" cols-lg="3">
                                <b-col>
                                    <b-form-group label="Días">
                                        <b-form-input
                                            type="number"
                                            v-model.number="
                                                minimumRecoveryTimeScaleDuration.days
                                            "
                                            :state="
                                                scaleViewState.minimum_recovery_time
                                            "
                                        ></b-form-input>
                                    </b-form-group>
                                </b-col>
                                <b-col>
                                    <b-form-group label="Horas">
                                        <b-form-select
                                            v-model="
                                                minimumRecoveryTimeScaleDuration.hours
                                            "
                                            :options="hours"
                                            label="Horas"
                                            :state="
                                                scaleViewState.minimum_recovery_time
                                            "
                                        ></b-form-select>
                                    </b-form-group>
                                </b-col>
                                <b-col>
                                    <b-form-group label="Minutos">
                                        <b-form-select
                                            v-model="
                                                minimumRecoveryTimeScaleDuration.minutes
                                            "
                                            :options="minutes"
                                            label="Minutos"
                                            :state="
                                                scaleViewState.minimum_recovery_time
                                            "
                                        ></b-form-select>
                                    </b-form-group>
                                </b-col>
                            </b-row>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese la criticidad de referencia para el RTO (es decir, la criticidad ingresada de referencia que no pueda superar el máximo RTO tolerable)"
                            invalid-feedback="La escala mínima para el RTO tiene que estar en el rango de la escala seleccionada"
                            :state="scaleViewState.minimum_scale_value"
                        >
                            <b-form-input
                                type="number"
                                v-model.number="scaleView.minimum_scale_value"
                                :state="scaleViewState.minimum_scale_value"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
                <p class="mt-3">
                    <strong>NOTA: </strong>al actualizar las escalas tiene dos
                    opciones:
                </p>
                <b-form-checkbox
                    v-model="scaleView.option"
                    value="1"
                    unchecked-value="2"
                >
                    <strong>1. </strong>se colocarán en nulo todas las
                    criticidades del componente de la organización a actualizar.
                </b-form-checkbox>
                <b-form-checkbox
                    v-model="scaleView.option"
                    value="2"
                    unchecked-value="1"
                >
                    <strong>2. </strong>el sistema realizará automáticamente un
                    ajuste de las criticidades de acuerdo a la media entre la
                    escala actual y la escala a modificar.
                </b-form-checkbox>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitUpdateScaleView"
                    >
                        Editar escala de la vista
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar actualizar escala de la vista
        -->
        <b-modal
            id="modal-confirm-update-scale-view"
            title="Confirmar actualizar escala de la vista"
            centered
        >
            <h4>¿Está seguro de actualizar esta escala de la vista?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="updateScaleView"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar eliminar escala de la vista
        -->
        <b-modal
            id="modal-confirm-delete-scale-view"
            title="Confirmar eliminar escala de la vista"
            centered
        >
            <h4>¿Está seguro de eliminar esta escala de la vista?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteScaleView"
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
import NotificationTemplate from "../Notifications/NotificationTemplate";
import {
    getRecoveryTimeText,
    getRecoveryTime,
    setRecoveryTime,
} from "../../helpers/helpers";

export default {
    name: "Scales",

    data: () => ({
        loading1: false,
        loading2: false,
        filterGlobal1: {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        },
        filterGlobal2: {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        },
        permissions: [],
        is_superuser: false,

        // Variables para manejar los modales
        show_modal_create_scale: false,

        scales: [],
        scaleId: 0,
        scalesView: [],
        scaleViewId: 0,

        scale: {
            name: "",
            min_value: 0,
            max_value: 0,
        },
        scaleState: {
            name: null,
            min_value: null,
            max_value: null,
        },
        scaleView: {
            name: "",
            scale: 0,
            option: 0,
            minimum_recovery_time: "",
            minimum_scale_value: 0,
        },
        scaleViewState: {
            name: null,
            scale: null,
            minimum_recovery_time: null,
            minimum_scale_value: null,
        },
        minimumRecoveryTimeScaleDuration: {
            days: 0,
            hours: 0,
            minutes: 0,
        },
        hours: [
            0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
            19, 20, 21, 22, 23,
        ],
        minutes: [0, 15, 30, 45],

        /**
         * Lista de todas las vistas del sistema en la que se utilizan escalas
         */
        viewsName: [
            "Servicios de la Organización",
            "Servicios de Soporte",
            "Actividades de la Organización",
            // "Partes Interesadas",
        ],
        viewsNameList: [],
    }),
    mounted() {
        this.getScales();
        this.getScalesView();
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

        /**
         * Escalas
         */
        async getScales() {
            this.loading1 = true;
            this.scales = [];

            axios
                .get(`${SERVER_ADDRESS}/api/config/scales/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.scales = res.data;
                    this.loading1 = false;
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
        /**
         * Filtros que se manejan en Prime Vue
         */
        clearFilter1() {
            this.initFilters1();
        },
        initFilters1() {
            this.filterGlobal1 = {
                value: null,
                matchMode: FilterMatchMode.CONTAINS,
            };
        },

        /**
         * Validar formularios
         */
        checkFormValidityScales() {
            let valid = true;
            if (!this.scale.name) {
                this.scaleState.name = false;
                valid = false;
            }
            if (this.scale.min_value <= 0) {
                this.scaleState.min_value = false;
                valid = false;
            }
            if (this.scale.max_value <= 0) {
                this.scaleState.max_value = false;
                valid = false;
            }
            if (this.scale.min_value >= this.scale.max_value) {
                this.errorMessage(
                    "La escala mínima no puede ser mayor o igual a la escala máxima"
                );
                valid = false;
            }
            if (this.scale.max_value > 10) {
                this.errorMessage("La escala máxima no puede ser mayor a 10");
                valid = false;
            }
            return valid;
        },
        resetModalScale() {
            this.scale.name = "";
            this.scaleState.name = null;
            this.scale.min_value = 0;
            this.scaleState.min_value = null;
            this.scale.max_value = 0;
            this.scaleState.max_value = null;
        },
        /**
         * Create
         */
        handleSubmitCreateScale() {
            // Inicializamos variables de estados
            this.scaleState.name = null;
            this.scaleState.min_value = null;
            this.scaleState.max_value = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidityScales()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create-scale");
            });
        },
        async createScale() {
            axios
                .post(`${SERVER_ADDRESS}/api/config/scales/`, this.scale, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡La escala ha sido creada exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create-scale");
                        this.$bvModal.hide("modal-create-scale");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getScales();
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
        /**
         * Update
         */
        handleSubmitUpdateScale() {
            // Inicializamos variables de estados
            this.scaleState.name = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidityScales()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-update-scale");
            });
        },
        async show_modal_update_scale(id) {
            this.scaleId = id;

            axios
                .get(`${SERVER_ADDRESS}/api/config/scale/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.scale = res.data;
                    this.$nextTick(() => {
                        this.$bvModal.show("modal-update-scale");
                    });
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
        async updateScale() {
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/config/scale/${this.scaleId}/`,
                    this.scale,
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
                        "¡La escala ha sido actualizada exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update-scale");
                        this.$bvModal.hide("modal-update-scale");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getScales();
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
        /**
         * Delete
         */
        show_modal_delete_scale(id) {
            this.scaleId = id;
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete-scale");
            });
        },
        async deleteScale() {
            axios
                .delete(`${SERVER_ADDRESS}/api/config/scale/${this.scaleId}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡La escala ha sido eliminada exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-delete-scale");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getScales();
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

        /**
         * Escalas de las vistas
         */
        async getScalesView() {
            this.loading2 = true;
            this.scalesView = [];

            axios
                .get(`${SERVER_ADDRESS}/api/config/scales/view/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    for (var i = 0; i < res.data.length; i++) {
                        //Convertimos en texto la duración
                        res.data[i].minimum_recovery_time = getRecoveryTimeText(
                            res.data[i].minimum_recovery_time
                        );
                        this.scalesView.push(res.data[i]);
                    }
                    this.loading2 = false;
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
        /**
         * Filtros que se manejan en Prime Vue
         */
        clearFilter2() {
            this.initFilters2();
        },
        initFilters2() {
            this.filterGlobal2 = {
                value: null,
                matchMode: FilterMatchMode.CONTAINS,
            };
        },

        /**
         * Validar formularios
         */
        checkFormValidityScalesViewCreate() {
            let valid = true;
            if (!this.scaleView.name) {
                this.scaleViewState.name = false;
                valid = false;
            }
            if (this.scaleView.scale == 0) {
                this.scaleViewState.scale = false;
                valid = false;
            }

            return valid;
        },
        checkFormValidityScalesViewUpdate() {
            let valid = true;
            if (!this.scaleView.name) {
                this.scaleViewState.name = false;
                valid = false;
            }
            if (this.scaleView.scale == 0) {
                this.scaleViewState.scale = false;
                valid = false;
            }
            /**
             * Si la escala fue seleccionada, entonces verificamos que el mínimo valor de la
             * escala para el rto (minimum_scale_value) no sea menor o igual que el mínimo
             * valor de la escala (scale.min_value)
             */
            if (
                this.scaleView.name == "Actividades de la Organización" ||
                this.scaleView.name == "Servicios de la Organización"
            ) {
                for (var i = 0; i < this.scales.length; i++) {
                    if (
                        this.scales[i].id == this.scaleView.scale &&
                        this.scales[i].min_value >=
                            this.scaleView.minimum_scale_value
                    ) {
                        this.errorMessage(
                            "El valor mínimo de la escala para el RTO no puede ser menor al valor mínimo disponible para la escala"
                        );
                        valid = false;
                    }
                    if (
                        this.scales[i].id == this.scaleView.scale &&
                        (this.scaleView.minimum_scale_value <
                            this.scales[i].min_value ||
                            this.scaleView.minimum_scale_value >
                                this.scales[i].max_value)
                    ) {
                        this.scaleViewState.minimum_scale_value = false;
                        valid = false;
                    }
                }
            }
            if (
                (this.scaleView.name == "Actividades de la Organización" ||
                    this.scaleView.name == "Servicios de la Organización") &&
                this.minimumRecoveryTimeScaleDuration.days == 0 &&
                this.minimumRecoveryTimeScaleDuration.hours == 0 &&
                this.minimumRecoveryTimeScaleDuration.minutes == 0
            ) {
                this.scaleViewState.minimum_recovery_time = false;
                valid = false;
            }
            if (this.scaleView.option == 0) {
                this.errorMessage(
                    "Seleccione una de las opciones antes de actualizar"
                );
                valid = false;
            }
            return valid;
        },
        resetModalScaleView() {
            this.scaleView.name = "";
            this.scaleViewState.name = null;
            this.scaleView.scale = 0;
            this.scaleViewState.scale = null;
        },
        /**
         * Create
         */
        handleSubmitCreateScaleView() {
            // Inicializamos variables de estados
            this.scaleViewState.name = null;
            this.scaleViewState.scale = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidityScalesViewCreate()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create-scale-view");
            });
        },
        async show_modal_create_scale_view() {
            /**
             * Filtramos que sólo se registren en viewsNameList las viewsName que no estén contenidas
             * en scalesView
             */
            this.viewsNameList = [];
            for (var i = 0; i < this.viewsName.length; i++) {
                for (var j = 0; j < this.scalesView.length; j++) {
                    if (this.scalesView[j].name == this.viewsName[i]) {
                        break;
                    }
                    // Si llega a la última posición entonces se inserta el elemento en el array
                    if (this.scalesView.length == j + 1) {
                        this.viewsNameList.push(this.viewsName[i]);
                    }
                }
            }
            if (this.scalesView.length == 0) {
                this.viewsNameList = this.viewsName;
            }

            this.$nextTick(() => {
                this.$bvModal.show("modal-create-scale-view");
            });
        },
        async createScaleView() {
            axios
                .post(
                    `${SERVER_ADDRESS}/api/config/scales/view/`,
                    this.scaleView,
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
                        "¡La escala de la vista ha sido creada exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create-scale-view");
                        this.$bvModal.hide("modal-create-scale-view");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getScalesView();
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
        /**
         * Update
         */
        handleSubmitUpdateScaleView() {
            // Inicializamos variables de estados
            this.scaleViewState.name = null;
            this.scaleViewState.scale = null;
            this.scaleViewState.minimum_recovery_time = null;
            this.scaleViewState.minimum_scale_value = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidityScalesViewUpdate()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-update-scale-view");
            });
        },
        async show_modal_update_scale_view(id) {
            this.scaleViewId = id;

            axios
                .get(`${SERVER_ADDRESS}/api/config/scale/view/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.scaleView = {
                        name: res.data.name,
                        scale: res.data.scale,
                        minimum_scale_value: res.data.minimum_scale_value,
                        option: 0,
                    };
                    this.minimumRecoveryTimeScaleDuration = getRecoveryTime(
                        res.data.minimum_recovery_time
                    );

                    this.$nextTick(() => {
                        this.$bvModal.show("modal-update-scale-view");
                    });
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
        async updateScaleView() {
            this.scaleView.minimum_recovery_time = setRecoveryTime(
                this.minimumRecoveryTimeScaleDuration
            );

            axios
                .patch(
                    `${SERVER_ADDRESS}/api/config/scale/view/${this.scaleViewId}/`,
                    this.scaleView,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    // Mensaje de éxito
                    console.log(res)
                    this.successMessage(
                        "¡La escala de la vista ha sido actualizada exitosamente!"
                    );
                    let scale_id = {
                        scale_id: this.scaleViewId,
                    };
                    axios
                        .post(
                            `${SERVER_ADDRESS}/api/notifications/notify_modified_scale/`,
                            scale_id,
                            {
                                withCredentials: true,
                                headers: {
                                    Authorization: TOKEN,
                                },
                            }
                        )
                        .then((res) => {
                            this.successMessage(
                                "¡El personal ha sido notificado satisfactoriamente del cambio de la escala!"
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
                                        "Ups! Ha ocurrido un error al enviar la notificación"
                                    );
                                }
                            } catch {
                                // Servidor no disponible
                                this.errorMessage(
                                    "Ups! Ha ocurrido un error al enviar la notificación"
                                );
                            }
                        });
                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update-scale-view");
                        this.$bvModal.hide("modal-update-scale-view");
                    });

                    this.getScalesView();
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
        /**
         * Delete
         */
        show_modal_delete_scale_view(id) {
            this.scaleViewId = id;
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete-scale-view");
            });
        },
        async deleteScaleView() {
            axios
                .delete(
                    `${SERVER_ADDRESS}/api/config/scale/view/${this.scaleViewId}/`,
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
                        "¡La escala de la vista ha sido eliminada exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-delete-scale-view");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getScalesView();
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
    },
};
</script>
<style lang="scss">
</style>
