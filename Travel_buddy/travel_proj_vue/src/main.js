import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'/* tells vue to use axios */

axios.defaults.baseURL = 'http://127.0.0.1:8000'

createApp(App).use(store).use(router).mount('#app')
