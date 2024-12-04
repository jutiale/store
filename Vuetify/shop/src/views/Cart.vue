<template>
    <div class="Cart">
        <v-app>
            <Navbar />

            <v-container v-if="currentUser">
                <p class="text-h4 text-center">Общая стоимость: {{ total_price }} руб.</p>
                <v-divider class="mx-4 mb-1 mt-2" v-if="currentUser"></v-divider>
                <v-row class="d-flex justify-center mb-6">
                    <BuyGoodsPopup @onGoodsBought="fetchData" :price="total_price" />
                    <ClearCart @onCartCleared="fetchData" />
                </v-row>

                <v-row>
                    <v-col cols="4" v-for="good in goods" :key="good.id">
                        <v-card variant="outlined">
                            <router-link :to="'/goods/' + good.id" style="text-decoration: none; color: inherit;" link>
                                <v-card-title class="text-center text-h5">{{ good.name }}</v-card-title>
                                <div class="text-center" v-for="(image, i) in good.images" :key="i">
                                    <v-avatar size="350" rounded="0" v-if="i == 0">
                                        <v-img :src="'http://localhost:8000/' + image.path"></v-img>
                                    </v-avatar>
                                </div>
                                <div class="d-flex justify-center mb-4 mt-2">
                                    <v-chip class="mr-2">{{ good.category.name }}</v-chip>
                                    <v-chip class="ml-2">{{ good.brand.name }}</v-chip>
                                </div>
                            </router-link>
                            <v-card-text align="center" class="text-h6">{{ good.price }} руб.</v-card-text>
                            <ChangeCountGood @onCountChanged="fetchData" :good="good"/>
                            <!-- <v-text-field label="Количество" type="number" v-model="good.count" class="mr-4 ml-4"
                                @change="changeCount(good.id_in_cart, good.count)"
                                onkeyup="if(this.value<=0)this.value=1"
                                onblur="if(this.value<=0)this.value=1"></v-text-field> -->
                            <v-divider class="mx-4 mb-1" v-if="currentUser"></v-divider>
                            <v-spacer></v-spacer>
                            <v-card-actions class="justify-center" v-if="currentUser">
                                <div>
                                    <DeleteGoodFromCartPopup @onGoodFromCartDeleted="fetchData" :good="good" />
                                </div>
                            </v-card-actions>
                        </v-card>
                    </v-col>
                </v-row>
            </v-container>
        </v-app>
    </div>
</template>



<script>
import { ref } from 'vue'
import Navbar from '@/components/Navbar'
import AddGoodPopup from '@/components/AddGoodPopup'
import UpdateGoodPopup from '@/components/UpdateGoodPopup'
import DeleteGoodFromCartPopup from '@/components/DeleteGoodFromCartPopup'
import BuyGoodsPopup from '@/components/BuyGoodsPopup'
import ClearCart from '@/components/ClearCart'
import ChangeCountGood from '@/components/ChangeCountGood'

import axios from 'axios'
import { useToast } from 'vue-toastification'

const toast = useToast()

export default {
    components: { Navbar, AddGoodPopup, UpdateGoodPopup, DeleteGoodFromCartPopup, BuyGoodsPopup, ClearCart, ChangeCountGood },
    name: 'Goods',
    setup() {
        let goods = ref(null);
        const total_price = ref(0);

        async function fetchData() {
            const token = localStorage.getItem('currentUserToken');

            const res = await axios.get(
                `http://localhost:8000/myprofile/cart/`, { headers: { "Authorization": `Bearer ${token}` } }
            )
            goods.value = res.data.goods
            total_price.value = res.data.total_price



            for (const good of goods.value) {
                const res = await fetch(`http://localhost:8000/goods/` + good.id + `/images`)
                good.images = await res.json()
            }
        }

        fetchData()

        return {
            goods,
            total_price,
            fetchData
        }
    },
    data() {
        return {
            items: [],
        }
    },
    computed: {
        currentUser() {
            return this.$store.state.user;
        },
        pageCount() {
            let l = this.pagination.total;
            return Math.ceil(l / 6);
        },
    },
    methods: {
        deleteGood(id, confirm) {
            if (confirm == true) {
                axios.delete('http://localhost:8000/goods/' + id)
                    .then(response => this.checkStatus(response))
                    .catch(error => console.log(error))
            }

        },
        async changeCount(id, count) {
            if (count <= 0) {
                count = 1;
            }
            const token = localStorage.getItem('currentUserToken');
            console.log(this.goods)
            const response = await axios.patch(
                'http://localhost:8000/myprofile/cart/' + id,
                '',
                {
                    params: {
                        'count': count
                    },
                    headers: {
                        'accept': 'application/json',
                        'Authorization': `Bearer ${token}`
                    }
                }
            )
                .then(response => this.checkStatus(response))
                .catch(error => console.log(error))

        },
        checkStatus(response) {
            console.log(response)
            if (response.status == 200) {
                this.fetchData;
            }
            else {
                toast.error("Произошла ошибка");
            }
        },
        // nextPage() {
        //   this.fetchData();
        // },
        // prevPage() {
        //   this.fetchData();
        // },

    }
}

</script>