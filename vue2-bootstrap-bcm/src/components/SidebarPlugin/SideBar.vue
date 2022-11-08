<template>
    <div
        class="sidebar"
        :data-background-color="backgroundColor"
        :data-active-color="activeColor"
    >
        <!--
            Tip 1: you can change the color of the sidebar's background using: data-background-color="white | black | darkblue"
            Tip 2: you can change the color of the active button using the data-active-color="primary | info | success | warning | danger"
        -->
        <!-- -->
        <div class="sidebar-wrapper" id="style-3">
            <div class="logo">
                <a href="#" class="simple-text">
                    <div v-if="logo_img" class="logo-img">
                        <!--div class="logo-img"-->
                        <img
                            :src="'data:image/jpeg;base64,' + logo_img"
                            alt=""
                        />
                    </div>
                    {{ title }}
                </a>
            </div>
            <slot> </slot>
            <ul class="nav">
                <!--By default vue-router adds an active class to each route link. This way the links are colored when clicked-->
                <slot name="links">
                    <sidebar-link
                        v-for="(link, index) in sidebarLinks"
                        :key="index"
                        :to="link.path"
                        :name="link.name"
                        :icon="link.icon"
                    >
                    </sidebar-link>
                </slot>
            </ul>
            <moving-arrow :move-y="arrowMovePx"> </moving-arrow>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { SERVER_ADDRESS, TOKEN } from "../../../config/config";

import MovingArrow from "./MovingArrow.vue";
import SidebarLink from "./SidebarLink";
export default {
    props: {
        title: {
            type: String,
            default: "Proyecto BCM",
        },
        backgroundColor: {
            type: String,
            default: "black",
            validator: (value) => {
                let acceptedValues = ["white", "black", "darkblue"];
                return acceptedValues.indexOf(value) !== -1;
            },
        },
        activeColor: {
            type: String,
            default: "success",
            validator: (value) => {
                let acceptedValues = [
                    "primary",
                    "info",
                    "success",
                    "warning",
                    "danger",
                ];
                return acceptedValues.indexOf(value) !== -1;
            },
        },
        sidebarLinks: {
            type: Array,
            default: () => [],
        },
        autoClose: {
            type: Boolean,
            default: true,
        },
    },
    provide() {
        return {
            autoClose: this.autoClose,
            addLink: this.addLink,
            removeLink: this.removeLink,
        };
    },
    components: {
        MovingArrow,
        SidebarLink,
    },
    computed: {
        /**
         * Styles to animate the arrow near the current active sidebar link
         * @returns {{transform: string}}
         */
        arrowMovePx() {
            return this.linkHeight * this.activeLinkIndex;
        },
    },
    data() {
        return {
            linkHeight: 65,
            activeLinkIndex: 0,
            windowWidth: 0,
            isWindows: false,
            hasAutoHeight: false,
            links: [],
            logo_img: null,
        };
    },
    methods: {
        findActiveLink() {
            this.links.forEach((link, index) => {
                if (link.isActive()) {
                    this.activeLinkIndex = index;
                }
            });
        },
        addLink(link) {
            const index = this.$slots.links.indexOf(link.$vnode);
            this.links.splice(index, 0, link);
        },
        removeLink(link) {
            const index = this.links.indexOf(link);
            if (index > -1) {
                this.links.splice(index, 1);
            }
        },

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

        async getOrganization() {
            axios
                .get(`${SERVER_ADDRESS}/api/config/organizations/`, {
                    withCredentials: true,
                    headers: {
                        Authorization: TOKEN,
                    },
                })
                .then((res) => {
                    this.logo_img = res.data[0].logo_base64;
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
    mounted() {
        this.$watch("$route", this.findActiveLink, {
            immediate: true,
        });
        this.getOrganization();
    },
};
</script>
<style>
</style>
