<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
const route = useRoute()

const good = ref(null)
const images = ref(null)

async function fetchData() {
    images.value = null;

    const responseGood = await axios.get('http://localhost:8000/goods/' + route.params.id);
    good.value = await responseGood.data;
    const responseImages = await axios.get('http://localhost:8000/goods/' + route.params.id + '/images');
    images.value = await responseImages.data;
}

fetchData();
</script>

<template>
    <div class="GoodRead" v-if="good">
        <Navbar />

        <v-container class="d-flex flex-row align-center justify-space-around">
            <v-card variant="flat" class="carousel-container">
                <v-carousel v-if="images" show-arrows="hover">
                    <v-carousel-item v-for="(image) in images" :key="image.path"
                        :src="'http://localhost:8000/' + image.path">
                        <!-- <img  height="auto"> -->
                        <div v-if="currentUser">
                            <DeleteImagePopup v-if="currentUser.userRole == 2 || currentUser.userRole == 3"
                                @onImageDeleted="fetchData" :image="image" :good="good" />
                        </div>
                    </v-carousel-item>
                </v-carousel>

            </v-card>

            <v-card variant="flat" class="text-card">
                <v-card-item>
                    <v-card-title>
                        {{ good.name }}
                    </v-card-title>
                </v-card-item>

                <v-card-text>
                    {{ good.description }}
                </v-card-text>
                <v-card-text>
                    Цена: {{ good.price }} руб.
                </v-card-text>
                <v-spacer></v-spacer>

                <v-card-item class="text-center">
                    <v-chip>{{ good.category.name }}</v-chip>
                </v-card-item>
                <v-card-item class="text-center">
                    <v-chip>{{ good.brand.name }}</v-chip>
                </v-card-item>

                <v-row>
                    <v-col cols="7">
                        <v-list-subheader>Выберите количество товара:</v-list-subheader>
                    </v-col>

                    <v-col cols="5">
                        <v-text-field label="Количество" type="number" v-model="count" 
                            onkeyup="if(this.value<=0)this.value=1"
                            onblur="if(this.value<=0)this.value=1"></v-text-field>
                    </v-col>
                </v-row>

                <v-spacer></v-spacer>
                <v-card-actions class="justify-center" v-if="currentUser">
                    <div v-if="currentUser">
                        <UpdateGoodPopup v-if="currentUser.userRole == 2 || currentUser.userRole == 3"
                            @onGoodUpdated="fetchData" :good="good" />
                        <DeleteGoodPopup v-if="currentUser.userRole == 2 || currentUser.userRole == 3"
                            @onGoodDeleted="fetchData" :good="good" />
                        <AddImagePopup v-if="currentUser.userRole == 2 || currentUser.userRole == 3"
                            @onImageAdded="fetchData" :good="good" />
                        <AddGoodToCartPopup :good="good" :count="count" />
                    </div>
                </v-card-actions>
            </v-card>
        </v-container>

    </div>
</template>


<script>
import Navbar from '@/components/Navbar'
import UpdateGoodPopup from '@/components/UpdateGoodPopup'
import DeleteGoodPopup from '@/components/DeleteGoodPopup'
import AddImagePopup from '@/components/AddImagePopup'
import DeleteImagePopup from '@/components/DeleteImagePopup'


import axios from 'axios'
import { useToast } from 'vue-toastification'
import AddGoodToCartPopup from '@/components/AddGoodToCartPopup.vue'

const toast = useToast()

export default {
    components: { Navbar, UpdateGoodPopup, DeleteGoodPopup, AddImagePopup, DeleteImagePopup, AddGoodToCartPopup },
    name: 'GoodRead',
    data() {
        return {
            count: '1',
        }
    },
    computed: {
        currentUser() {
            return this.$store.state.user;
        },
    },
}

</script>


<style scoped>
.carousel-container {
    width: 60%;
    /* Увеличиваем ширину карусели на 70% */
}

.carousel-container img {
    width: 100%;
}

.text-card {
    width: 40%;
    margin-left: 100px;
    margin-top: 50px;
    /* Для создания пространства между каруселью и карточкой с текстом */
}
</style>