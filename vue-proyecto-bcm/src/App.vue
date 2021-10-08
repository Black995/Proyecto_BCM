<template>
	<v-app class="v-application">
		<router-view />
	</v-app>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
	name: 'App',

	data: () => ({
		//
	}),
})
</script>

<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Varta:wght@600&display=swap');

$font-family: 'Varta';

body {
	background: #f1f1f1;
}
.v-application {
	font-family: $font-family;
}
</style>