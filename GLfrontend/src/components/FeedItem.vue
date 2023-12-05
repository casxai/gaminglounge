<template>

    <div class="px-2">
        <!-- top part ng post-->
        <div class="mb-4 flex items-center justify-between">
            <!-- username nd pfp -->
            <div class="flex items-center space-x-2">
                <img :src="post.created_by.get_avatar" class="h-[50px] w-[50px] rounded-img">
                <div>
                    <p class="font-semibold text-xl tracking-wide">
                    <RouterLink :to="{ name: 'profile', params: { 'id': post.created_by.id } }">{{ post.created_by.name }}
                    </RouterLink>
                    </p>
                <!-- time posted -->
                <p class="text-gray-300 text-xs font-light">{{ post.created_at_formatted }}</p>
                </div>
            </div>
            <p class="mb-4 tracking-wider font-semibold">{{ post.game_title ? post.game_title.title : 'No Game Title' }}</p>
        </div>

        <!--  -->
        <p class="mb-4 text-base/7">{{ post.body }}</p>

        <template v-if="post.attachments && post.attachments.length">
            <div v-for="image in post.attachments" :key="image.id">
                <img v-if="image.get_image !== null && image.get_image !== 'self'" :src="getCorrectImageUrl(image.get_image)"
                    class="w-full mb-4 rounded-xl">
                <!-- Your small icon HTML or any other content goes here, outside the img element -->
            </div>
        </template>
        <template v-if="post.post_url">
            <p class="text">
                SOURCE:
                <a :href="post.post_url" target="_blank" class="italic text-blue-400 hover:text-blue-500 break-words">
                    {{ post.post_url }}
                </a>
            </p>
        </template>
        <!-- lower part ng post -->
        <div class="mt-6 flex flex-row justify-between">
                <div class="flex space-x-6">
                                    <!-- likes -->
                        <div @mouseenter="isHovered = true" @mouseleave="isHovered = false" class="flex items-center space-x-3" @click="likePost(post.id)" >
                            <svg  xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" width="30" height="30" :class="{ 'fill-red': isHovered }">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z">
                                </path>
                            </svg>
                            <span class="text-gray-300 ">{{ post.likes_count }} likes</span>
                        </div>
                        <!-- comments -->
                        <div class="flex items-center space-x-3">
                            <RouterLink :to="{ name: 'postview', params: { id: post.id } }" class="cursor-pointer">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                    stroke="currentColor" width="30">
                                    <path stroke-linecap="round" stroke-linejoin="round"
                                        d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z">
                                    </path>
                                </svg>
                            </RouterLink>
                            <RouterLink :to="{ name: 'postview', params: { id: post.id } }" class="text-gray-300">{{
                                post.comments_count }} comments</RouterLink>
                        </div>
                        <div v-if="post.is_private" class="flex items-center space-x-2 text-gray-300 text-xs">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                                stroke="currentColor" width="35" height="30">
                                <path stroke-linecap="round" stroke-linejoin="round"
                                    d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                            </svg>
                            <span>private post</span>
                </div>


                </div>

                <div> <!-- three dots -->
                    <div @click="toggleExtraModal" class="">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2"
                            stroke="currentColor" width=30>
                            <path stroke-linecap="round" stroke-linejoin="round"
                                d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z">
                            </path>
                        </svg>
                    </div>
                </div>

            </div>
       

        <div v-if="showExtraModal">
            <div class="flex mt-2 space-x-6 items-center">
                <div class="flex items-center space-x-2 delete-button" @click="deletePost(post.id)">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-6 h-6 text-red-500">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                    </svg>
                    <span class="text-red-500 text-xs">delete post</span>
                </div>

                <div class="flex items-center space-x-2" @click="reportPost">
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                        stroke="currentColor" class="w-6 h-6 text-orange-500">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M3 3v1.5M3 21v-6m0 0l2.77-.693a9 9 0 016.208.682l.108.054a9 9 0 006.086.71l3.114-.732a48.524 48.524 0 01-.005-10.499l-3.11.732a9 9 0 01-6.085-.711l-.108-.054a9 9 0 00-6.208-.682L3 4.5M3 15V4.5" />
                    </svg>
                    <span class="text-orange-500 text-xs">report post</span>
                </div>


            </div>
        </div>
    </div>
</template>

<style>
.word-wrap {
    word-wrap: break-word;
    /* Older browsers */
    word-break: break-word;
    /* As of CSS 3.0 */
    overflow-wrap: break-word;
    /* Preferred for CSS3 */
}

.text-overflow {
    white-space: nowrap;
    /* Keep the text on a single line */
    overflow: hidden;
    /* Hide the overflow text */
    text-overflow: ellipsis;
    /* Show ellipsis */
}

.break-words {
    word-break: break-all;
}
</style>


<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
import { useToastStore } from '@/stores/toast'

export default {
    props: {
        post: Object
    },

    emits: ['postDeleted'],

    setup() {
        const userStore = useUserStore()
        const toastStore = useToastStore()

        return {
            userStore,
            toastStore
        }
    },

    data() {
        return {
            showExtraModal: false,
            isHovered: false,
        
          
        }
    },
    mounted() {

    },

    methods: {
        getCorrectImageUrl(imageSource) {
       
            return imageSource;
        },
   
        likePost(id) {

            axios
            
                .post(`/api/posts/${id}/like/`)
                .then(response => {
                    if (response.data.message == 'like created') {
                       
                        this.post.likes_count += 1;
                    }
                })
                .catch(error => {
                    console.log('error', error);
                });
        },
        reportPost() {
            axios
                .post(`/api/posts/${this.post.id}/report/`)
                .then(response => {
                    console.log(response.data)

                    this.toastStore.showToast(5000, 'The post was reported', 'bg-emerald-500')
                })
                .catch(error => {
                    console.log('error', error);
                });
        },

        deletePost(postId) {
            axios
                .delete(`/api/posts/${postId}/delete/`)
                .then(response => {
                   
                    this.$emit('postDeleted', postId);
                    
                    // Update the client-side state
                    this.posts = this.posts.filter(post => post.id !== postId);

                    // Decrement the post count on the user
                    this.userStore.decrementPostCount(); // Assuming you have a method to decrement the post count in your user store

                    // Optionally display a success message
                    console.log(response.data.message);
                })
                .catch(error => {
                    // Handle any errors
                    console.error('Error deleting post:', error);
                });
        },

        toggleExtraModal() {
            console.log('toggleExtraModal')

            this.showExtraModal = !this.showExtraModal
        }
    },
}
</script>

<style>
.fill-red {
    fill: rgb(248 113 113); 
}
</style>