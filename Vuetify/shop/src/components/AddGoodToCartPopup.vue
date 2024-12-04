<script setup>


defineProps({
  good: Object,
  count: String,
})
</script>

<template>
  <div class="text-center pa-4">
    <v-dialog v-model="dialog" max-width="400" persistent>
      <template v-slot:activator="{ props: activatorProps }">
        <v-btn v-bind="activatorProps" @click="dialog = true" variant="tonal">
          Добавить в корзину
        </v-btn>
      </template>


      <v-card title="Добавление в корзину" :text="`Вы действительно хотите добавить в корзину товар ${good.name}?`">
        <template v-slot:actions>
          <v-spacer></v-spacer>

          <v-btn @click="cancel">
            Нет
          </v-btn>

          <v-btn @click="addGoodToCart">
            Да
          </v-btn>
        </template>
      </v-card>

    </v-dialog>
  </div>
</template>

<script>
import axios from 'axios'
import { useToast } from 'vue-toastification'

const toast = useToast()

export default {
  data() {
    return {
      dialog: false,
      form: '',
    }
  },
  methods: {
    cancel() {
      this.dialog = false;

    },
    async addGoodToCart() {
      const token = localStorage.getItem('currentUserToken');
      console.log("Count: " + this.count);
      const response = await axios.post(
        'http://localhost:8000/goods/' + this.good.id + '/add_to_cart',
        '',
        {
          params: {
            'count': this.count
          },
          headers: {
            'accept': 'application/json',
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      )
        .then(response => this.checkStatus(response))
        .catch(error => this.checkStatus(error))
    },

    checkStatus(response) {
      console.log(response)
      if (response.status == 200) {
        toast.success("Товар успешно добавлен в корзину!");
        this.dialog = false;
      }
      else {
        toast.error("Произошла ошибка");
      }
    },
  }
}

</script>