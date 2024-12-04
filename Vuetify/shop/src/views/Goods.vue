<template>
  <div class="Home">
    <v-app>
      <Navbar />
      <div class="mt-4 m-3" v-if="currentUser">
        <div v-if="currentUser.userRole == 3 || currentUser.userRole == 2">
          <AddGoodPopup @onGoodAdded="fetchData" />
        </div>
      </div>

      <v-container>
        <v-row>
          <v-col cols="4" v-for="good in goods" :key="good.id">
            <v-card variant="outlined" link>
              <router-link :to="'/goods/' + good.id" style="text-decoration: none; color: inherit;">
                <v-card-title class="text-center text-h5">{{ good.name }}</v-card-title>
                  <div class="text-center" v-for="(image, i) in good.images" :key="i">
                        <v-avatar size="350" rounded="0"  v-if="i == 0">
                          <v-img :src="'http://localhost:8000/' + image.path" ></v-img>
                        </v-avatar>
                  </div>
                    <div class="d-flex justify-center mb-4 mt-2">
                      <v-chip class="mr-2">{{ good.category.name }}</v-chip>
                      <v-chip class="ml-2">{{ good.brand.name }}</v-chip>
                    </div>
                    <v-card-text align="center" class="text-h6">{{ good.price }} руб.</v-card-text>
              </router-link>
              <v-divider class="mx-4 mb-1" v-if="currentUser"></v-divider>
              <v-spacer></v-spacer>
              <v-card-actions class="justify-center" v-if="currentUser">
                <div>
                  <UpdateGoodPopup v-if="currentUser.userRole == 2 || currentUser.userRole == 3" 
                  @onGoodUpdated="fetchData" :good="good" />
                  <DeleteGoodPopup v-if="currentUser.userRole == 2 || currentUser.userRole == 3" 
                  @onGoodDeleted="fetchData" :good="good" />
                  <AddGoodToCartPopup :good="good" :count="`1`" />
                </div>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
        <div class="text-center">
          <v-pagination v-model="page" :length="Math.ceil(total / 5)" @click="fetchData"
            :total-visible="Math.ceil(total.value / 6) < 7 ? Math.ceil(total.value / 6) : 7"></v-pagination>
        </div>
      </v-container>
      <!-- <v-row class="mx-auto">
        <v-col cols="4" v-for="good in goods" :key="good.id">
          <v-card variant="outlined" max-width="700">
            <v-row>
              <v-col v-for="(image, i) in good.images" :key="i">
                    <v-avatar v-if="i == 0" class="ma-3" rounded="0" size="200">
                      <v-img :src="'http://localhost:8000/' + image.path"></v-img>
                    </v-avatar>
              </v-col>
              <v-col>
                <div >
                  <v-card-title class="text-h6">
                    {{ good.name }}
                  </v-card-title>
                </div>

                <v-chip class="text-subtitle-1 ">{{ good.category.name }}</v-chip>
                <v-chip class="text-subtitle-1 ">{{ good.brand.name }}</v-chip>
                </v-col>
            </v-row> -->
                  
                
            <!-- <v-divider class="mx-4 mb-1"></v-divider>
            <v-card-actions block>
              <v-btn class="ms-2" size="small" text="START RADIO" variant="outlined"></v-btn>
            </v-card-actions> -->



          <!-- </v-card>
        </v-col>
      </v-row> -->
    </v-app>
  </div>
</template>



<script>
import { ref } from 'vue'
import Navbar from '@/components/Navbar'
import AddGoodPopup from '@/components/AddGoodPopup'
import UpdateGoodPopup from '@/components/UpdateGoodPopup'
import DeleteGoodPopup from '@/components/DeleteGoodPopup'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import AddGoodToCartPopup from '@/components/AddGoodToCartPopup.vue'

const toast = useToast()

export default {
  components: { Navbar, AddGoodPopup, UpdateGoodPopup, DeleteGoodPopup, AddGoodToCartPopup },
  name: 'Goods',
  setup() {
    let goods = ref(null);
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
        `http://localhost:8000/goods/?skip=` + (page.value - 1) * 6 + `&limit=6`
      )
      goods.value = res.data.goods
      total.value = res.data.total
      pagination.perPage = res.data.on_page



      for (const good of goods.value) {
        const res = await fetch(`http://localhost:8000/goods/` + good.id + `/images`)
        good.images = await res.json()
      }
    }

    fetchData()

    return {
      goods,
      pagination,
      page,
      total,
      fetchData
    }
  },
  data() {
    return {
      items: [],
    }
  },
  computed: {
    currentUser() {
      return this.$store.state.user;
    },
    pageCount() {
      let l = this.pagination.total;
      return Math.ceil(l / 6);
    },
  },
  methods: {
    deleteGood(id, confirm) {
      if (confirm == true) {
        axios.delete('http://localhost:8000/goods/' + id)
          .then(response => this.checkStatus(response))
          .catch(error => console.log(error))
      }

    },
    checkStatus(response) {
      console.log(response)
      if (response.status == 200) {
        toast.success("Товар успешно удален!");
        const res = fetch(`http://localhost:8000/goods/?skip=0&limit=100`)
        goods.value = res.json()
      }
      else {
        toast.error("Произошла ошибка");
      }
    },
    // nextPage() {
    //   this.fetchData();
    // },
    // prevPage() {
    //   this.fetchData();
    // },

  }
}

</script>