<template>
        <div class="grid gap-4">
            <!-- left part -->
            <!-- <div class="main-left self-center ">    
                    <h1 class="mb-6 tracking-wide leading-tight font-black text-6xl">
                        DISCOVER YOUR<br>GAMING QUEST.
                    </h1>
                    <p class="mb-6 text-lg font-light w-4/5">
                        Look no further - Gaming Lounge is the ultimate one-stop<br> hub for gaming fans. Connect and quest alongside casual and competitive gamers.
                    </p>
                    <p class="font-medium text-xl">
                    already have an account? <RouterLink to="/" class="font-semibold active:text-blue_link underline">click here </RouterLink> to login!
                    </p>
            </div> -->
            <!-- right part -->
            <div class="main-center justify-self-center py-32">
                <h1 class="md:mb-14 font-bold tracking-wide welcome md:text-6xl">
                    Welcome<br>Gamer!
                </h1>
                <form class="md:space-y-6 md:w-96" v-on:submit.prevent="submitForm">
                    <div>
                        <!-- username -->
                        <input type="text" v-model="form.name" placeholder="enter your username" class="forms-email bg-transparent w-full md:py-3 md:px-6 border border-purple1 rounded-full">
                    </div>
                    <div>
                        <!-- email -->
                        <input type="email" v-model="form.email" placeholder="enter your email" class="forms-email bg-transparent w-full md:py-3 md:px-6 border border-purple1 rounded-full">
                    </div>
                    <div>
                        <!-- password -->
                        <input type="password" v-model="form.password1" placeholder="enter your password" class="forms-email bg-transparent w-full md:py-3 md:px-6 border border-purple1 rounded-full">
                    </div>
                    <div>
                        <!-- confirm password -->
                        <input type="password" v-model="form.password2" placeholder="confirm password" class="forms-email bg-transparent w-full md:py-3 md:px-6 border border-purple1 rounded-full">
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-400 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}
                            </p>                        
                        </div>
                    </template>
                    
                    <div class="space-y-2">
                        
                        <button class="login-button active:bg-purple_main tracking-wider bg-[#8250CB] w-full md:py-3 px-6 text-white rounded-full font-semibold">register</button>

                        <Modal @close="toggleTerms" :modalActive="modalActive">
                        <!-- <div class="rounded-full bg-transparent space-y-1 text-right model-content"> -->
                            <Terms />
                        <!-- </div> -->
               
                        <!-- <div class="rounded-full bg-transparent space-y-1 text-right model-content"> -->
                            <DataPrivacy />
                        <!-- </div> -->

                        
                        </Modal>   
                        
                        <p class="forms-email text-center md:text-[0.84rem] font-light">by clicking register, you agree to the gaming lounges' 
                            <button @click="toggleTerms" type="button" class="text-blue_link hover:underline active:text-[#0085FF]" >terms of service || data privacy</button> 
                        </p>

                        <p class="forms-email text-center md:text-[0.86rem] font-medium p-2">already have an acconut? 
                            <RouterLink to="/" class="text-blue_link underline active:text-[#0085FF]" href="#">login</RouterLink>
                        </p>

                       
                    </div>
                </form>
            </div>

        </div>

</template>
<style scoped>
@media (max-width: 768px) {
  .hide-on-mobile {
    display: none; /* Hide the logo on smaller screens */
  }
  .welcome{
    font-size: 28px;
    margin-bottom: 1rem;
    padding-left: 4px;

  }
  .login-button{
    padding: 6px 10px 6px 10px;
    font-size: 14px;
  }
  .forms-email {
    margin-bottom: 0.5rem;
    font-size: 14px;
    padding: 6px 10px 6px 10px;
  }
}
</style>
<script>
import axios from 'axios'

import { useToastStore } from '@/stores/toast'
import Modal from '@/components/Modal.vue';
import Terms from '@/components/Terms.vue';
import DataPrivacy from '@/components/DataPrivacy.vue';

import {ref} from 'vue'


export default {
    components: {
 
    Modal,
   
    Terms,
    DataPrivacy,
    },
    setup() {
        const toastStore = useToastStore()
        const modalActive = ref(false)
        const toggleTerms = () => {
            modalActive.value = !modalActive.value;
        }
 

        return {
            toastStore,
            modalActive,
            toggleTerms,
          
            
            
        }
    },

    data() {
        return {
            form: {
                name: '',
                email: '',            
                password1: '',
                password2: '',
            },
            errors: [],
        }
    },

    methods: {
        submitForm() {
            this.errors = []

            //validation of data

            if (this.form.email === ''){
                this.errors.push('Your email is missing')
            }

            if (this.form.name === ''){
                this.errors.push('Your name is missing')
            }

            if (this.form.password1 === ''){
                this.errors.push('Your password is missing')
            }

            if (this.form.password1 !== this.form.password2){
                this.errors.push('Your password does not match')
            }

            if (this.errors.length === 0) {
                axios
                    .post('/api/signup/', this.form)
                    .then(response => {
                        if (response.data.message === 'success') {
                            this.toastStore.showToast(5000, 'The user is registered. Please activate your account by clicking your email link','bg-emerald-700')
                            this.form.name = ''
                            this.form.email = ''
                            this.form.password1 = ''
                            this.form.password2 = ''
                        } else {
                            // signup error
                            const data = JSON.parse(response.data.message)
                            for(const key in data){
                                this.errors.push(data[key][0].message)
                            }
                            
                            this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red-300')
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