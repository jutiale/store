<script setup>

defineProps({
    good: Object
})

const emit = defineEmits(['onCountChanged'])


</script>

<template>
    <v-text-field label="Количество" type="number" v-model="good.count" class="mr-4 ml-4"
        @change="changeCount" onkeyup="if(this.value<=0)this.value=1"
        onblur="if(this.value<=0)this.value=1"></v-text-field>
</template>

<script>
import axios from 'axios'
import { useToast } from 'vue-toastification'

const toast = useToast()
// const token = localStorage.getItem('currentUserToken');

export default {
    data() {
        return {
            dialog: false,
            form: '',
            name: 'ChangeCount',
            errors: []

        }
    },
    methods: {
        async changeCount() {
            if (this.good.count <= 0) {
                this.good.count = 1;
            }
            const token = localStorage.getItem('currentUserToken');
            console.log(this.good)
            const response = await axios.patch(
                'http://localhost:8000/myprofile/cart/' + this.good.id_in_cart,
                '',
                {
                    params: {
                        'count': this.good.count
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
                // toast.success("Товар успешно изменен!");
                this.dialog = false;
                this.$emit('onCountChanged')
            }

            else {
                toast.error("Произошла ошибка");
            }
        }
    }
}

</script>