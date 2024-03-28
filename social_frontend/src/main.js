import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import axios  from 'axios'

const app = createApp(App)

// axios.defaults.baseURL ='http://127.0.0.1:8000'
axios.defaults.baseURL = import.meta.env.VITE_API_URL

app.use(createPinia())
app.use(router, axios)

app.mount('#app')
