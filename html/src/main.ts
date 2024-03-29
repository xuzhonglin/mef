import {createApp} from 'vue'
import App from './App.vue'
import router from './router'

// @ts-ignore
import JsonViewer from 'vue-json-viewer'
import 'element-plus/dist/index.css'

const app = createApp(App)

app.use(router)
app.use(JsonViewer)
app.mount('#app')
