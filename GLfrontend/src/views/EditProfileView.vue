<template>
    <div class="max-w-7xl  mx-auto grid pt-16">

        <div class="main-center justify-self-center">
            <h1 class="mb-14 font-bold tracking-wide text-6xl">
                Edit<br>Profile
            </h1>
            <form class="space-y-6 w-96 " v-on:submit.prevent="submitForm">
                <!-- username -->
                <div>    
                    <input type="text" v-model="form.name" placeholder="enter your username" class="bg-transparent w-full py-3 px-6 border border-purple1 rounded-img">
                </div>
                <!-- email -->
                <div>
                    <input type="email" v-model="form.email" placeholder="enter your email" class="bg-transparent w-full py-3 px-6 border font-white border-violet1 rounded-img">
                </div>
                <!-- bio -->
                <div>
                    
                    <input type="text" v-model="form.bio" placeholder="enter something about yourself" class="bg-transparent w-full py-3 px-6 border font-white border-violet1 rounded-img">
                </div>
                <!-- avatar -->
                <div class="flex flex-col space-y-4">  
                    <div class="flex-col flex">
                        <label class=" active:bg-[8250CB] hover:bg-violet1 inline-block text-center w-42 py-3 px-6 bg-purple_main text-white rounded-img ">
                            <input type="file" ref="file" @change="onFileChange">
                        change avatar
                        
                         </label>
                        
                            <div class="grid text-center text-sm space-y-2 italic p-2">
                                <div v-if="fileName">
                                {{ fileName }}
                                </div>
                                <img v-if="url" :src="url" class="md:object-contain justify-self-center object-contain rounded-img w-14 h-14 ">
                            </div>

                    </div>   

                    <div>
                    <RouterLink to ="/profile/edit/password" class="underline">
                        change password
                    </RouterLink> <br>
                    <RouterLink to ="/popup" class="underline">
                    change category & game titles
                    </RouterLink>
    

                    </div>
                </div>




                <template v-if="errors.length > 0">
                    <div class="bg-red-400 text-white rounded-lg p-6">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}
                        </p>                        
                    </div>
                </template>

                <div class="space-y-2">
                    <button class="hover:bg-violet1 tracking-wider bg-[#8250CB] w-full mt-8 py-3 px-6 text-white rounded-img font-semibold">save changes</button>
                    
                </div>
            </form>
        </div>
        <br>
        <br>
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
            userStore,
            fileName: null,
             url: null,
        }
    },

    data() {
        return {
            form: {
                name: this.userStore.user.name,
                email: this.userStore.user.email, 
                bio: this.userStore.user.bio,         
            },
            errors: [],
        }
    },

    methods: {
                onFileChange(e) {
            const file = e.target.files[0];
            
            this.fileName = file.name;

            const reader = new FileReader();
            reader.onload = e => {
                this.url = e.target.result;  
            };
            
            reader.readAsDataURL(file); 
        
            },
            removeFile() {
            this.fileName = null;
            this.url = null; 
            },
        submitForm() {
            this.errors = []

            //validation of data


            if (this.form.name === ''){
                this.errors.push('your name is missing')
            }

            if (this.form.email === ''){
                this.errors.push('your email is missing')
            }
            if (this.errors.length === 0) {
                let formData = new FormData() //avatar
                formData.append('avatar', this.$refs.file.files[0])
                formData.append('name', this.form.name)
                formData.append('email', this.form.email)
                formData.append('bio', this.form.bio)

                axios
                    .post('/api/editprofile/', formData, {
                        headers: { // to let the backend know that there other content types or info
                            "Content-Type": "multipart/form-data",
                        }
                    })
                    .then(response => {
                        if (response.data.message === 'information updated') {
                            this.toastStore.showToast(5000, 'Profile Information Updated!','bg-emerald-500')
                            
                            //update the user store in the browser 
                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                email: this.form.email,
                                bio: this.form.bio,
                                avatar: response.data.user.get_avatar
                            })
                            
                            //to go back to profile page after edit profile info
                            this.$router.back()
                        } else {
                            this.toastStore.showToast(5000, `${response.data.message}. Please try again`, 'bg-red-300')
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