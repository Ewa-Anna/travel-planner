import { registerPlugins } from '@/plugins'
import App from './App.vue'
import router from './router'
import axios from 'axios'
import { createApp } from 'vue'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
  fab,
  faFacebook,
  faGithub,
  faLinkedin,
  faInstagram,
  faYoutube
} from '@fortawesome/free-brands-svg-icons'

const DEV_URL = 'http://127.0.0.1:8000'
axios.defaults.baseURL = DEV_URL
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

library.add(fab, faFacebook, faGithub, faLinkedin, faInstagram, faYoutube)

/* eslint-disable @typescript-eslint/no-unsafe-argument */
const app = createApp(App)

app.component('font-awesome-icon', FontAwesomeIcon)

registerPlugins(app)

app.use(router)
app.mount('#app')
