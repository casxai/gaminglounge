<template>

    <div data-te-infinite-scroll-init class ="max-w-screen pt-4 mx-auto grid grid-cols-4 gap-4 px-12">

        <!-- left side -->
        <div class="main-left space-y-6 sticky top-[8rem] h-screen "> 
            <LeftPanel />    
        </div>
       
        <!-- center -->
        <div class="px-4 main-center col-span-2 space-y-6">
            <div class="p-5 bg-purple_main rounded-full border-2 border-gray-400" v-for="post in posts" v-bind:key="post.id"> 
                <FeedItem :post="post" @postDeleted="handlePostDeleted" />
            </div>
        </div>

        <!-- right side -->
        <div class="main-right col-span-1 space-y-6 sticky top-[8rem] h-screen ">

            <PeopleYouMayKnow />

        </div>


    </div>
</template> 


<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import { useUserStore } from '@/stores/user'
import FeedItem from '../components/FeedItem.vue'
import LeftPanel from '@/components/LeftPanel.vue'
export default {
    name: 'BetatestingView',

    emits: ['postDeleted'],

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
    },
    data() {
        return {
            posts: [],
            body: '',
        }
    },
    mounted() {
        this.getFeed()
    },
    methods:
    {
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
        getFeed() {
            axios
                .get('/api/posts/beta_posts/')
                .then(response => {
                    console.log('data', response.data)
                    this.posts = response.data
                })
                .catch(error => {
                    console.log('error', error)
                })
        },
        search() {
            // Redirect to the search page with the query as a URL parameter
            this.$router.push({ name: 'search', query: { q: this.searchQuery } });
        },
    }
}
</script>