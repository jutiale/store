<script setup>
const emit = defineEmits(['onCartCleared'])

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
            Очистить корзину
          </v-btn>
        </template>
  

        <v-card
        title="Очистка корзины"
        :text="`Вы действительно хотите очистить корзину?`"
      >
          <template v-slot:actions>
            <v-spacer></v-spacer>
  
            <v-btn @click="cancel">
              Нет
            </v-btn>
  
            <v-btn @click="clearCart">
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
      clearCart() {
        const token = localStorage.getItem('currentUserToken');
        console.log(token);

        axios.delete('http://localhost:8000/myprofile/cart/', {
        headers: {"Authorization": `Bearer ${token}`}
    })
                .then(response => this.checkStatus(response))
                .catch(error => this.checkStatus(error))
    },      
      
    checkStatus(response) {
            console.log(response)
            if (response.status == 200) {
                toast.success("Корзина успешно очищена!");
                this.dialog = false;
                this.$emit('onCartCleared')
            }
            else {
                toast.error("Произошла ошибка");
            }
        },
    }
}

</script>