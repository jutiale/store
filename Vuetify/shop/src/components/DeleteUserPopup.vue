<script setup>
const emit = defineEmits(['onUserDeleted'])


defineProps({
    user: Object
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
        :text="`Вы действительно хотите удалить пользователя ${user.name}?`"
      >
          <template v-slot:actions>
            <v-spacer></v-spacer>
  
            <v-btn @click="cancel">
              Нет
            </v-btn>
  
            <v-btn @click="deleteUser">
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
      deleteUser() {
        const token = localStorage.getItem('currentUserToken');
        axios.delete('http://localhost:8000/users/' + this.user.id, {
        headers: {"Authorization": `Bearer ${token}`}
    })
                .then(response => this.checkStatus(response))
                .catch(error => this.checkStatus(error))
    },      
      
    checkStatus(response) {
            console.log(response)
            if (response.status == 200) {
                toast.success("Пользователь успешно удален!");
                this.dialog = false;
                this.$emit('onUserDeleted')
            }
            else {
                toast.error("Произошла ошибка");
            }
        },
    }
}

</script>