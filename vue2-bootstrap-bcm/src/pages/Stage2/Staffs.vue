<template>
    <div class="container-fluid">
        <b-row align-v="center">
            <b-col>
                <div class="text-center">
                    <b-button
                        variant="success"
                        class="float-center"
                        @click="getBulkUploadTemplate"
                        :disabled="downloadBulkUploadTemplate"
                    >
                        <div v-if="!spinnerDownloadBulkUploadTemplate">
                            <font-awesome-icon icon="fa-solid fa-download" />
                            Descargar plantilla de carga masiva del personal
                        </div>
                        <b-spinner
                            v-if="spinnerDownloadBulkUploadTemplate"
                            small
                        ></b-spinner>
                    </b-button>
                </div>
            </b-col>
            <b-col>
                <div class="text-center">
                    <b-button
                        variant="info"
                        class="float-center"
                        @click="show_modal_bulk_upload = true"
                    >
                        <font-awesome-icon icon="fa-solid fa-upload" />
                        Carga masiva del personal
                    </b-button>
                </div>
            </b-col>
        </b-row>
        <div class="row mt-3">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="staffs"
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
                                'staff_number',
                                'names',
                                'surnames',
                                'earnings',
                                'area_name',
                                'position_name',
                            ]"
                            :filters="filterGlobal"
                        >
                            <template #header>
                                <b-row class="justify-content-between">
                                    <b-col sm="4">
                                        <b-button
                                            v-if="
                                                is_superuser == true ||
                                                permissions.includes(
                                                    'bcm_phase2.add_staff'
                                                )
                                            "
                                            title="Crear personal"
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
                                    <b-col sm="1">
                                        <b-button
                                            title="Descargar"
                                            variant="warning"
                                        >
                                            <font-awesome-icon
                                                icon="fa-solid fa-file-pdf"
                                            />
                                        </b-button>
                                    </b-col>
                                </b-row>
                            </template>
                            <Column
                                field="staff_number"
                                header="Número de Identificación"
                            ></Column>
                            <Column field="names" header="Nombres"></Column>
                            <Column
                                field="surnames"
                                header="Apellidos"
                            ></Column>
                            <Column field="earnings" header="Ingreso promedio">
                                <template #body="slotProps">
                                    <div v-if="slotProps.data.earnings > 0">
                                        {{ slotProps.data.earnings }}$
                                    </div>
                                </template>
                            </Column>
                            <Column field="area_name" header="Area"></Column>
                            <Column
                                field="position_name"
                                header="Cargo"
                            ></Column>
                            <Column field="id" header="Opciones">
                                <template #body="slotProps">
                                    <b-button
                                        title="Detalle del personal"
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
                                        v-if="
                                            is_superuser == true ||
                                            permissions.includes(
                                                'bcm_phase2.change_staff'
                                            )
                                        "
                                        title="Editar personal"
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
                                        v-if="
                                            is_superuser == true ||
                                            permissions.includes(
                                                'bcm_phase2.delete_staff'
                                            )
                                        "
                                        title="Eliminar personal"
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

                            <template #empty>
                                No hay personal encontrado.
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
            Modal del detalle  
        -->
        <b-modal
            id="modal-detail"
            title="Detalle del personal"
            ref="modal"
            size="lg"
            centered
        >
            <h3 class="text-center font-weight-bold">
                {{ staffDetail.names }} {{ staffDetail.surnames }}
            </h3>
            <ul class="list-group list-group-flush">
                <li v-if="staffDetail.user_email" class="list-group-item">
                    <strong
                        >Correo del usuario del sistema asociado a este
                        personal:</strong
                    >
                    {{ staffDetail.user_email }}
                </li>
                <li v-if="!staffDetail.user_email" class="list-group-item">
                    <strong
                        >Este personal no posee un usuario en el sistema</strong
                    >
                </li>
                <li class="list-group-item">
                    <strong>Número de Identificación: </strong
                    >{{ staffDetail.staff_number }}
                </li>
                <li class="list-group-item">
                    <strong>Teléfono 1: </strong>({{
                        staffDetail.phone_number_code_1
                    }}) {{ staffDetail.phone_number_1_format_international }}
                </li>
                <li
                    v-if="staffDetail.phone_number_2_format_international"
                    class="list-group-item"
                >
                    <strong>Teléfono 2: </strong>({{
                        staffDetail.phone_number_code_2
                    }}) {{ staffDetail.phone_number_2_format_international }}
                </li>
                <li
                    v-if="!staffDetail.phone_number_2_format_international"
                    class="list-group-item"
                >
                    <strong>Teléfono 2: </strong>-
                </li>
                <li v-if="staffDetail.earnings" class="list-group-item">
                    <strong>Ingreso promedio: </strong
                    >{{ staffDetail.earnings }}
                </li>
                <li v-if="!staffDetail.earnings" class="list-group-item">
                    <strong>Ingreso promedio: </strong>no aplica
                </li>
                <li class="list-group-item">
                    <strong>Area: </strong>{{ staffDetail.area_name }}
                </li>
                <li class="list-group-item">
                    <strong>Cargo: </strong>{{ staffDetail.position_name }}
                </li>
                <li class="list-group-item">
                    <strong>Area: </strong>{{ staffDetail.area_name }}
                </li>
                <li class="list-group-item">
                    <strong>Sede: </strong>{{ staffDetail.headquarter_name }}
                </li>
                <li class="list-group-item">
                    <strong>Ciudad de la sede: </strong
                    >{{ staffDetail.headquarter_city }}
                </li>
                <li class="list-group-item">
                    <strong>Parroquia de la sede: </strong
                    >{{ staffDetail.headquarter_parish }}
                </li>
                <li class="list-group-item">
                    <strong>Municipio de la sede: </strong
                    >{{ staffDetail.headquarter_township }}
                </li>
                <li class="list-group-item">
                    <strong>Estado de la sede: </strong
                    >{{ staffDetail.headquarter_state }}
                </li>
            </ul>

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
            title="Crear personal"
            ref="modal"
            size="lg"
            centered
            @show="resetModal"
        >
            <form ref="form" @submit.stop.prevent="handleSubmitCreate">
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Ingrese los nombres del personal"
                            invalid-feedback="Este campo es obligatorio"
                            :state="staffState.names"
                        >
                            <b-form-input
                                id="name-input"
                                v-model="staff.names"
                                :state="staffState.names"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese los apellidos del personal"
                            invalid-feedback="Este campo es obligatorio"
                            :state="staffState.surnames"
                        >
                            <b-form-input
                                id="name-input"
                                v-model="staff.surnames"
                                :state="staffState.surnames"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Ingrese el número de Identificación del personal"
                            invalid-feedback="Este campo es obligatorio"
                            :state="staffState.staff_number"
                        >
                            <b-form-input
                                id="name-input"
                                v-model="staff.staff_number"
                                :state="staffState.staff_number"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Seleccione el área a la que pertenece este personal"
                            invalid-feedback="Este campo es obligatorio"
                            :state="staffState.area"
                        >
                            <b-form-select
                                v-model="staff.area"
                                :options="areas"
                                value-field="id"
                                text-field="name"
                                :state="staffState.area"
                                required
                            ></b-form-select>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Ingrese el teléfono 1 del personal"
                            invalid-feedback="Es necesario cumplir con el formato del país seleccionado"
                            :state="staffState.phone_number_1"
                        >
                            <VuePhoneNumberInput
                                v-model="staff.phone_number_1"
                                v-bind="phone_number_1_props.props"
                                @update="onUpdateNumber1"
                            />
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese el teléfono 2 del personal (opcional)"
                            invalid-feedback="Es necesario cumplir con el formato del país seleccionado"
                            :state="staffState.phone_number_2"
                        >
                            <VuePhoneNumberInput
                                v-model="staff.phone_number_2"
                                v-bind="phone_number_2_props.props"
                                @update="onUpdateNumber2"
                            />
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Ingrese el ingreso promedio personal (en dólares)"
                            invalid-feedback="Este campo no puede ser negativo"
                            :state="staffState.earnings"
                        >
                            <b-form-input
                                id="name-input"
                                v-model.number="staff.earnings"
                                :state="staffState.earnings"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Seleccione el cargo del personal"
                            invalid-feedback="Este campo es obligatorio"
                            :state="staffState.position"
                        >
                            <b-form-select
                                v-model="staff.position"
                                :options="positions"
                                value-field="id"
                                text-field="name"
                                :state="staffState.position"
                                required
                            ></b-form-select>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Seleccione la sede del personal"
                            invalid-feedback="Este campo es obligatorio"
                            :state="staffState.headquarter"
                        >
                            <b-form-select
                                v-model="staff.headquarter"
                                :options="headquarters"
                                value-field="id"
                                text-field="name"
                                :state="staffState.headquarter"
                                required
                            ></b-form-select>
                        </b-form-group>
                    </b-col>
                </b-row>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="handleSubmitCreate"
                    >
                        Crear personal
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar crear  
        -->
        <b-modal
            id="modal-confirm-create"
            title="Confirmar crear personal"
            centered
        >
            <h4>¿Está seguro de crear esta personal?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="success"
                        class="float-right"
                        @click="createStaff"
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
            title="Editar personal"
            ref="modal"
            size="lg"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitUpdate">
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Ingrese los nombres del personal"
                            invalid-feedback="Este campo es obligatorio"
                            :state="staffState.names"
                        >
                            <b-form-input
                                id="name-input"
                                v-model="staff.names"
                                :state="staffState.names"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese los apellidos del personal"
                            invalid-feedback="Este campo es obligatorio"
                            :state="staffState.surnames"
                        >
                            <b-form-input
                                id="name-input"
                                v-model="staff.surnames"
                                :state="staffState.surnames"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Ingrese el número de Identificación del personal"
                            invalid-feedback="Este campo es obligatorio"
                            :state="staffState.staff_number"
                        >
                            <b-form-input
                                id="name-input"
                                v-model="staff.staff_number"
                                :state="staffState.staff_number"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Seleccione el área a la que pertenece este personal"
                            invalid-feedback="Este campo es obligatorio"
                            :state="staffState.area"
                        >
                            <b-form-select
                                v-model="staff.area"
                                :options="areas"
                                value-field="id"
                                text-field="name"
                                :state="staffState.area"
                                required
                            ></b-form-select>
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Ingrese el teléfono 1 del personal"
                            invalid-feedback="Es necesario cumplir con el formato del país seleccionado"
                            :state="staffState.phone_number_1"
                        >
                            <VuePhoneNumberInput
                                v-model="staff.phone_number_1"
                                v-bind="phone_number_1_props.props"
                                @update="onUpdateNumber1"
                            />
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Ingrese el teléfono 2 del personal (opcional)"
                            invalid-feedback="Es necesario cumplir con el formato del país seleccionado"
                            :state="staffState.phone_number_2"
                        >
                            <VuePhoneNumberInput
                                v-model="staff.phone_number_2"
                                v-bind="phone_number_2_props.props"
                                @update="onUpdateNumber2"
                            />
                        </b-form-group>
                    </b-col>
                </b-row>
                <b-row>
                    <b-col>
                        <b-form-group
                            label="Ingrese el ingreso promedio personal (en dólares)"
                            invalid-feedback="Este campo no puede ser negativo"
                            :state="staffState.earnings"
                        >
                            <b-form-input
                                id="name-input"
                                v-model.number="staff.earnings"
                                :state="staffState.earnings"
                                required
                            ></b-form-input>
                        </b-form-group>
                    </b-col>
                    <b-col>
                        <b-form-group
                            label="Seleccione el cargo del personal"
                            invalid-feedback="Este campo es obligatorio"
                            :state="staffState.position"
                        >
                            <b-form-select
                                v-model="staff.position"
                                :options="positions"
                                value-field="id"
                                text-field="name"
                                :state="staffState.position"
                                required
                            ></b-form-select>
                        </b-form-group>
                    </b-col> </b-row
                ><b-row>
                    <b-col>
                        <b-form-group
                            label="Seleccione la sede del personal"
                            invalid-feedback="Este campo es obligatorio"
                            :state="staffState.headquarter"
                        >
                            <b-form-select
                                v-model="staff.headquarter"
                                :options="headquarters"
                                value-field="id"
                                text-field="name"
                                :state="staffState.headquarter"
                                required
                            ></b-form-select>
                        </b-form-group>
                    </b-col>
                </b-row>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitUpdate"
                    >
                        Editar personal
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar editar  
        -->
        <b-modal
            id="modal-confirm-update"
            title="Confirmar editar personal"
            centered
        >
            <h4>¿Está seguro de editar este personal?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="updateStaff"
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
            title="Confirmar eliminar personal"
            centered
        >
            <h4>¿Está seguro de eliminar este personal?</h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="danger"
                        class="float-right"
                        @click="deleteStaff"
                    >
                        Confirmar
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de carga masiva del personal  
        -->
        <b-modal
            v-model="show_modal_bulk_upload"
            id="modal-bulk-upload"
            title="Carga masiva del personal"
            ref="modal"
            centered
        >
            <form ref="form" @submit.stop.prevent="handleSubmitBulkUploadStaff">
                <b-form-file
                    v-model="bulkUploadTemplate.template"
                    :state="bulkUploadTemplateState.template"
                    placeholder="Elija un archivo o arrástrelo aquí"
                    drop-placeholder="Arrastre el archivo aquí"
                ></b-form-file>
            </form>

            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="handleSubmitBulkUploadStaff"
                    >
                        Cargar archivo
                    </b-button>
                </div>
            </template>
        </b-modal>

        <!--
            Modal de confirmar actualizar documentación
        -->
        <b-modal
            id="modal-confirm-bulk-upload"
            title="Confirmar carga masiva del personal"
            centered
        >
            <h4>
                ¿Está seguro de cargar masivamente al personal contenido en la
                plantilla cargada?
            </h4>
            <template #modal-footer>
                <div class="w-100">
                    <b-button
                        variant="warning"
                        class="float-right"
                        @click="bulkUploadStaff"
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
import VuePhoneNumberInput from "vue-phone-number-input";

