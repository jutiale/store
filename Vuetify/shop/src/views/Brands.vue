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
  <div class="Brands">
    <v-app>
      <Navbar />
      <div class="mt-4 m-3">
        <AddBrandPopup @onBrandAdded="fetchData" v-if="currentUser?.userRole == 2 || currentUser?.userRole == 3"/>
      </div>


      <v-container>
        <v-row>
          <v-col cols="4" v-for="brand in brands" :key="brand.id">
            <v-card variant="outlined">
              <v-card-title class="text-center">{{ brand.name }}</v-card-title>
              <v-card-actions class="justify-center" v-if="currentUser">
                <div v-if="currentUser.userRole == 2 || currentUser.userRole == 3">
                  <UpdateBrandPopup @onBrandUpdated="fetchData" :brand="brand" />
                  <DeleteBrandPopup @onBrandDeleted="fetchData" :brand="brand" />
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



<!-- <script>
export default {
  data() {
    return {
      drawer: false
    }
  }
}
</script> -->

<script>
import { ref } from 'vue'
import axios from 'axios'
import Navbar from '@/components/Navbar'
import AddBrandPopup from '@/components/AddBrandPopup'
import UpdateBrandPopup from '@/components/UpdateBrandPopup'
import DeleteBrandPopup from '@/components/DeleteBrandPopup.vue'

export default {
  components: { Navbar, AddBrandPopup, UpdateBrandPopup, DeleteBrandPopup },
  name: 'App',
  computed: {
    currentUser() {
      return this.$store.state.user;
    },
  },
  setup() {
    let brands = ref(null);
    const page = ref(1);
    const total = ref(0);
    let pagination = {
      // page: 1,
      // total: 0,
      perPage: 0,
      visible: 7
    }

    async function fetchData() {

      const res = await axios.get(
        `http://localhost:8000/brands/?skip=` + (page.value - 1) * 6 + `&limit=6`
      )
      brands.value = res.data.brands
      total.value = res.data.total
      pagination.perPage = res.data.onPage
    }

    fetchData()

    return {
      brands,
      pagination,
      page,
      total,
      fetchData
    }
  },

}
</script>
