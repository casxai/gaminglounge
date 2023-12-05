<template>
   
    <div class=" max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <!-- left part -->
        <div class="main-left self-center ">    
                <h1 class="mb-6 tracking-wide leading-tight font-black text-6xl">
                    DISCOVER YOUR<h1 class="text-[#8250CB]">GAMING</h1>QUEST. 
                </h1>
                <p class="mb-6 text-lg font-light w-4/5">
                    Look no further - Gaming Lounge is the ultimate one-stop<br> hub for gaming fans. Connect and quest alongside casual and competitive gamers.
                </p>
                <p class="font-medium text-xl">
                not a user yet? <RouterLink to="/Signup" class="font-semibold active:text-blue_link underline">click here</RouterLink> to register!
                </p>
        </div>
        <!-- right part -->
        <div class="main-right py-32 justify-self-end ">
                <!-- <div class="mb-16">
					<img src="/assets/img/logo/gl_logo.png" alt="logo"/>
				</div> -->
            <h1 class="mb-14 font-bold tracking-wide text-6xl">
                Welcome<br>Back!
            </h1>
            <form class="space-y-6 w-96" v-on:submit.prevent="submitForm">
                <div>
                    <!-- email -->
                    <input type="text" v-model="form.email" placeholder="enter your email" class="bg-transparent w-full py-3 px-6 border border-purple1 rounded-full">
                </div>

                <div>
                    <!-- password -->
                    <input type="password" v-model="form.password" placeholder="enter your password" class="bg-transparent w-full py-3 px-6 border border-purple1 rounded-full">
                </div>

                <template v-if="errors.length > 0">
                        <div class="bg-red-400 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>                        </div>
                    </template>

                <div class="space-y-2">
                    <button class="active:bg-purple_main tracking-wider bg-[#8250CB] w-full mt-8 py-3 px-6 text-white rounded-full font-semibold">login</button>

                    <p class="text-center text-[0.86rem] font-light">by clicking register, you agree to the gaming lounges' 
                        <a class="text-blue_link underline active:text-[#0085FF]" href="#">terms of service</a> and 
                        <a class="text-blue_link underline active:text-[#0085FF]" href="#">privacy policy</a>
                    </p>
                </div>
            </form>
        </div>
       <!-- <div class="h-28">

       </div> -->
    </div>

   
</template>
<script>
import axios from 'axios'

import { useUserStore } from '@/stores/user'

export default {
    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    data() {
        return {
            form: {
                email: '', //could be username
                password: '',
            },
            errors: []
        }
    },

    methods: {
            async submitForm() {
                this.errors = [];

                if (this.form.email === '') {
                this.errors.push('your e-mail is missing');
                }

                if (this.form.password === '') {
                this.errors.push('your password is missing');
                }

                if (this.errors.length === 0) {
                try {
                    const response = await axios.post('/api/login/', this.form);
                    this.userStore.setToken(response.data);

                    if (response.data.new_user) {
                    // New user logic (e.g., redirect to a topic selection page)
                    this.$router.push('/popup');
                    } else {
                    axios.defaults.headers.common['Authorization'] =
                        'Bearer ' + response.data.access;
                    }
                } catch (error) {
                    console.log('error', error);
                    this.errors.push(
                    'The email or password is incorrect! Or the user is not activated!'
                    );
                }
                }

                if (this.errors.length === 0) {
                try {
                    const response = await axios.get('/api/me/');
                    this.userStore.setUserInfo(response.data);

                    // Check if pref_game_category is empty in the login response
                    if (!response.data.pref_game_category) {
                        // Redirect to /popup if pref_game_category is empty
                        this.$router.push('/popup');
                    } else {
                        // Redirect to /feed if pref_game_category is not empty
                        this.$router.push('/feed');
                    }
                } catch (error) {
                    console.log('error', error);
                }
                }
            },
        }
    }
</script>
