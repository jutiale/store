<script setup>
const emit = defineEmits(['onGoodsBought'])
defineProps({
    price: Number
})
</script>

<template>
    <div class="text-center pa-4">
      <v-dialog
        v-model="dialog"
        max-width="400"
        persistent
      >
        <template v-slot:activator="{ props: activatorProps }">
          <v-btn v-bind="activatorProps" @click="dialog = true" variant="tonal">
            Оформить заказ
          </v-btn>
        </template>
  

        <v-card
        title="Оформление заказа"
        :text="`Вы действительно хотите оформить заказ?`"
      >
      <v-card-text>Общая стоимость заказа: {{ price }} руб.</v-card-text>
          <template v-slot:actions>
            <v-spacer></v-spacer>
  
            <v-btn @click="cancel">
              Нет
            </v-btn>
  
            <v-btn @click="buyGoods">
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
      async buyGoods() {
        const token = localStorage.getItem('currentUserToken');
        console.log(token);
        const response = await axios.post(
          'http://localhost:8000/myprofile/cart/buy',
        '',
        {
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
                toast.success("Заказ успешно оформлен!");
                this.dialog = false;
                this.$emit('onGoodsBought')
            }
            else {
                toast.error("Произошла ошибка");
            }
        },
    }
}

</script>