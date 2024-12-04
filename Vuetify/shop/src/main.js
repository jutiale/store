import "vue-toastification/dist/index.css";
import App from './App.vue'
import router from './router';
import Toast from "vue-toastification";
import { createApp } from 'vue'
import { registerPlugins } from '@/plugins'
import { store } from './store'

const app = createApp(App).use(router).use(store);

registerPlugins(app)

app.mount('#app')

const options = {

};

app.use(Toast, options);

