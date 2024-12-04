<script setup>
import { ref } from 'vue'


const emit = defineEmits(['onImageAdded'])

defineProps({
  good: Object
})


</script>

<template>
  <div class="text-center">
    <v-dialog v-model="dialog" width="800" persistent>

      <template v-slot:activator="{ on }">
        <v-btn class="success" variant="tonal" @click="dialog = true">Добавить фотографию</v-btn>
      </template>
      <v-card>
        <v-toolbar>
          <v-spacer />

          <v-toolbar-title>Добавление фотографии</v-toolbar-title>
          <v-spacer />
          <div class="text-left">
            <v-btn icon="mdi-close" @click="dialog = false" class="mr-4"></v-btn>
            <v-spacer />
          </div>
        </v-toolbar>
        <v-form  class="text-center" @submit.prevent="addImage" v-model="form" enctype="multipart/form-data">
          <div class="container">
            <div>
              <label>File
                <input type="file" id="file" ref="file" @change="onSelect"/>
              </label>
              <v-container><v-btn class="success" type="submit" :disabled="isDisable"
                  block>Сохранить</v-btn></v-container>
            </div>
          </div>



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
      name: 'addImage',
      file: undefined,
    }
  },
  computed: {
    isDisable() {
      return this.file === undefined;
  }
  },
  methods: {
    onSelect() {
      const file = this.$refs.file.files[0];
      this.file = file;
    },
    addImage() {
      const token = localStorage.getItem('currentUserToken');
      let formData = new FormData();
      if (!(this.file['type'] ==='image/jpeg')) {
        toast.error("Неверный тип файла");
        return;
      }
      formData.append("file", this.file);
      formData.append("good_id", this.good.id);
      console.log(token);
      axios.post('http://localhost:8000/goods/' + this.good.id + '/images', formData, {
        headers: {
          "Authorization": `Bearer ${token}`,
          "Content-Type": "multipart/form-data",
        },
      }).then(response => this.checkStatus(response))
        .catch(error => this.checkStatus(error));
    },
    checkStatus(response) {
      console.log(response)
      if (response.status == 200) {
        toast.success("Фотография успешно добавлена!");
        this.dialog = false;
        this.$emit('onImageAdded')
      }

      else {
        toast.error("Произошла ошибка");
      }
    }
  }
}

</script>