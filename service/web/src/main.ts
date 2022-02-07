import { createApp } from 'vue'
import App from '/@/App.vue'

import 'element-plus/dist/index.css'
import ElementPlus from 'element-plus'

import { router } from '/@/store/router'

const app = createApp(App)
app.use(ElementPlus)
app.use(router)
app.mount('#app')

