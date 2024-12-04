<script setup>
const emit = defineEmits(['onGoodDeleted'])


defineProps({
    good: Object
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
            Удалить
          </v-btn>
        </template>
  

        <v-card
        title="Удаление"
        :text="`Вы действительно хотите удалить товар ${good.name}?`"
      >
          <template v-slot:actions>
            <v-spacer></v-spacer>
  
            <v-btn @click="cancel">
              Нет
            </v-btn>
  
            <v-btn @click="deleteGood">
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
      deleteGood() {
        const token = localStorage.getItem('currentUserToken');
        console.log(token);

        axios.delete('http://localhost:8000/goods/' + this.good.id, {
        headers: {"Authorization": `Bearer ${token}`}
    })
                .then(response => this.checkStatus(response))
                .catch(error => this.checkStatus(error))
    },      
      
    checkStatus(response) {
            console.log(response)
            if (response.status == 200) {
                toast.success("Товар успешно удален!");
                this.dialog = false;
                this.$emit('onGoodDeleted')
            }
            else {
                toast.error("Произошла ошибка");
            }
        },
    }
}

</script>