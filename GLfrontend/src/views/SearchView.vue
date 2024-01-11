<template>
    <div class="grid grid-cols-4 gap-4">
        <!--Search bar-->
        <div class="main-left main-center md:col-span-3 col-span-4 space-y-6">
            
                <form v-on:submit.prevent="submitForm" class="md:px-4 flex ">  
                    <input v-model="query" type="search" class="md:p-4 w-full text-black rounded-bl-large rounded-tl-large search" placeholder="who are you looking for?">
                    <button class="inline-block md:py-4 px-6 hover:bg-purple1 bg-purple_main text-white rounded-br-large rounded-tr-large search">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"></path>
						</svg>
                    </button>
                </form>
            <div 
                class="md:p-4 grid md:grid-cols-4 gap-4"
                v-if="users.length"
            >
                <div 
                    class="md:p-6 bg-purple_main text-center rounded-full"
                    v-for="user in users"
                    v-bind:key="user.id"
                    
                >       
                    <div class="usernamesubimg">
                            <div class="md:mb-4 md:mt-4 md:flex imgsearch">
                                <img :src="user.get_avatar" class="avatar aspect-square rounded-img md:h-30 md:w-30 object-cover">
                            </div>
                            <div class="usernamesub">
                                <RouterLink class="font-medium md:text-lg username " :to="{name: 'profile', params:{'id': user.id}}">{{ user.name }}</RouterLink>                      
                        
                                <div class="md:mt-2 md:mb-2 flex md:space-x-8 md:justify-around">
                                    <p class="text-sm text-gray-400 subtexts charisma">{{ user.charisma_score }} charisma</p>
                                    <p class="text-sm text-gray-400 subtexts">{{ user.posts_count }} posts</p>
                                </div>
                            </div>
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

 
        <div class="bg-purple_main border-gray-400 border-2 rounded-full h-fit hide-on-mobile">
            <h3 class="rounded-full font-semibold text-xl tracking-wide pl-6 py-4">People you may know</h3>

            
                <div v-for="user in users" :key="user.id" class="flex items-center justify-between border-gray-200 hover:bg-[#120719] hover:rounded-full">
                    
                    <div class="justify-self-start items-center flex my-3 px-6">
                        <img :src="user.get_avatar" alt="avatar" class="h-12 rounded-img object-cover aspect-square mr-3" width="50" height="50">
                        <div class="flex flex-col">
                            <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }" >
                            <span class="font-medium">{{ user.name }}</span>
                            </RouterLink>
                            <span class=" text-sm text-gray-400">{{ user.charisma_score }} charisma</span>
                        </div>
 
                    </div>

                </div>    
        </div>
    </div>
</template>
<style scoped>
@media (max-width: 768px) {
  .hide-on-mobile {
    display: none; /* Hide the logo on smaller screens */
  }
  .avatar {
    height: 40px;
    width: auto;
    
  }
  .username {
    font-size: 16px;
    justify-self: start;
    display: flex;
  }
  .subtexts {
    font-size: 14px;
  }
  .usernamesub {
    
    display: flex;
    flex-direction: column;
    align-self: center;
    
  }
  .charisma {
    display: none;
  }
  .usernamesubimg {
    display: flex;
    
  
  }
  .imgsearch {
    padding: 1rem;
  }
 .search {
    font-size: 14px;

 }
}
</style>

<script>
import axios from 'axios'
// import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue' 
import FeedItem from '../components/FeedItem.vue'


export default {
    name: 'SearchView',
    components: {

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
    mounted() {
        this.getFriendSuggestions();

    },
    methods: 
    {
        getFriendSuggestions() {
            axios
                .get('/api/friends/suggested/')
                .then(response => {
                    console.log(response.data);
                    this.users = response.data;
                })
                .catch(error => {
                    console.log('error', error);
                });
        },

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