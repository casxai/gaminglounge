<template>
    <div class="max-w-screen px-12 pt-4 mx-auto grid grid-cols-4 gap-4">

        <!-- left side 
             col-span-1: takes 1 of the 4 columns -->
        <div class="main-left col-span-1 space-y-6 sticky top-[8rem] h-screen "> 
            <!-- profile -->
            <div class="p-6 bg-purple_main rounded-full border border-2 border-gray-400">
                <!-- profile picture -->
                <div class="flex items-center space-x-4">
                    <img :src="user.get_avatar" class="h-[80px] w-[80px] rounded-img"> 
                    <p class="font-semibold text-xl">{{ user.name }}</p>
                    <!-- Conditionally display the warning -->
                    <div v-if="isCloseToBan" class="p-6 bg-red-400 rounded-full border border-2 border-gray-400">
                        Account Ban Warning
                    </div>
                </div>
                <!-- charisma points nd posts-->
                <div class="my-5 px-12 py-4 flex flex-row justify-between items-center bg-transparent border-y-2 border-gray-400 text-center">
                    <div>
                        <p class="text-lg/none">{{ user.posts_count }}</p>
                        <label class="text-sm">posts</label>
                    </div>
                    <div>
                        <p class="text-lg/none">{{ user.charisma_score }}</p>
                        <label class="text-sm">charisma</label>
                    </div>
                    <div>
                        <p class="text-lg/none">{{ user.friends_count }}</p>
                        <RouterLink :to="{name: 'friends', params: {id: user.id}}" class="text-sm">friends</RouterLink>
                    </div>
                    
                
                </div>
                <!-- about me -->
                <p class="px-1 text-justify">{{ user.bio }}</p>
                
                <!-- send friend request button -->
                <div class = "mt-6">
                    <button 
                        class = "inline-block py-3 hover:bg-purple-600 bg-[#28183e] font-semibold rounded-full w-full" 
                        @click="sendFriendshipRequest"
                        v-if="userStore.user.id !== user.id 
                        && can_send_friendship_request"
                        >
                        add friend
                    </button>
                    <button 
                        class = "inline-block py-3 mt-4 hover:bg-purple-600 bg-[#28183e] font-semibold rounded-full w-full" 
                        @click="sendDirectMessage"
                        v-if="userStore.user.id !== user.id
                        "
                        >
                        send message
                    </button> 
                    
                    <!-- edit profile button -->
                    <RouterLink
                        class = "inline-block py-3 my-4 text-center hover:bg-[#120719] bg-[#28183e] font-semibold rounded-full w-full" 
                        to="/profile/edit"
                        v-if="userStore.user.id === user.id"
                        >
                        edit profile
                    </RouterLink> 

                    <!-- Logout button -->
                    <button 
                        class = "inline-block py-3 hover:bg-red-400 bg-[#28183e] font-semibold rounded-full w-full" 
                        @click="logout"
                        v-if="userStore.user.id === user.id"
                        >
                        logout
                    </button> 
                 </div>
            </div>  
            
            <div class="p-6 bg-purple_main border-gray-400 border-2 rounded-full">
                <h3 class="mb-4 font-semibold text-xl tracking-wide text-center">get your game on at gaming lounge!</h3>
            
            <div class="flex items-center justify-between"> 
                                             
                        <p class="text-justify lowercase">Welcome to your ultimate gamer destination, designed for gamers by gamers! Our platforms allow you to connect through forums, tournaments, marketplace and more - all centered around gaming.<br><br>

                            We encourage open and passionate discussion while fostering a positive community. Our Offensive Language Sheriff system automatically detects and discourages negative behavior. Users gain points for engagement like making connections, commenting, and participating, keeping conversations uplifting.<br><br>

                            At Gaming Lounge you can share wisdom, find squads, and talk games to your heart's content in an inclusive space. Just bring your A-game attitude and get involved in our community - the positivity you spread will continue to shape this space for all gamers.<br><br>

                            So get your game on with us and experience gaming's finest digital playground! Join passionate, like-minded gamers where you direct the vibe. We can't wait for you to plug into our supportive community and make it even better.
                        </p>
              

            </div>

            </div>
        </div> 
        
        <!-- center -->
            <!-- col-span-2: takes 2 of the 4 columns
                 space-y-4: 6 spaces each post -->
        <div class="px-4 main-center col-span-2 space-y-6">
            <!-- write something -->
            <div class="feed"> <!--modal design-->
                    <Modal @close="toggleModal" :modalActive="modalActive">
                        <div class="rounded-full bg-transparent space-y-1 text-right model-content">
                           
                            <FeedForm v-bind:user="null" v-bind:posts="posts"/>
                        </div>
                    </Modal>
                <div class="flex items-center justify-between bg-purple_main border-2 border-gray-400 rounded-full space-x-2 p-4">
                    <img :src="userStore.user.avatar" alt="user.profile" class="w-14 h-14 rounded-img">
                    <button @click="toggleModal" class="py-4 px-3 w-full  bg-[#28183e] bg-opacity-100 rounded-img text-left transition-colors duration-150 focus:shadow-outline hover:bg-[#120719]"> 
                        <span class="text-gray-400 pl-2 ">lets talk gaming?</span>
                    </button>
                </div>

            </div>
            <!-- post -->     
            <div class="p-5 bg-purple_main rounded-full border-2 border-gray-400"
                    v-for="post in posts" 
                    v-bind:key="post.id"> <!-- loop ng post -->

                    <FeedItem :post="post" @postDeleted="handlePostDeleted" />
            </div>
        </div>
        
        <!-- right side -->
        <div class="main-right col-span-1 space-y-6 sticky top-[8rem] h-screen ">
            
            <div class="p-6 bg-purple_main border-gray-400 h-fit border-2 rounded-full ">

