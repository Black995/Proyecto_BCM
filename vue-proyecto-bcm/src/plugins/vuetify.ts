import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'

Vue.use(Vuetify)

export default new Vuetify({
	theme: {
		options: {
			customProperties: true,
		},
		themes: {
			//Modo light del fondo de pantalla
			light: {
				primary: '#00b050',
				secondary: '#35B39C',
			},
			//Modo dark del fondo de pantalla
			dark: {},
		},
	},
})
