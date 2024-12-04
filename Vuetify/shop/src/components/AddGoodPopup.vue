<script setup>
import { ref } from 'vue'

const categories = ref(null)
const brands = ref(null)

const emit = defineEmits(['onGoodAdded'])

async function fetchDataCategories() {
    const res = await axios.get(
        `http://localhost:8000/categories/?skip=0&limit=100`
    )
    categories.value = await res.data.categories

}

async function fetchDataBrands() {
    const res = await axios.get(
        `http://localhost:8000/brands/?skip=0&limit=100`
    )
    brands.value = await res.data.brands
}

fetchDataCategories();
fetchDataBrands();

</script>

<template>
    <div class="text-center">
      <v-dialog v-model="dialog" width="800" persistent>

        <template v-slot:activator="{ on }">
          <v-btn class="success" @click="dialog = true">Добавить товар</v-btn>
        </template>
        <v-card>
            <v-toolbar>
                <v-spacer />

          <v-toolbar-title>Добавление товара</v-toolbar-title>
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
            <v-form @submit.prevent="addGood" v-model="form">
                <v-text-field
                v-model="FormData.name"
                class="mt-4 ml-4 mr-4"
                label="Название*"
                :rules="[v => !!v || 'Укажите название']"
                required
              ></v-text-field>
              <v-text-field
              v-model="FormData.description"
                class="ml-4 mr-4"
                label="Описание"
              ></v-text-field>

              <v-select
        v-model="FormData.category_id"
        class="ml-4 mr-4"
        :rules="[v => !!v || 'Укажите категорию']"
        label="Категория*" 
          placeholder="Не выбрано" 
          :items="categories" 
          item-title="name"
          item-value="id"
          dense 
          outlined
          required
      >
    </v-select>


      <v-select
        v-model="FormData.brand_id"
        class="ml-4 mr-4"
        :rules="[v => !!v || 'Укажите бренд']"
        label="Бренд*" 
          placeholder="Не выбрано" 
          :items="brands" 
          item-title="name"
          item-value="id"
          dense 
          outlined
          required
      >
      
    </v-select>

              <v-text-field
              v-model="FormData.price"
                class="ml-4 mr-4"
                label="Цена*"
                type="number"
                onkeyup="if(this.value<0)this.value=1"
                onblur="if(this.value<0)this.value=1"                
                :rules="[v => !!v || 'Укажите цену']"
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
            name: 'addGood',
            FormData: {
                name: '',
                description: '',
                category_id: '',
                brand_id: '',
                price: ''
            },
            errors: []

        }
    },
    methods: {
        addGood() {
          const token = localStorage.getItem('currentUserToken');

            console.log(this.FormData)
            axios.post('http://localhost:8000/goods/', this.FormData, {
        headers: {"Authorization": `Bearer ${token}`}
    })
            .then(response => this.checkStatus(response))
            .catch(error => this.checkStatus(error))
            this.FormData.name = ''
            this.FormData.description = ''
            this.FormData.category_id = ''
            this.FormData.brand_id = ''
            this.FormData.price = ''
            
        },
        checkStatus(response) {
            console.log(response)
            if (response.status == 200) {
                toast.success("Товар успешно добавлен!");
                this.dialog = false;
                this.$emit('onGoodAdded')
            }

            else {
                toast.error("Произошла ошибка");
            }
        }
    }
}

</script>