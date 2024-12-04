<script setup>
const emit = defineEmits(['onUserAdded'])
</script>

<template>
    <div class="text-center">
        <v-dialog v-model="dialog" width="800" persistent>

            <template v-slot:activator="{ on }">
                <v-btn class="success" @click="dialog = true">Добавить пользователя</v-btn>
            </template>
            <v-card>
                <v-toolbar>
                    <v-spacer />

                    <v-toolbar-title>Добавление пользователя</v-toolbar-title>
                    <v-spacer />
                    <div class="text-left">
                        <v-btn icon="mdi-close" @click="dialog = false" class="mr-4"></v-btn>
                        <v-spacer />
                    </div>
                </v-toolbar>
                <v-form @submit.prevent="addUser" v-model="form">
                    <v-text-field v-model="FormData.name" class="mt-4 ml-4 mr-4" label="Имя*"
                        :rules="[v => !!v || 'Укажите имя']" required></v-text-field>
                    <v-text-field v-model="FormData.email" class="mt-4 ml-4 mr-4" label="Эл. почта*"
                        :rules="[v => !!v || 'Укажите почту']" required></v-text-field>
                    <v-text-field v-model="FormData.password" class="mt-4 ml-4 mr-4" label="Пароль*" type="password"
                        :rules="[v => !!v || 'Укажите пароль']" required></v-text-field>
                    <v-select v-model="FormData.role" class="ml-4 mr-4" :rules="[v => !!v || 'Укажите роль']"
                        label="Роль*" placeholder="Не выбрано" :items="roles" item-title="roleName" item-value="roleId"
                        dense outlined required></v-select>

                    <v-container><v-btn class="success" type="submit" :disabled="!form"
                            block>Сохранить</v-btn></v-container>

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
            name: 'addUser',
            FormData: {
                name: '',
                email: '',
                role: '',
                password: '',
            },
            roles: [
                {
                    roleId: 1,
                    roleName: "Обычный пользователь"
                },
                {
                    roleId: 2,
                    roleName: "Менеджер"
                },
                {
                    roleId: 3,
                    roleName: "Администратор"
                }
            ]
        }
    },
    methods: {
        addUser() {

            const token = localStorage.getItem('currentUserToken');

            console.log(this.FormData)
            axios.post('http://localhost:8000/users/', this.FormData, {
                headers: { "Authorization": `Bearer ${token}` }
            })
                .then(response => this.checkStatus(response))
                .catch(error => this.checkStatus(error))
        },
        checkStatus(response) {
            console.log(response)
            if (response.status == 200) {
                toast.success("Пользователь успешно добавлен!");
                this.dialog = false;
                this.FormData.name = '';
                this.FormData.email = '';
                this.FormData.role = '';
                this.FormData.password = '';
                this.$emit('onUserAdded')
            }

            else {
                toast.error("Произошла ошибка");
            }
        }
    }
}

</script>