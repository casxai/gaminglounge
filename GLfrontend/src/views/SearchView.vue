<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <!--Search bar-->
        <div class="main-left col-span-3">
            
                <form v-on:submit.prevent="submitForm" class="p-4 flex ">  
                    <input v-model="query" type="search" class="p-4 w-full text-black rounded-bl-large rounded-tl-large" placeholder="who are you looking for?">
                    <button class="inline-block py-4 px-6 hover:bg-purple1 bg-purple_main text-white rounded-br-large rounded-tr-large">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
						</svg>
                    </button>
                </form>
          

            <div 
                class="p-4 grid grid-cols-4 gap-4"
                v-if="users.length"
            >
                <div 
                    class="p-6 bg-purple_main text-center rounded-full"
                    v-for="user in users"
                    v-bind:key="user.id"
                >
                    <img :src="user.get_avatar" class=" mb-4 rounded-img h-30 w-30 m:h-30 sm:w-30 object-cover">
                           
                    @<RouterLink class="font-medium text-lg" :to="{name: 'profile', params:{'id': user.id}}">{{ user.name }}</RouterLink>                      
                 
                    <div class="mt-2 mb-2 flex space-x-8 justify-around">
                        <p class="text-sm text-gray-400">{{ user.friends_count }} friends</p>
                        <p class="text-sm text-gray-400">{{ user.posts_count }} posts</p>
                    </div>
                </div>
            </div>

            <!-- post area -->
            <div class="p-4 m-4 bg-purple_main rounded-full"
                    v-for="post in posts" 
                    v-bind:key="post.id"> <!-- loop ng post -->
                
                <FeedItem v-bind:post="post" />
            </div>
        </div>

        <div class="main-right col-span-1 space-y-4">
           <PeopleYouMayKnow />
         
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue' 
import FeedItem from '../components/FeedItem.vue'


export default {
    name: 'SearchView',
    components: {
        PeopleYouMayKnow,
     
        FeedItem,
    },

    data() {
        return {
            query: '',
            searchQuery: '',
            users: [],
            posts: []
        }
    },

    methods: 
    {
        submitForm() 
        {
            console.log('submitForm', this.query)

            axios
                .post('/api/search/', 
                {
                    query: this.query
                })
                .then(response => 
                {
                    console.log('response:', response.data)

                    this.users = response.data.users
                    this.posts = response.data.posts
                })
                .catch(error =>
                {
                    console.log('error:', error)
                })
        }
    }


}
</script>