<template>
    <body class="hold-transition sidebar-mini layout-fixed">
        <div class="wrapper">
            <Navbar></Navbar>
            <Sidebar></Sidebar>

            <div class="content-wrapper">
                <ContentHeader></ContentHeader>

                <section class="content">
                    <div class="container-fluid">
                        <!--ExampleForm></ExampleForm-->
                        <router-view />
                    </div>
                </section>
            </div>

            <!--Footer></Footer-->
            <ControlSidebar></ControlSidebar>
        </div>
    </body>
</template>

<script>
import $ from "jquery";
import "../../node_modules/admin-lte/plugins/select2-bootstrap4-theme/select2-bootstrap4.min.css";
import "../../node_modules/admin-lte/plugins/select2/css/select2.min.css";

import ContentHeader from "./ContentHeader.vue";
//import ExampleForm from "../components/ExampleForm.vue";
import Navbar from "./Navbar.vue";
import Sidebar from "./Sidebar.vue";
//import Footer from "./Footer.vue";
import ControlSidebar from "./ControlSidebar.vue";

export default {
    name: "Dashboard",
    components: {
        ContentHeader,
        //ExampleForm,
        Navbar,
        Sidebar,
        //Footer,
        ControlSidebar,
    },
    methods: {
        initializeSelect2() {
            //Initialize Select2 Elements
            $(".select2").select2();

            //Initialize Select2 Elements
            $(".select2bs4").select2({
                theme: "bootstrap4",
            });
        },
    },
    mounted() {
        this.initializeSelect2();
    },
};
</script>

<style>
@import url("https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,400i,700&display=fallback");
</style>
