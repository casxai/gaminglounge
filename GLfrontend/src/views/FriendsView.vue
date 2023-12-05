<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <!-- left side 
             col-span-1: takes 1 of the 4 columns -->
        <div class="main-left col-span-1 space-y-6"> 
            <!-- profile -->
            <div class="p-4 bg-purple_main rounded-full">
                <!-- profile picture -->
                <div class="flex items-center space-x-4">
                    <img :src="user.get_avatar" class="w-[80px] rounded-img">
                    <p class="font-semibold text-xl">{{ user.name }}</p>
                </div>
                <!-- charisma points nd posts-->
                <div class="my-5 px-12 py-4 flex flex-row justify-between items-center bg-dark_purple rounded-full text-center">
                    <div>
                        <p class="text-lg/none">{{ user.posts_count }}</p>
                        <label class="text-sm">posts</label>
                    </div>
                     <div class="font-semibold" >
                        <p class="text-lg/none">{{  user.friends_count }}</p>
                        <label class="text-sm">friends</label>
                    </div>
                
                </div>
                <!-- about me -->
            
                
            </div>  
            <!-- trending games -->
    
        </div> 
        
        <!-- center -->
        <div class="p-4 main-center col-span-2 space-y-6 rounded-full bg-purple_main">
            
            
            <div class="rounded-full p-4 space-y-6" 
            v-if="friendshipRequests.length"
            >

                <h1 class="mb-2 mx-1 text-lg font-medium">Friend Requests</h1>
                <div 
                    class="p-6 border border-dark_purple text-center rounded-full "
                    v-for="friendshipRequests in friendshipRequests"
                    v-bind:key="friendshipRequests.id"
                >
                    <img :src="friendshipRequests.created_by.get_avatar" class=" mb-4 mx-auto rounded-full">
                                 
                     @<RouterLink class="font-medium text-lg" :to="{name: 'profile', params:{'id': friendshipRequests.created_by.id}}">{{ friendshipRequests.created_by.name }}</RouterLink>
                       
                    <div class="mt-2 mb-2 flex space-x-8 justify-around">
                        <p class="text-sm text-gray-400">{{ user.friends_count }} friends </p>
                        <p class="text-sm text-gray-400">{{ user.posts_count }} posts</p>
                    </div>
                    <div class="mt-6 space-x-4">
                        <button class="inline-block py-3 px-5 hover:bg-green-500 bg-green-400 text-black text-sm font-semibold rounded-img" @click="handleRequest('accepted', friendshipRequests.created_by.id)">accept</button>
                        <button class="inline-block py-3 px-5 hover:bg-[#28183e] bg-dark_purple text-sm font-medium rounded-img" @click="handleRequest('rejected', friendshipRequests.created_by.id)">reject</button>
                    </div>
                </div>               
                
            </div>
                <!-- friends -->
            <div class="rounded-full p-4 space-y-6"               
                v-if="friends.length"> 
                <h1 class="mb-2 mx-1 text-lg font-medium">Friends</h1>
                
                <div 
                    class="p-6 border border-dark_purple text-center rounded-full "
                    v-for="user in friends"
                    v-bind:key="user.id"
                >
                    <img :src="user.get_avatar" class="w-[80px] rounded-img">
                                 
                     @<RouterLink class="font-medium text-lg" :to="{name: 'profile', params:{'id': user.id}}">{{ user.name }}</RouterLink>
                       
                    <div class="mt-1 flex space-x-4 justify-around">
                        <p class="text-sm text-gray-400">{{ user.friends_count }} friends</p>
                        <p class="text-sm text-gray-400">{{ user.posts_count }} posts</p>
                    </div>

                </div>
                 
             
            </div>

        </div>
        
        <!-- right side -->
        <div class="main-right col-span-1 space-y-6">
            

            <PeopleYouMayKnow />
          
           
        </div>


    </div> 
</template> 


<script>

import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'

import { useUserStore } from '@/stores/user'
import FeedItem from '../components/FeedItem.vue'


export default {
    name: 'FriendsView',

    setup() {
        const userStore = useUserStore()
       
        

        return {
            userStore
         
        }
    },
         
    components: {
        PeopleYouMayKnow,

        FeedItem,
    },
    data(){
        return {
            user: {},
            friendshipRequests: [],
            friends: []
        }
    }, 
    mounted() {
        this.getFriends()
    },

    methods: {
        getFriends() {
        axios
            .get(`/api/friends/${this.$route.params.id}/`)
            .then(response => {
                console.log('data', response.data)

                this.friendshipRequests = response.data.requests
                this.friends = response.data.friends
                this.user = response.data.user
            })
            .catch(error => {
                console.log('error', error)
            })
    },

        handleRequest(status, pk){
            console.log('handleRequest', status);

            axios
                .post(`/api/friends/${pk}/${status}/`)
                .then(response => {
                    console.log('data', response.data);

                    this.friendshipRequests = this.friendshipRequests.filter(request => request.created_by.id !== pk);
                    this.getFriends();
                })

                .catch(error => {
                    console.log('error', error)
                })

        }
    }
}
</script>