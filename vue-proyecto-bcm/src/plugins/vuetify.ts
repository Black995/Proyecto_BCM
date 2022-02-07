import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'
import es from 'vuetify/src/locale/es'

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
				secondary: '#26964b',
			},
			//Modo dark del fondo de pantalla
			dark: {},
		},
	},
	lang: {
		locales: { es },
		current: 'es'
	}
})
