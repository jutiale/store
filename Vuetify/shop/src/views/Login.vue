<template>
  <div class="Auth">

    <Navbar />
    <p class="mt-10 mb-10 text-center text-h5">Войдите в свой аккаунт</p>
    <v-card variant="outlined" align-self="center" class="ma-auto mt-10 px-6 py-8" max-width="344">
      <v-form v-model="form" @submit.prevent="login">
        <v-text-field v-model="email" class="mb-2" label="Эл. почта" clearable></v-text-field>

        <v-text-field v-model="password" type="password" label="Пароль" clearable></v-text-field>

        <br>

        <v-btn :disabled="!form" size="large" type="submit" variant="elevated" block>
          Войти
        </v-btn>
      </v-form>
    </v-card>
    <!-- <v-snackbar v-model="snackbar" vertical>
      <div class="text-subtitle-1 pb-2">Оформлен новый заказ</div>

      <textarea v-model="message">{{ message }}</textarea>

      <template v-slot:actions>
        <v-btn color="indigo" variant="text" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar> -->
  </div>
</template>

<script>
import axios from 'axios'
import { useToast, POSITION } from 'vue-toastification'
import Navbar from '@/components/Navbar'
import { authenticationService } from '@/services/authenticationService';
import { router } from '@/router';


const toast = useToast()

export default {
  data() {
    return {
      dialog: false,
      backgroundcolor: "#16a085",
      form: '',
      password: '',
      returnUrl: '',
      email: '',
      name: 'Auth',
      user: '',

    }
  },
  created() {
    if (authenticationService.currentUserValue) {
      return router.push('/');
    }
  },
  components: { Navbar },
  methods: {
    login() {
      authenticationService.login(this.email, this.password).then(() => {
        let user = authenticationService.getCurrentUser();
        this.$store.commit('setUser', user);
        router.push('/');
        if (user.userRole == 2) {
          const socket = new WebSocket("ws://localhost:8000/ws?token=" + localStorage.getItem('currentUserToken'));
          socket.onmessage = function (event) {
            let data = JSON.parse(event.data);
            console.log(data);
            toast.info("Пользователь " + data.user_name + " оформил \nзаказ на сумму " + data.total_price + " руб.", 
            { timeout: 10000, position: POSITION.BOTTOM_LEFT });
          };
        }
      });
    },
  }
}


</script>

<style>
#wrapper:fullscreen {
  width: 100vw;
  height: 100vh;
  color: aqua;
}
</style>