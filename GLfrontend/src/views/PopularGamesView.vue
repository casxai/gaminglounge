<template>

    <div data-te-infinite-scroll-init class="grid grid-cols-4 gap-4">
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
    name: 'PopularGamesView',
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
    },
    data() {
        return {
            posts: [],
            currentPage: 1,
            totalPages: null,
            hasNext: false,
        }
    },
    mounted() {
        this.getPostsForGame();
        this.userStore.initStore();

        window.onscroll = () => {
            let bottomOfWindow = document.documentElement.scrollTop + window.innerHeight > document.documentElement.offsetHeight - 100; // 100px threshold
            if (bottomOfWindow && this.hasNext) {
                this.currentPage++;
                this.getPostsForGame();
            }
        };
    },
    methods: {
        getPostsForGame() {
            axios
                .get(`/api/posts/popular_game/${this.$route.params.id}/?page=${this.currentPage}`)
                .then(response => {
                    this.posts = [...this.posts, ...response.data.results];
                    this.totalPages = Math.ceil(response.data.count / response.data.results.length);
                    this.hasNext = !!response.data.next;
                })
                .catch(error => {
                    console.error('Error fetching posts:', error);
                });
        },
        handlePostDeleted(deletedPostId) {
            this.posts = this.posts.filter(post => post.id !== deletedPostId);
        },
    }
}
</script>

<style lang="scss" scoped>

</style>