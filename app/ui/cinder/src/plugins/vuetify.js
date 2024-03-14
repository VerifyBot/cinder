/**
 * plugins/vuetify.js
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'

import * as components from 'vuetify/components'
import * as labsComponents from 'vuetify/labs/components'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides

const cinderDark = {
  dark: true,
  colors: {
    background: '#1f222e',
    surface: '#1f222e',
    primary: '#1f222e',
    'primary-darken-1': '#eb4d4b',
    secondary: '#03DAC6',
    'secondary-darken-1': '#018786',
    error: '#e2777a',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FB8C00',
  },
}


export default createVuetify({
  theme: {
    defaultTheme: 'cinderDark',
    themes: {
      cinderDark,
    },
  },
  components: {
    ...components,
    ...labsComponents,
  },
})