<h3 class="mb-4 font-semibold text-xl tracking-wide text-center">Useful Links</h3>
<div class="space-y-4">
     
        <div class="game news">  
           
            <ul class="menu space-y-2">
                <p class="font-semibold">Gaming News:</p>
                <li class="hover:underline ">
                  <a href="https://www.gamespot.com/" target="_blank" rel="noopener noreferrer" class="flex items-center">
                       
                        <span>GameSpot</span>
                </a>
                </li>

                <li class="hover:underline">
                    <a href="https://www.ign.com/news" target="_blank" rel="noopener noreferrer" class="flex items-center">
                       <span>IGN</span></a>
                      </li>

                      <li class="hover:underline">
                          <a href="https://www.polygon.com/" target="_blank" rel="noopener noreferrer" class="flex items-center"><span>Polygon</span></a>
                      </li>

                      <li class="hover:underline">
                          <a href="https://www.thegamer.com/" target="_blank" rel="noopener noreferrer" class="flex items-center"><span>TheGamer</span></a>
                      </li>
               
          </ul>
        </div>
        <div class="game gears">  
            <ul class="menu space-y-2">
                <p class="font-semibold">Gaming Gears:</p>
                <li class="hover:underline">
                  <a href="https://www.razer.com/ap-en" target="_blank" rel="noopener noreferrer" class="flex items-center">
                       
                        <span>Razer</span>
                </a>
                </li>

                <li class="hover:underline">
                    <a href="https://www.logitechg.com/" target="_blank" rel="noopener noreferrer" class="flex items-center">
                       <span>Logitech</span></a>
                      </li>

                      <li class="hover:underline">
                          <a href="https://www.sony.com.ph/gaming-gear" target="_blank" rel="noopener noreferrer" class="flex items-center"><span>Sony</span></a>
                      </li>
                      <li class="hover:underline">
                          <a href="https://hyperx.com/" target="_blank" rel="noopener noreferrer" class="flex items-center"><span>HyperX</span></a>
                      </li>
                      <li class="hover:underline">
                          <a href="https://www.corsair.com/us/en" target="_blank" rel="noopener noreferrer" class="flex items-center"><span>Corsair</span></a>
                      </li>
                  </ul>
        </div>
       


        <div class="download games">  
              
                  <ul class="menu">
                    <p class="font-semibold">Download Games:</p>
                    <div class="space-y-2">
                        <li class="hover:underline">
                          <a href="https://www.riotgames.com/en" target="_blank" rel="noopener noreferrer" class="flex items-center">
                              <img src="/assets/img/logo/riot_logo.png" class="h-auto max-w-full" alt="logo" />
                              <span>Riot Games</span>
                          </a>
                      </li>

                      <li class="hover:underline">
                          <a href="https://store.steampowered.com/" target="_blank" rel="noopener noreferrer" class="flex items-center"><img
                                  src="/assets/img/logo/steam_logo.png" class="h-auto max-w-full" alt="logo" /><span>Steam Games</span></a>
                      </li>
                  
                    
                        <li class="hover:underline">
                          <a href="https://store.epicgames.com/en-US/" target="_blank" rel="noopener noreferrer" class="flex items-center"><img
                                  src="/assets/img/logo/epic_logo.png" class="h-auto max-w-full" alt="logo" /><span>Epic Games</span></a>
                      </li>

                      <li class="hover:underline">
                          <a href="https://us.shop.battle.net/en-us" target="_blank" rel="noopener noreferrer" class="flex items-center"><img
                                  src="/assets/img/logo/battle_logo.png" class="h-auto max-w-full" alt="logo" /><span>Battle.net</span></a>
                      </li>
                    </div>

             
                  </ul>
        </div>
        
