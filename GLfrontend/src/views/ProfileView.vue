<template>
    <div class="grid grid-cols-4 gap-4">

        <!-- left side 
             col-span-1: takes 1 of the 4 columns -->
        <div class="main-left md:col-span-1 col-span-4 space-y-6 md:sticky top-[8rem] h-fit "> 
            <!-- profile -->
            <div class="p-6 bg-purple_main rounded-full border border-2 border-gray-400">
                <!-- profile picture -->
                <div class="flex items-center space-x-4">
                    <img :src="user.get_avatar" class="avatar object-cover aspect-square h-[80px] w-[80px] rounded-img"> 
                    <div class="flex flex-col">
                        <p class="font-semibold text-xl">{{ user.name }}</p>
                        <div v-if="is_admin" class="text-sm inline-block">ADMIN</div>
                        <div v-if="isCloseToBan && userStore.user.id === user.id" class="p-2 bg-red-400 rounded-full border border-2 border-gray-400">
                            Account Ban Warning
                            </div>
                    </div>
                </div>
                <!-- charisma points nd posts-->
                <div class="my-5 px-12 py-4 flex flex-row justify-between items-center bg-transparent border-y-2 border-gray-400 text-center">
                    <div>
                        <p class="text-lg/none sub">{{ user.posts_count }}</p>
                        <label class="text-sm ">posts</label>
                    </div>
                    <div>
                        <p class="text-lg/none sub">{{ user.charisma_score }}</p>
                        <label class="text-sm ">charisma</label>
                    </div>
                    <div>
                        <p class="text-lg/none sub">{{ user.friends_count }}</p>
                        <RouterLink :to="{name: 'friends', params: {id: user.id}}" class="text-sm">friends</RouterLink>
                    </div>
                    
                </div>
                <!-- about me -->
                <p v-if="user.bio" class="px-1 text-justify sub">{{ user.bio }}</p>

                <!-- send friend request button -->
                <div class = "md:mt-6 buttons">
                    <button 
                        class = "inline-block md:py-3 inside hover:bg-purple-600 bg-[#28183e] font-semibold rounded-full w-full sub" 
                        @click="sendFriendshipRequest"
                        v-if="userStore.user.id !== user.id 
                        && can_send_friendship_request"
                        >
                        add friend
                    </button>
                    <button 
                        class = "inline-block md:py-3 md:mt-4 inside hover:bg-purple-600 bg-[#28183e] font-semibold rounded-full w-full sub" 
                        @click="sendDirectMessage"
                        v-if="userStore.user.id !== user.id
                        && can_send_message
                        "
                        >
                        send message
                    </button> 
                    
                    <!-- edit profile button -->
                    <RouterLink
                        class = "inline-block md:py-3 inside md:my-4 text-center hover:bg-[#120719] bg-[#28183e] font-semibold rounded-full w-full sub" 
                        to="/profile/edit"
                        v-if="userStore.user.id === user.id"
                        >
                        edit profile
                    </RouterLink> 

                    <!-- Logout button -->
                    <button 
                        class = "inline-block inside md:py-3 hover:bg-red-400 bg-[#28183e] font-semibold rounded-full w-full sub" 
                        @click="logout"
                        v-if="userStore.user.id === user.id"
                        >
                        logout
                    </button> 
                 </div>
            </div>  
        </div> 
        
        <!-- center -->
            <!-- col-span-2: takes 2 of the 4 columns
                 space-y-4: 6 spaces each post -->
        <div class="md:px-4 main-center md:col-span-2 col-span-4 space-y-6">
            <!-- write something -->
            <div class="feed" v-if="userStore.user.id === user.id"> <!--modal design-->
                    <Modal @close="toggleModal" :modalActive="modalActive">
                        <div class="rounded-full bg-transparent space-y-1 text-right model-content">
                           
                            <FeedForm v-bind:user="null" v-bind:posts="posts"/>
                        </div>
                    </Modal>
                <div class="flex items-center justify-between bg-purple_main border-2 border-gray-400 rounded-full space-x-2 p-4">
                    <img :src="userStore.user.avatar" alt="user.profile" class="avatar object-cover  aspect-square w-14 h-14 rounded-img">
                    <button @click="toggleModal" class="md:py-4 md:px-3 w-full md:bg-[#28183e] bg-opacity-100 rounded-img text-left transition-colors duration-150 focus:shadow-outline md:hover:bg-[#120719]"> 
                        <span class="text-gray-400 pl-2 sub">lets talk gaming?</span>
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
            <div class="p-6 bg-purple_main border-gray-400 border-2 rounded-full h-fit sticky top-[8rem] hide-on-mobile">
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

</template> 

<style scoped>
input[type="file"] {
    display: none;
}
.custom-file-upload {
    border: 1px solid #ccc;
    display: inline-block;
    padding: 6px 12px;
    cursor: pointer;
}

@media (max-width: 768px) {
  .hide-on-mobile {
    display: none; /* Hide the logo on smaller screens */
  }
  .buttons {
    margin-top: 10px;
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
  .main {
    font-size: 16px;
  }
  .sub {
    font-size: 14px;
  }

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
            is_admin: false,
            posts:[],
            user: {
                id: ''
            },
            can_send_friendship_request: null,
            can_send_message: null,
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
                    this.can_send_message = response.data.can_send_message
                    this.is_admin = response.data.is_admin
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