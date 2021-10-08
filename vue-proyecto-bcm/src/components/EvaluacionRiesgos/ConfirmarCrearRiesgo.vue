<template>
	<v-row justify="center">
		<v-dialog v-model="dialog" persistent max-width="290">
			<template v-slot:activator="{ on, attrs }">
				<v-btn color="primary" dark v-bind="attrs" v-on="on">
					Open Dialog
				</v-btn>
			</template>
			<v-card>
				<v-card-title class="text-h5">
					¿Está seguro de crear este riesgo?
				</v-card-title>
				<v-card-actions>
					<v-spacer></v-spacer>
					<v-btn
						color="primary darken-1"
						text
						@click="dialog = false"
					>
						Cerrar
					</v-btn>
					<v-btn color="primary" text @click="dialog = false">
						Confirmar
					</v-btn>
				</v-card-actions>
			</v-card>
		</v-dialog>
	</v-row>
</template>


<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
	data: () => ({
		dialog: false,
	}),
})
</script>