</div>
</div>
            
        
            </div>

            
    
        </div>

</template> 

<style>
input[type="file"] {
    display: none;
}
.custom-file-upload {
    border: 1px solid #ccc;
    display: inline-block;
    padding: 6px 12px;
    cursor: pointer;
}
</style>

<script>
import axios from 'axios'
import { computed } from 'vue'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Modal from '@/components/Modal.vue';
import FeedForm from '../components/FeedForm.vue'
import FeedItem from '@/components/FeedItem.vue'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

import {ref} from 'vue'

export default {
    name: 'ProfileView',

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()
        const modalActive = ref(false)
        const toggleModal = () => {
            modalActive.value = !modalActive.value;
        }
        return {
            userStore,
            toastStore,
            modalActive,
            toggleModal,
        }
    },
        
    components: {
        PeopleYouMayKnow,
        Modal,
        FeedItem,
        FeedForm
    },
    data(){
        return {
            isCloseToBan: false,
            posts:[],
            user: {
                id: ''
            },
            can_send_friendship_request: null,
            // currentPage: 1,
            // totalPages: null,
            // perPage: 5, // Set this to whatever your page size is
            // hasNext: false, // Flag to indicate if there is a next page
        }
    }, 
    mounted() {
        this.getFeed();
        this.getUserPostCount(); // Fetch and update user's post count
        this.getCharismaScore();
        // this.userStore.initStore();

        // window.onscroll = () => {
        //     let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
        //     if (bottomOfWindow && this.hasNext) {
        //         this.currentPage += 1;
        //         this.getFeed();
        //     }
        // };

    },
    watch: {
        '$route.params.id': {
            handler: function() {
                this.getFeed()
            },
            deep: true,
            immediate: true 
        }
    },
 
    methods: {
        deletePost(id) {
            // Filter out the deleted post
            this.posts = this.posts.filter(post => post.id !== id);
        },

        handlePostDeleted(deletedPostId) {
            this.posts = this.posts.filter(post => post.id !== deletedPostId);
            // Decrement the user's posts count
            if (this.user) {
                this.user.posts_count -= 1;
            }
        },

        sendDirectMessage() {
            console.log('sendDirectMessage')

            axios
                .get(`api/chat/${this.$route.params.id}/get-or-create/`)
                .then(response => {
                    console.log(response.data)

                    this.$router.push('/chat')
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        sendFriendshipRequest() {
            axios
            .post(`/api/friends/${this.$route.params.id}/request/`) 
                .then(response => {
                    console.log('data', response.data)

                    this.can_send_friendship_request = false

                    if (response.data.message == 'request already sent')
                    {
                        this.toastStore.showToast(5000, 'The request has already been sent', 'bg-red-400')
                    }
                    else{
                        this.toastStore.showToast(5000, 'The request was sent!', 'bg-emerald-500')
                         // Update friends count if the request was successful
                        if (response.data.request_accepted) {
                             // Update friends count if the request was accepted
                            this.user.friends_count += 1; // Increment friends count here
                        }
                    }
                })
                .catch(error => {
                    console.log('error', error)
                })
        },

        getFeed(){
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`) //using ` for the js
                .then(response => {
                    console.log('data', response.data)

                    this.posts = response.data.posts
                    this.user = response.data.user
                    this.can_send_friendship_request = response.data.can_send_friendship_request
                    this.isCloseToBan = response.data.is_close_to_ban || false;
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        getUserPostCount() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/post_count/`)
                .then((response) => {
                // Update the user's post count in the component state
                this.user.posts_count = response.data.posts_count;
                })
                .catch((error) => {
                console.error('Error fetching user post count', error);
                });
        },
        getCharismaScore() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/charisma_score/`)
                .then((response) => {
            
                // Update the user's post count in the component state
                this.user.charisma_score = response.data.charisma_score_count;
                })
                .catch((error) => {
                console.error('Error fetching user charisma score', error);
                });
        },
        logout() {
        
            this.userStore.removeToken()

            this.$router.push('/')
        }
    }
}
</script>