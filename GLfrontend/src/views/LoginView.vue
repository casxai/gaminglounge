<template>
   
    <div class="md:grid gap-4">
        <!-- left part -->
        <!-- <div class="main-left self-center ">    
                <h1 class="mb-6 tracking-wide leading-tight font-black text-6xl">
                    DISCOVER YOUR<h1 class="text-[#8250CB]">GAMING</h1>QUEST. 
                </h1>
                <p class="mb-6 text-lg font-light w-4/5">
                    Look no further - Gaming Lounge is the ultimate one-stop<br> hub for gaming fans. Connect and quest alongside casual and competitive gamers.
                </p>
                <p class="font-medium text-xl">
                not a user yet? <RouterLink to="/Signup" class="font-semibold active:text-blue_link underline">click here</RouterLink> to register!
                </p>
        </div> -->
        <!-- right part -->
        <div class="main-center justify-self-center py-32">
                <!-- <div class="mb-16">
					<img src="/assets/img/logo/gl_logo.png" alt="logo"/>
				</div> -->
            <h1 class="md:mb-14 font-bold tracking-wide welcome md:text-6xl">
                Welcome<br>Back!
            </h1>
            <form class="md:space-y-6 md:w-96" v-on:submit.prevent="submitForm">
                <div>
                    <!-- email -->
                    <input type="text" v-model="form.email" placeholder="enter your email" class="forms-email bg-transparent w-full md:py-3 md:px-6 border border-purple1 rounded-full">
                </div>

                <div>
                    <!-- password -->
                    <input type="password" v-model="form.password" placeholder="enter your password" class="forms-email bg-transparent w-full md:py-3 md:px-6 border border-purple1 rounded-full">
                </div>

                <template v-if="errors.length > 0">
                        <div class="bg-red-400 text-white rounded-lg p-6">
                            <p v-for="error in errors" v-bind:key="error">{{ error }}</p>                        </div>
                    </template>

                <div class="space-y-2">
                    <button class="login-button active:bg-purple_main tracking-wider bg-[#8250CB] w-full md:mt-8 md:py-3 px-6 text-white rounded-full font-semibold">login</button>

                    <p class="text-center md:text-[0.86rem] font-light forms-email">not a user yet? 
                        <RouterLink to="/Signup" class="text-blue_link underline active:text-[#0085FF]" href="#">click here</RouterLink> to register!
                        
                    </p>
                </div>
            </form>
        </div>
       <!-- <div class="h-28">

       </div> -->
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
