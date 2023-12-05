<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">

        <div class="main-left col-span-1 space-y-6"> 
            <!-- trending games -->
            <LeftPanel />
        </div> 
        <div class="col-span-2 space-y-2 ">
            <div class="bg-purple_main rounded-tr-full rounded-tl-full">            
                <!-- post area -->     
                <div class="p-4 text-lg border-b border-gray-400  rounded-tr-full rounded-tl-full"
                        v-if="post.id">

                    <FeedItem v-bind:post="post" />             
                </div>

                
                <!-- comment area -->
                <div 
                    class="py-4 pl-8 pr-4 border-b border-gray-400 "
                    v-for="comment in post.comments"
                    v-bind:key="comment.id"
                >
                    <CommentItem v-bind:comment="comment"/>
                </div>   
            </div>
            <!-- write something comment -->
             
                <form v-on:submit.prevent="submitForm"
                    method="post">
                        <div class="flex items-center px-3 py-2 rounded-br-full rounded-bl-full dark:bg-purple_main">
                            <textarea v-model="body" rows="2" class="bg-purple_main block mr-2 p-2.5 w-full rounded-br-full rounded-bl-full" placeholder="say something about this post.."></textarea>
                                <button type="submit" class="inline-flex justify-center p-3 rounded-img cursor-pointer hover:bg-[#28183e]">
                                <svg class="w-6 h-6 rotate-90" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="white" viewBox="0 0 18 20">
                                    <path d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z"/>
                                </svg>
                                </button>
                        </div>
                </form>

            
        </div>
        
        <!-- right side -->
        <div class="main-right col-span-1  space-y-6">
            <PeopleYouMayKnow />
     
        </div>


    </div> 
</template> 


<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import { useUserStore } from '@/stores/user'
import FeedItem from '../components/FeedItem.vue'
import CommentItem from '../components/CommentItem.vue'
import LeftPanel from '@/components/LeftPanel.vue'
export default {
    name: 'PostView',


    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },
    components: {
        PeopleYouMayKnow,
        LeftPanel,
        FeedItem,
        CommentItem,
    },
    data(){
        return {
            post:{
                id: null,
                comments: [],
          
            },
            body: ''
        }
    },
    mounted(){
        this.getPost()
    },

    methods: 
    {
        getPost()
        {
            axios
                .get(`/api/posts/${this.$route.params.id}/`)
                .then(response => {
                    console.log('data', response.data)

                    this.post = response.data.post
                })
                .catch(error => {
                    console.log('error', error)
                })
        },  
        submitForm()
        {
            console.log('submitForm', this.body) //textarea v-model="body" 

            axios //sending to backend
                .post(`/api/posts/${this.$route.params.id}/comment/`, 
                {
                    'body': this.body
                })
                .then(response =>{
                    console.log('data', response.data)

                    this.post.comments.push(response.data)
                    this.post.comments_count += 1
                    this.body = ''
                })
                .catch(error =>{
                    console.log('error', error)
                })
        },
        search() 
        {
        // Redirect to the search page with the query as a URL parameter
        this.$router.push({ name: 'search', query: { q: this.searchQuery } });
        },
    }
}
</script>