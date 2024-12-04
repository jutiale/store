<!-- <script setup>
import { ref } from 'vue'

const categories = ref(null)



async function fetchData() {
  const res = await fetch(
    `http://localhost:8000/categories/?skip=0&limit=100`
  )
  categories.value = await res.json()

  // for (const good of goods.value) {
  //   const res = await fetch(`http://localhost:8000/categories/` + good.id + `/images`)
  //   good.images = await res.json()
  //   console.log(good.images)
  // }
} -->
<!-- 

fetchData()
</script> -->

<template>
  <div class="Categories">
    <v-app>
      <Navbar />
      <div class="mt-4 m-3" v-if="currentUser">
          <AddCategoryPopup @onCategoryAdded="fetchData" v-if="currentUser.userRole == 2 || currentUser.userRole == 3"/>
      </div>


      <v-container>
        <v-row>
          <v-col cols="4" v-for="category in categories" :key="category.id">
            <v-card variant="outlined">
              <v-card-title class="text-center">{{ category.name }}</v-card-title>
              <v-card-actions class="justify-center" v-if="currentUser">
                <div v-if="currentUser.userRole == 2 || currentUser.userRole == 3">
                  <UpdateCategoryPopup @onCategoryUpdated="fetchData" :category="category" />
                  <DeleteCategoryPopup @onCategoryDeleted="fetchData" :category="category" />
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
import AddCategoryPopup from '@/components/AddCategoryPopup'
import UpdateCategoryPopup from '@/components/UpdateCategoryPopup'
import DeleteCategoryPopup from '@/components/DeleteCategoryPopup.vue'

export default {
  components: { Navbar, AddCategoryPopup, UpdateCategoryPopup, DeleteCategoryPopup },
  name: 'Categories',
  setup() {
    let categories = ref(null);
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
        `http://localhost:8000/categories/?skip=` + (page.value - 1) * 6 + `&limit=6`
      )
      categories.value = res.data.categories
      total.value = res.data.total
      pagination.perPage = res.data.onPage
    }

    fetchData()

    return {
      categories,
      pagination,
      page,
      total,
      fetchData
    }
  },
  computed: {
    currentUser() {
      return this.$store.state.user;
    },
    visibleCount() {
      pageCount = Math.ceil(this.total / 6);
      if (pageCount > 7) {
        return 7;
      }
      if (pageCount < 2) {
        return 1;
      }
      return pageCount
    },
  },


}
</script>
