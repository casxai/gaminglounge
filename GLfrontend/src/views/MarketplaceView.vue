<template>
  
    <div data-te-infinite-scroll-init class="grid grid-cols-4 gap-6">
        <!-- left side -->
        <div class="main-left space-y-6 sticky top-[8rem] h-fit hide-on-mobile"> 
            <LeftPanel /> 
        </div>

       

        <!-- center side -->
        <div data-te-infinite-scroll-init class="main-center md:col-span-2 col-span-4 space-y-6 ">
         
            <div class="p-5 bg-purple_main rounded-full border-2 border-gray-400" v-for="post in posts" v-bind:key="post.id"> 
                <FeedItem :post="post" @postDeleted="handlePostDeleted" />
            </div>

        </div>

        <!-- right side -->
        <div class="main-right col-span-1 space-y-6 top-[8rem] h-fit sticky hide-on-mobile">

            <PeopleYouMayKnow />

            </div>

    </div>
</template> 

<style scoped>
@media (max-width: 768px) {
  .hide-on-mobile {
    display: none; /* Hide the logo on smaller screens */
  }

}
</style>
<script>
import axios from 'axios'
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import { useUserStore } from '@/stores/user'
import FeedItem from '../components/FeedItem.vue'
import LeftPanel from '@/components/LeftPanel.vue'
export default {
    name: 'MarketplaceView',

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
        // getFeed() {
        //     axios
        //         .get('/api/posts/marketplace_posts/')
        //         .then(response => {
        //             console.log('data', response.data)
        //             this.posts = response.data
        //         })
        //         .catch(error => {
        //             console.log('error', error)
        //         })
        // },
        getFeed() {
            axios
                .get(`/api/posts/marketplace_posts/?page=${this.currentPage}`)
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
        search() {
            // Redirect to the search page with the query as a URL parameter
            this.$router.push({ name: 'search', query: { q: this.searchQuery } });
        },
    }
}
</script>