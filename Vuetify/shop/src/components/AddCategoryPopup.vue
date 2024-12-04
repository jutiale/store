<script setup>
import { ref } from 'vue'

const categories = ref(null)
const brands = ref(null)

const emit = defineEmits(['onCategoryAdded'])


</script>

<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="800" persistent>

      <template v-slot:activator="{ on }">
        <v-btn class="success" @click="dialog = true">Добавить категорию</v-btn>
      </template>
      <v-card>
        <v-toolbar>
          <v-spacer />

          <v-toolbar-title>Добавление категории</v-toolbar-title>
          <v-spacer />
          <div class="text-left">
            <v-btn icon="mdi-close" @click="dialog = false" class="mr-4"></v-btn>
            <v-spacer />
          </div>
        </v-toolbar>
        <v-form @submit.prevent="addCategory" v-model="form">
          <v-text-field v-model="FormData.name" class="mt-4 ml-4 mr-4" label="Название*"
            :rules="[v => !!v || 'Укажите название']" required></v-text-field>

          <v-container><v-btn class="success" type="submit" :disabled="!form" block>Сохранить</v-btn></v-container>

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
      name: 'addCategory',
      FormData: {
        name: '',
      },

    }
  },
  methods: {
    addCategory() {
      const token = localStorage.getItem('currentUserToken');
      console.log(this.FormData)
      axios.post('http://localhost:8000/categories/', this.FormData, {
        headers: { "Authorization": `Bearer ${token}` }
      })
        .then(response => this.checkStatus(response))
        .catch(error => this.checkStatus(error))
    },
    checkStatus(response) {
      console.log(response)
      if (response.status == 200) {
        toast.success("Категория успешно добавлена!");
        this.dialog = false;
        this.$emit('onCategoryAdded')
      }

      else {
        toast.error("Произошла ошибка");
      }
    }
  }
}

</script>