<script setup>
const emit = defineEmits(['onBrandAdded'])
</script>

<template>
    <div class="text-center">
      <v-dialog v-model="dialog" width="800" persistent>

        <template v-slot:activator="{ on }">
          <v-btn class="success" @click="dialog = true">Добавить бренд</v-btn>
        </template>
        <v-card>
            <v-toolbar>
                <v-spacer />

          <v-toolbar-title>Добавление бренда</v-toolbar-title>
          <v-spacer />
                     <div class="text-left">
          <v-btn
            icon="mdi-close"
            @click="dialog = false"
            class="mr-4"
          ></v-btn>
          <v-spacer />
        </div>     
            </v-toolbar>
            <v-form @submit.prevent="addBrand" v-model="form">
                <v-text-field
                v-model="FormData.name"
                class="mt-4 ml-4 mr-4"
                label="Название*"
                :rules="[v => !!v || 'Укажите название']"
                required
              ></v-text-field>
              
<v-container><v-btn class="success" type="submit":disabled="!form" block>Сохранить</v-btn></v-container>
      
    </v-form>
          <v-card-actions>
        <v-spacer></v-spacer>
      </v-card-actions>
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
            name: 'addBrand',
            FormData: {
                name: '',
            },

        }
    },
    methods: {
        addBrand() {
          const token = localStorage.getItem('currentUserToken');
            console.log(this.FormData)
            axios.post('http://localhost:8000/brands/', this.FormData, {
        headers: {"Authorization": `Bearer ${token}`}
    })
            .then(response => this.checkStatus(response))
            .catch(error => this.checkStatus(error))
        },
        checkStatus(response) {
            console.log(response)
            if (response.status == 200) {
                toast.success("Бренд успешно добавлен!");
                this.dialog = false;
                this.FormData.name = '';
                this.$emit('onBrandAdded')
            }

            else {
                toast.error("Произошла ошибка");
            }
        }
    }
}

</script>