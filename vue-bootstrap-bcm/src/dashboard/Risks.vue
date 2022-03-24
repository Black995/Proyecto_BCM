<template>
    <div class="container-fluid">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body table-responsive">
                        <DataTable
                            class="header-table"
                            :value="risks"
                            responsiveLayout="scroll"
                            :paginator="true"
                            :rows="10"
                            :rowsPerPageOptions="[10, 20]"
                            currentPageReportTemplate="Showing {first} to {last} of {totalRecords}"
                            :resizableColumns="true"
                            :autoLayout="true"
                            :responsive="true"
                            :reorderableColumns="true"
                            :lazy="true"
                            :loading="loading"
                            filterDisplay="row"
                            :globalFilterFields="['name', 'description']"
                        >
                            <template #header>
                                <div class="flex justify-content-between">
                                    <button
                                        class="btn-success btn mr-3"
                                        @click="open_modal_create()"
                                    >
                                        <i class="fas fa-plus"></i>
                                    </button>
                                    <span class="p-input-icon-left">
                                        <i class="pi pi-search" />
                                        <InputText
                                            v-model="filterGlobal"
                                            placeholder="Buscar..."
                                        />
                                    </span>
                                </div>
                            </template>
                            <Column field="name" header="Nombre"></Column>
                            <Column
                                field="description"
                                header="Descripción"
                            ></Column>

                            <template #empty> No customers found. </template>
                        </DataTable>
                    </div>
                    <!-- /.card-body -->
                </div>
                <!-- /.card -->
            </div>
            <!-- /.col -->
        </div>
        <!-- /.row -->
    </div>
</template>

<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../config/config";
import { FilterMatchMode } from "primevue/api";

export default {
    name: "Risks",

    data: () => ({
        loading: false,
        filterGlobal: null,

        risks: [],
        deleteRiskId: 0,
    }),
    mounted() {
        this.getRisks();
    },
    methods: {
        async getRisks() {
            this.loading = true;
            this.risks = [];

            axios
                .get(`${SERVER_ADDRESS}/api/phase1/risks/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.risks = res.data;
                    this.loading = false;
                })
                .catch((err) => {
                    try {
                        // Error 400 por unicidad o 500 generico
                        if (err.response.status == 400) {
                            console.log(err.response.data);
                            //this.mensajeError = err.response.data;
                            //this.snackbar = true;
                        } else {
                            console.log(
                                "Ups! Ha ocurrido un error en el servidor"
                            );
                            // Servidor no disponible
                            //this.mensajeError = "Ups! Ha ocurrido un error en el servidor";
                            //this.snackbar = true;
                        }
                    } catch {
                        // Servidor no disponible
                        console.log("Ups! Ha ocurrido un error en el servidor");
                        //this.mensajeError = "Ups! Ha ocurrido un error en el servidor";
                        //this.snackbar = true;
                    }
                });
        },
        open_modal_create() {},

        clearFilter1() {
            this.initFilters1();
        },
        initFilters1() {
            this.filterGlobal = {
                value: null,
                matchMode: FilterMatchMode.CONTAINS,
            };
        },
    },
};
</script>

<style lang="scss">
.header-table {
    background-color: rgb(17, 17, 17);
    color: rgb(255, 255, 255);
}
</style>