<script setup>
import { ref } from 'vue'

</script>

<template>

  <nav>

    <v-toolbar flat app>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>Магазин</v-toolbar-title>


      <v-spacer></v-spacer>

      <!-- <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>mdi-heart</v-icon>
      </v-btn> -->

      <div v-if="currentUser" class="d-flex align-center">
        <div style="text-align:center">
          <span class="ml-4 mr-4 text-overline font-weight-black">{{ currentUser.userName }}</span>
        </div>
        <div class="ma-2 pa-2 d-flex">
          <v-btn @click="logout" class="mr-4" variant="elevated" title="Выйти">
            <v-icon>mdi-export</v-icon>
            Выйти
          </v-btn>
        </div>
      </div>

      <div v-else>
        <router-link to="/login" style="text-decoration: none; color: inherit;">
          <v-btn title="Войти" variant="elevated" class="mr-4">
            <v-icon>mdi-export</v-icon>
            Войти
          </v-btn>
        </router-link>
      </div>

    </v-toolbar>



  </nav>
  <v-navigation-drawer app temporary v-model="drawer">

    <v-list-item title="Магазин"></v-list-item>
    <v-divider></v-divider>
    <router-link to="/goods" style="text-decoration: none; color: inherit;"><v-list-item link
        title="Товары"></v-list-item></router-link>
    <router-link to="/categories" style="text-decoration: none; color: inherit;"><v-list-item link
        title="Категории"></v-list-item></router-link>
    <router-link to="/brands" style="text-decoration: none; color: inherit;"><v-list-item link
        title="Бренды"></v-list-item></router-link>
    <div v-if="currentUser && currentUser.userRole == 3">
      <router-link to="/users" style="text-decoration: none; color: inherit;"><v-list-item link
          title="Пользователи"></v-list-item></router-link>
    </div>
    <div v-if="currentUser">
      <router-link to="/cart" style="text-decoration: none; color: inherit;"><v-list-item link
          title="Корзина"></v-list-item></router-link>
    </div>
  </v-navigation-drawer>

</template>



<script>
import { authenticationService } from '@/services/authenticationService';

export default {
  name: "App",
  setup() {

  },
  data() {
    return {
      drawer: false,
      // currentUser: authenticationService.currentUserValue,
      // currentUser: '',
      links: [
        { text: 'Goods', route: '/' },
        { text: 'Categories', route: '/categories' }
      ]
    }
  },
  computed: {
    currentUser() {
      return this.$store.state.user;
    },
    isAdmin() {
      return this.currentUser.value && this.currentUser.value.role === Role.Admin;
    }
  },
  created() {
    //console.log(this.currentUser);
    // console.log(authenticationService.getCurrentUser())
    //this.currentUser.value = authenticationService.getCurrentUser();
    // authenticationService.currentUser.subscribe(x => this.currentUser = x);
    console.log(this.currentUser);
  },
  methods: {
    logout() {
      authenticationService.logout();
      this.$store.commit('deleteUser');
    },
  }
}

</script>

<style>
.align-center {
  align-items: center;
}
</style>