export default {
    name: "Staffs",
    components: {
        VuePhoneNumberInput,
    },
    data: () => ({
        loading: false,
        filterGlobal: {
            global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        },
        permissions: [],
        is_superuser: false,

        // Variables para manejar los modales
        show_modal_create: false,

        staffs: [],
        staffDetail: {
            staff_number: "",
            names: "",
            surnames: "",
            earnings: 0,
            area_name: "",
            position_name: "",
            headquarter_name: "",
            headquarter_city: "",
            headquarter_parish: "",
            headquarter_township: "",
            headquarter_state: "",
            user_email: "",
            phone_number_code_1: "",
            phone_number_1_format_international: "",
            phone_number_code_2: "",
            phone_number_2_format_international: "",
        },
        staffId: 0,

        staff: {
            staff_number: "",
            names: "",
            surnames: "",
            phone_number_1: "",
            phone_number_code_1: "",
            phone_number_1_format_international: "",
            phone_number_2: "",
            phone_number_code_2: "",
            phone_number_2_format_international: "",
            earnings: 0,
            area: 0,
            position: 0,
            headquarter: 0,
        },
        staffState: {
            staff_number: null,
            names: null,
            surnames: null,
            phone_number_1: null,
            phone_number_2: null,
            earnings: null,
            area: null,
            position: null,
            headquarter: null,
        },

        areas: [],
        positions: [],
        headquarters: [],
        phone_number_1_props: {
            props: {
                countryCode: "",
                defaultCountryCode: "VE",
                isValid: true,
                error: false,
                formatInternational: "",
            },
        },
        phone_number_2_props: {
            props: {
                countryCode: "",
                defaultCountryCode: "VE",
                isValid: true,
                error: false,
                formatInternational: "",
            },
        },
        show_modal_bulk_upload: false,
        downloadBulkUploadTemplate: false,
        spinnerDownloadBulkUploadTemplate: false,
        bulkUploadTemplate: {
            template: null,
        },
        bulkUploadTemplateState: {
            template: null,
        },
    }),
    mounted() {
        this.getStaffs();
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
        onUpdateNumber1(payload) {
            //console.log("payload");
            //console.log(payload);
            this.phone_number_1_props.props.countryCode = payload.countryCode;
            this.phone_number_1_props.props.isValid = payload.isValid;
            this.phone_number_1_props.props.formatInternational =
                payload.formatInternational;
        },
        onUpdateNumber2(payload) {
            this.phone_number_2_props.props.countryCode = payload.countryCode;
            this.phone_number_2_props.props.isValid = payload.isValid;
            this.phone_number_2_props.props.formatInternational =
                payload.formatInternational;
        },
        async getAreas() {
            this.areas = [];
            axios
                .get(`${SERVER_ADDRESS}/api/config/areas/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.areas = res.data;
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
        async getPositions() {
            this.positions = [];
            axios
                .get(`${SERVER_ADDRESS}/api/config/positions/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.positions = res.data;
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
        async getHeadquarters() {
            this.headquarters = [];
            axios
                .get(`${SERVER_ADDRESS}/api/config/headquarters/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.headquarters = res.data;
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
        async getStaffs() {
            this.loading = true;
            this.staffs = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/staffs/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.staffs = res.data;
                    this.loading = false;

                    // Mientras tanto vamos cargando los elementos de los formularios
                    this.getAreas();
                    this.getPositions();
                    this.getHeadquarters();
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
                value: null,
                matchMode: FilterMatchMode.CONTAINS,
            };
        },

        /**
         * Validar formularios
         */
        checkFormValidity() {
            let valid = true;
            if (!this.staff.names) {
                this.staffState.names = false;
                valid = false;
            }
            if (!this.staff.surnames) {
                this.staffState.surnames = false;
                valid = false;
            }
            if (!this.staff.staff_number) {
                this.staffState.staff_number = false;
                valid = false;
            }
            if (!this.staff.phone_number_1) {
                this.phone_number_1_props.props.error = true;
                this.staffState.phone_number_1 = false;
                valid = false;
            }

            /**
             * En caso de que el teléfono no cumpla el formato adecuado
             */
            if (!this.phone_number_1_props.props.isValid) {
                this.phone_number_1_props.props.error = true;
                this.staffState.phone_number_1 = false;
                valid = false;
            }
            if (
                !this.phone_number_2_props.props.isValid &&
                this.staff.phone_number_2
            ) {
                this.phone_number_2_props.props.error = true;
                this.staffState.phone_number_2 = false;
                valid = false;
            }

            if (this.staff.earnings < 0) {
                this.staffState.earnings = false;
                valid = false;
            }
            if (this.staff.area == 0) {
                this.staffState.area = false;
                valid = false;
            }
            if (this.staff.position == 0) {
                this.staffState.position = false;
                valid = false;
            }
            if (this.staff.headquarter == 0) {
                this.staffState.headquarter = false;
                valid = false;
            }
            return valid;
        },
        resetModal() {
            this.staff.names = "";
            this.staffState.names = null;
            this.staff.surnames = "";
            this.staffState.surnames = null;
            this.staff.staff_number = "";
            this.staffState.staff_number = null;
            this.staff.earnings = 0;
            this.staffState.earnings = null;
            this.staff.area = 0;
            this.staffState.area = null;
            this.staff.position = 0;
            this.staffState.position = null;
            this.staff.headquarter = 0;
            this.staffState.headquarter = null;
            this.staff.phone_number_1 = "";
            this.phone_number_1_props.props.error = false;
            this.staffState.phone_number_1 = null;
            this.staff.phone_number_2 = "";
            this.phone_number_2_props.props.error = false;
            this.staffState.phone_number_2 = null;
        },

        /**
         * Detail
         */
        async show_modal_detail(id) {
            this.staffDetail = {
                staff_number: "",
                names: "",
                surnames: "",
                earnings: 0,
                area_name: "",
                position_name: "",
                headquarter_name: "",
                headquarter_city: "",
                headquarter_parish: "",
                headquarter_township: "",
                headquarter_state: "",
                user_email: "",
                phone_number_code_1: "",
                phone_number_1_format_international: "",
                phone_number_code_2: "",
                phone_number_2_format_international: "",
            };

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/staff/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.staffDetail = res.data;

                    this.$nextTick(() => {
                        this.$bvModal.show("modal-detail");
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

        /**
         * Create
         */
        handleSubmitCreate() {
            // Inicializamos variables de estados
            this.staffState.names = null;
            this.staffState.surnames = null;
            this.staffState.staff_number = null;
            this.staffState.earnings = null;
            this.staffState.area = null;
            this.staffState.position = null;
            this.staffState.headquarter = null;
            this.phone_number_1_props.props.error = false;
            this.staffState.phone_number_1 = null;
            this.phone_number_2_props.props.error = false;
            this.staffState.phone_number_2 = null;

            console.log("Staff");
            console.log(this.staff);
            console.log(this.phone_number_1_props);

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-create");
            });
        },
        async createStaff() {
            // Se le agregar los códigos de teléfono
            this.staff.phone_number_code_1 =
                this.phone_number_1_props.props.countryCode;
            this.staff.phone_number_1_format_international =
                this.phone_number_1_props.props.formatInternational;
            this.staff.phone_number_code_2 =
                this.phone_number_2_props.props.countryCode;
            this.staff.phone_number_2_format_international =
                this.phone_number_2_props.props.formatInternational;
            // Validar de que si se dejó vacío el campo de ganancia entonces se coloca cero
            if (!this.staff.earnings) {
                this.staff.earnings = 0;
            }
            axios
                .post(`${SERVER_ADDRESS}/api/phase2/staffs/`, this.staff, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡El personal ha sido creado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-create");
                        this.$bvModal.hide("modal-create");
                    });

                    // Cargamos de nuevo la tabla de riesgos
                    this.getStaffs();
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
         * Update
         */
        handleSubmitUpdate() {
            // Inicializamos variables de estados
            this.staffState.names = null;
            this.staffState.surnames = null;
            this.staffState.staff_number = null;
            this.staffState.earnings = null;
            this.staffState.area = null;
            this.staffState.position = null;
            this.staffState.headquarter = null;
            this.phone_number_1_props.props.error = false;
            this.staffState.phone_number_1 = null;
            this.phone_number_2_props.props.error = false;
            this.staffState.phone_number_2 = null;

            // Exit when the form isn't valid
            if (!this.checkFormValidity()) {
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-update");
            });
        },
        async show_modal_update(id) {
            this.staffId = id;

            this.staffState.names = null;
            this.staffState.surnames = null;
            this.staffState.staff_number = null;
            this.staffState.earnings = null;
            this.staffState.area = null;
            this.staffState.position = null;
            this.staffState.headquarter = null;
            this.phone_number_1_props.props.error = false;
            this.staffState.phone_number_1 = null;
            this.phone_number_2_props.props.error = false;
            this.staffState.phone_number_2 = null;

            axios
                .get(`${SERVER_ADDRESS}/api/phase2/staff/${id}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.staff = res.data;

                    if (res.data.phone_number_code_1) {
                        this.phone_number_1_props.props.countryCode =
                            res.data.phone_number_code_1;
                        this.phone_number_1_props.props.defaultCountryCode =
                            res.data.phone_number_code_1;
                    }
                    if (res.data.phone_number_code_2) {
                        this.phone_number_2_props.props.countryCode =
                            res.data.phone_number_code_2;
                        this.phone_number_2_props.props.defaultCountryCode =
                            res.data.phone_number_code_2;
                    }

                    this.$nextTick(() => {
                        this.$bvModal.show("modal-update");
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
        async updateStaff() {
            this.staff.phone_number_code_1 =
                this.phone_number_1_props.props.countryCode;
            this.staff.phone_number_1_format_international =
                this.phone_number_1_props.props.formatInternational;
            this.staff.phone_number_code_2 =
                this.phone_number_2_props.props.countryCode;
            this.staff.phone_number_2_format_international =
                this.phone_number_2_props.props.formatInternational;
            // Validar de que si se dejó vacío el campo de ganancia entonces se coloca cero
            if (!this.staff.earnings) {
                this.staff.earnings = 0;
            }
            axios
                .patch(
                    `${SERVER_ADDRESS}/api/phase2/staff/${this.staffId}/`,
                    this.staff,
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
                        "¡El personal ha sido actualizado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-update");
                        this.$bvModal.hide("modal-update");
                    });

                    this.getStaffs();
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
         * Delete
         */
        show_modal_delete(id) {
            this.staffId = id;
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-delete");
            });
        },
        async deleteStaff() {
            axios
                .delete(`${SERVER_ADDRESS}/api/phase2/staff/${this.staffId}/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡El personal ha sido eliminado exitosamente!"
                    );

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-delete");
                    });

                    this.getStaffs();
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
         * Download bulk upload template
         */
        async getBulkUploadTemplate() {
            this.downloadBulkUploadTemplate = true;
            this.spinnerDownloadBulkUploadTemplate = true;

            axios
                .get(
                    `${SERVER_ADDRESS}/api/phase2/staff/bulk_upload_template/`,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                    }
                )
                .then((res) => {
                    this.downloadBulkUploadTemplate = false;
                    this.spinnerDownloadBulkUploadTemplate = false;

                    saveAs(res.config.url);
                })
                .catch((err) => {
                    this.downloadBulkUploadTemplate = false;
                    this.spinnerDownloadBulkUploadTemplate = false;
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
         * Bulk Upload staff
         */
        handleSubmitBulkUploadStaff() {
            // Inicializamos variables de estados
            this.bulkUploadTemplateState.template = null;

            // Exit when the form isn't valid

            if (!this.bulkUploadTemplate.template) {
                this.bulkUploadTemplateState.template = false;
                return;
            }

            // Mostrar modal de confirmar
            this.$nextTick(() => {
                this.$bvModal.show("modal-confirm-bulk-upload");
            });
        },
        async bulkUploadStaff() {
            let formData = new FormData();
            formData.append(
                "template",
                this.bulkUploadTemplate.template,
                this.bulkUploadTemplate.template.name
            );

            axios
                .post(
                    `${SERVER_ADDRESS}/api/phase2/staff_bulk_upload/bulk_upload/`,
                    formData,
                    {
                        withCredentials: true,
                        headers: {
                            Authorization: TOKEN,
                        },
                        responseType: "blob",
                    }
                )
                .then((res) => {
                    // Mensaje de éxito
                    this.successMessage(
                        "¡El personal de la organización ha sido cargado exitosamente!"
                    );
                    this.getStaffs();

                    //Ocultamos los modales
                    this.$nextTick(() => {
                        this.$bvModal.hide("modal-confirm-bulk-upload");
                        this.$bvModal.hide("modal-bulk-upload");
                    });
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            this.errorMessage(
                                "El documento contiene errores, por favor verificar el mismo"
                            );
                            saveAs(err.response.data, "error_response.xlsx");
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
