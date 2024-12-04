<!-- <script setup>
import { ref } from 'vue'

const brands = ref(null)



async function fetchData() {
  const res = await fetch(
    `http://localhost:8000/brands/?skip=0&limit=100`
  )
  brands.value = await res.json()

}


fetchData()
</script> -->

<template>
  <div class="Users">
    <v-app>
      <Navbar />
      <div class="mt-4 m-3">
        <AddUserPopup @onUserAdded="fetchData" />
      </div>


      <v-container>
        <v-row>
          <v-col cols="4" v-for="user in users" :key="user.id">
            <v-card variant="outlined" prepend-icon="mdi-account">
              <v-card-title class="text-center">{{ user.name }}</v-card-title>
              <v-card-title primary-title class="text-center">
                <p>Эл. почта: {{ user.email }}</p>
                <p>Роль: {{ roles[user.role] }}</p>
              </v-card-title>
              <v-card-actions class="justify-center" v-if="currentUser">
                <div v-if="currentUser.userRole == 3">
                  <UpdateUserPopup @onUserUpdated="fetchData" :user="user" />
                  <DeleteUserPopup @onUserDeleted="fetchData" :user="user" />
                </div>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
      <div class="text-center">
        <v-pagination v-model="page" :length="Math.ceil(total / 6)" @click="fetchData"
          :total-visible="Math.ceil(total.value / 6) < 7 ? Math.ceil(total.value / 6) : 7"></v-pagination>
      </div>
    </v-app>
  </div>
</template>


<script>
import { ref } from 'vue'
import axios from 'axios'
import Navbar from '@/components/Navbar'
import AddUserPopup from '@/components/AddBrandPopup'
import UpdateUserPopup from '@/components/UpdateUserPopup'
import DeleteUserPopup from '@/components/DeleteUserPopup.vue'


export default {
  components: { Navbar, AddUserPopup, UpdateUserPopup, DeleteUserPopup },
  name: 'App',
  computed: {
    currentUser() {
      return this.$store.state.user;
    },
  },
  data() {
    return {
      roles: {
        "1": "Обычный пользователь",
        "2": "Менеджер",
        "3": "Администратор"
      }
    }
  },
  setup() {
    let users = ref(null);
    const page = ref(1);
    const total = ref(0);
    let pagination = {
      // page: 1,
      // total: 0,
      perPage: 0,
      visible: 7
    }

    async function fetchData() {
      const token = localStorage.getItem('currentUserToken');

      const res = await axios.get(
        `http://localhost:8000/users/?skip=` + (page.value - 1) * 6 + `&limit=6`,
        { headers: { "Authorization": `Bearer ${token}` } }
      )
      users.value = res.data.users
      total.value = res.data.total
      pagination.perPage = res.data.onPage
    }

    fetchData()

    return {
      users,
      pagination,
      page,
      total,
      fetchData
    }
  },

}
</script>