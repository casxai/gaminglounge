<template>

    <div data-te-infinite-scroll-init class="max-w-screen mx-auto grid grid-cols-4 gap-4 px-12 pt-4">
        <div class="main-left space-y-6 sticky h-screen "> 
            <LeftPanel />    
        </div>
       
        <!-- center -->
        <!-- col-span-2: takes 2 of the 4 columnsspace-y-4: 6 spaces each post -->
        <div class="px-4 main-center col-span-2 space-y-6 "> <!--whole feed-->
            <!-- bg-gradient-to-r from-violet-900  -->
            <!-- post area -->
                <div class="p-5 bg-purple_main rounded-full border-2 border-gray-400"  v-for="post in posts" v-bind:key="post.id">
                
                <!-- loop ng post -->

                <FeedItem :post="post" @postDeleted="handlePostDeleted"/>
            </div>
        </div>

        <!-- right side -->
        <div class="main-right col-span-1 space-y-6 sticky h-screen">
            <PeopleYouMayKnow />
        </div>
        <!-- <div
            id="spinner"
            class="hidden h-8 w-8 animate-spin rounded-full border-4 border-solid border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
            role="status">
            <span
            class="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]"
            >Loading...</span
            >
  </div> -->

    </div>
</template> 


<script>


import axios from 'axios'
import FeedForm from '../components/FeedForm.vue'
import FeedItem from '../components/FeedItem.vue'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import { useUserStore } from '@/stores/user'
import LeftPanel from '@/components/LeftPanel.vue'



export default {
    name: 'FeedView',

    emits: ['postDeleted'],

    setup() {
        const userStore = useUserStore()

        return {
            userStore,

        }
        
    },
        components: {
            PeopleYouMayKnow,
            
            LeftPanel,
            FeedItem,
            FeedForm,
            Modal,
        },
        
    data() {
    
        return {
            posts: [],
            body: '',
            currentPage: 1,
            totalPages: null,
            perPage: 5, // Set this to whatever your page size is
            hasNext: false, // Flag to indicate if there is a next page

        }
    },
    mounted() {
        this.getFeed();
        this.userStore.initStore();

        window.onscroll = () => {
            let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight === document.documentElement.offsetHeight;
            if (bottomOfWindow && this.hasNext) {
                this.currentPage += 1;
                this.getFeed();
            }
        };
    },
    methods:
    {
        getFeed() {
            axios
                .get(`/api/posts/discussion_posts/?page=${this.currentPage}`)
                .then(response => {
                    // Assuming the response structure includes 'results' for posts,
                    // and pagination information like 'next' and 'totalPages'.
                    this.posts = this.posts.concat(response.data.results);
                    this.totalPages = Math.ceil(response.data.count / this.perPage);

                    // Check if there is a next page
                    this.hasNext = !!response.data.next;

                    console.log(response.data);
                })
                .catch(error => {
                    console.log('error', error);
                });
        },
        

        handlePostDeleted(deletedPostId) {
            this.posts = this.posts.filter(post => post.id !== deletedPostId);
            // Decrement the user's posts count
            if (this.user) {
                this.user.posts_count -= 1;
            }
        },

        search() {
            // Redirect to the search page with the query as a URL parameter
            this.$router.push({ name: 'search', query: { q: this.searchQuery } });
        },
    }
}
</script>

<style lang="scss" scoped>

</style>