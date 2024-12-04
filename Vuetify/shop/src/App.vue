<template>
  <div class="Goods">
    <v-app>
      <router-view></router-view>
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
import { store } from './store'
import { watchEffect } from 'vue'

let snackbar = ref(false);
let snackbarText = ref('');

const toast = useToast()

export default {
  components: { Navbar, AddGoodPopup, UpdateGoodPopup, DeleteGoodPopup },
  name: 'App',
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
      pagination.perPage = res.data.onPage



      for (const good of goods.value) {
        const res = await fetch(`http://localhost:8000/goods/` + good.id + `/images`)
        good.images = await res.json()
        console.log(good.images);
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
      console.log(id, confirm);
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

  }
}

</script>
