<template>
    <div class="max-w-7xl mx-auto grid grid-cols-1 gap-4">
        <!-- left part -->

        <!-- right part -->
        <div class="main-right py-28 justify-self-center">
            <h1 class="mb-14 font-bold tracking-wide text-6xl">
                Edit<br>Password
            </h1>
            <form class="space-y-6 w-96" v-on:submit.prevent="submitForm">
                <div>
                    <!--old password -->
                    <input type="password" v-model="form.old_password" placeholder="enter your old password" class="bg-transparent w-full py-3 px-6 border border-purple1 rounded-full">
                </div>

                <div>
                    <!--new password -->
                    <input type="password" v-model="form.new_password1" placeholder="enter your new password" class="bg-transparent w-full py-3 px-6 border border-purple1 rounded-full">
                </div>

                <div>
                    <!--confirm new password -->
                    <input type="password" v-model="form.new_password2" placeholder="confirm your new password" class="bg-transparent w-full py-3 px-6 border border-purple1 rounded-full">
                </div>

                <template v-if="errors.length > 0">
                    <div class="bg-red-400 text-white rounded-lg p-6">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}
                        </p>                        
                    </div>
                </template>

                <div class="space-y-2">
                    <button class="active:bg-purple_main tracking-wider bg-[#8250CB] w-full mt-8 py-3 px-6 text-white rounded-full font-semibold">save changes</button>
                    
                </div>
            </form>
        </div>

    </div>

</template>

<script>
import axios from 'axios'

import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()

        return {
            toastStore,
            userStore
        }
    },

    data() {
        return {
            form: {
                old_password: '',
                new_password1: '',
                new_password2: '',
            },
            errors: [],
        }
    },

    methods: {
        submitForm() {
            this.errors = []

            //validation of data

            if (this.form.password1 !== this.form.password2){
                this.errors.push('your password does not match')
            }

            if (this.errors.length === 0) {
                //information to send to the backend
                let formData = new FormData()
                formData.append('old_password', this.form.old_password)
                formData.append('new_password1', this.form.new_password1)
                formData.append('new_password2', this.form.new_password2)

                axios
                    .post('/api/editpassword/', formData, {
                        headers: { // to let the backend know that there other content types or info
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'Profile Information Updated!','bg-emerald-500')
                            
                            this.$router.push(`/profile/${this.userStore.user.id}`) //to go back to profile page after changing password
                        } else {
                            const data = JSON.parse(response.data.message)

                            for(const key in data){
                                this.errors.push(data[key][0].message)
                            }
                        }
                    })
                    .catch(error => {
                        console.log('error', error)
                    })
            }

        }
    }

}
</script>