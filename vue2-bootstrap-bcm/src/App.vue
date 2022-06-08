<template>
    <!--
        Se coloca la clase 'login' cuando la vista actual sea el Login, con el fin de poder colocar 
        el fondo de pantalla del login
    -->
    <div
        :class="{
            'nav-open': $sidebar.showSidebar,
            login: $route.name == 'Login',
        }"
    >
        <notifications></notifications>
        <router-view></router-view>
    </div>
</template>


<script>
export default {
    name: "App",

    data: () => ({
        loginActive: false,
    }),

    mounted() {
        console.log("ruta actual");
        console.log(this.$route.name);
    },
    methods: {},
};
</script>

<!-- Librería para el multiselect -->
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="scss">
.login {
    background-image: url("./assets/img/business_image.jpg");
    background-repeat: no-repeat;
    /* Full height */
    height: 100%;
    width: 100%;
    background-size: cover;
}

.vue-notifyjs.notifications {
    .alert {
        z-index: 10000;
    }
    .list-move {
        transition: transform 0.3s, opacity 0.4s;
    }
    .list-item {
        display: inline-block;
        margin-right: 10px;
    }
    .list-enter-active {
        transition: transform 0.2s ease-in, opacity 0.4s ease-in;
    }
    .list-leave-active {
        transition: transform 1s ease-out, opacity 0.4s ease-out;
    }

    .list-enter {
        opacity: 0;
        transform: scale(1.1);
    }
    .list-leave-to {
        opacity: 0;
        transform: scale(1.2, 0.7);
    }
}
</style>
