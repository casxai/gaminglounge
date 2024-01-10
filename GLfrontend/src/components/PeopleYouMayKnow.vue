<template>
    <div class="space-y-6">

        <div class="py-4 bg-purple_main border-gray-400 border-2 rounded-full">
            <h3 class="rounded-full font-semibold text-xl tracking-wide pl-6 mb-3">Most talked about Games</h3>

                <div v-for="(game, index) in popularGames" :key="index"
                    class="flex items-center justify-between border-gray-200 hover:bg-[#120719] text-left">
                    <div class="flex flex-col my-3 px-6">
                        <RouterLink :to="'/populargames/' + game.id" class="font-semibold text-lg w-full">
                        {{ game.title }}
                        </RouterLink>
                        <p class="text-sm text-gray-400">{{ game.num_posts }} posts</p>
                    </div>

                </div>
         
        </div>

        <!-- ------------------------- -->

        <div class="mt-4 bg-purple_main border-gray-400 border-2 rounded-full h-fit">
            <h3 class="rounded-full font-semibold text-xl tracking-wide pl-6 py-4">People you may know</h3>

            
                <div v-for="user in users" :key="user.id" class="flex items-center justify-between border-gray-200 hover:bg-[#120719] hover:rounded-full">
                    
                    <div class="justify-self-start items-center flex my-3 px-6">
                        <img :src="user.get_avatar" alt="avatar" class="h-12 rounded-img aspect-square mr-3" width="50" height="50">
                        <div class="flex flex-col">
                            <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }" >
                            <span class="font-medium">{{ user.name }}</span>
                            </RouterLink>
                            <span class=" text-sm text-gray-400">{{ user.friends_count }} friends</span>
                        </div>
 
                    </div>

                    <!-- <div>
                        <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }" class="py-3 px-6 hover:bg-[#120719] bg-[#28183e] text-sm rounded-img">
                            view
                        </RouterLink>
                    </div> -->
                </div>
       



         
        </div>

    </div>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'

export default {
    data() {
        return {
            users: [],
            popularGames: [],
        };
    },
    mounted() {
        this.getFriendSuggestions();
        this.fetchPopularGames();

    },
    methods: {
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
        fetchPopularGames() {
            axios.get('/api/posts/popular_games') // Replace with your actual API endpoint
                .then(response => {
                    this.popularGames = response.data;
                })
                .catch(error => {
                    console.error('Error fetching popular games:', error);
                });
        },

    },
    components: { RouterLink }
}

</script>