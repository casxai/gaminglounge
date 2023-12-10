<template>
    <div class="space-y-6">
        <div class="p-6 bg-purple_main border-gray-400 border-2 rounded-full">
            <h3 class="mb-2 font-semibold text-xl tracking-wide text-center">Leaderboards</h3>

            <div class="text-left">
                <div v-for="user in leaderboard" :key="user.id"
                    class="flex items-center justify-between border-b-2 font-medium">

                    <div class="justify-self-start flex py-4">
                        <img :src="user.avatar" alt="avatar" class="h-12 rounded-img" width="50" height="50">
                        <div class="flex flex-col">
                            <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }"><span class="font-semibold">{{
                                user.name }}</span>
                            </RouterLink>
                            <span class="">{{ user.charisma_score }}</span>
                        </div>
                    </div>

                </div>
            </div>

        </div>
        <div class="p-6 bg-purple_main border-gray-400 border-2 rounded-full">
            <h3 class="mb-2 font-semibold text-xl tracking-wide text-center">Most talked about Games</h3>
            <div class="space-y-4 text-left">
                <div v-for="(game, index) in popularGames" :key="index"
                    class="flex items-center justify-between border-b-2 lowercase font-medium">
                    <RouterLink :to="'/populargames/' + game.id" class="text-lg w-full py-2">
                        {{ game.title }}
                    </RouterLink>
                    <p class="text">{{ game.num_posts }}</p>
                </div>
            </div>
        </div>


        <div class="p-6 bg-purple_main border-gray-400 border-2 rounded-full">
            <h3 class="mb-2 font-semibold text-xl tracking-wide text-center">People you may know</h3>

<div class="text-left">
    <div v-for="user in users" :key="user.id" class="flex items-center justify-between border-b-2 font-medium">
        <div class="flex items-center py-4">
            <img :src="user.get_avatar" alt="avatar" class="h-12 rounded-img" width="50" height="50">
            <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }" class="ml-4">
                <span class="font-semibold">{{ user.name }}</span>
            </RouterLink>
        </div>

        <div>
            <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }">
                <a href="#" class="py-3 px-4 bg-violet-600 text-white rounded-lg">Follow</a>
            </RouterLink>
        </div>
    </div>
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
            leaderboard: [],
        };
    },
    mounted() {
        this.getFriendSuggestions();
        this.fetchPopularGames();
        this.fetchLeaderboard();
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
        fetchLeaderboard() {
            axios.get('/api/leaderboard') // Replace with your actual API endpoint
                .then(response => {
                    this.leaderboard = response.data;
                })
                .catch(error => {
                    console.error('Error fetching leaderboard:', error);
                });
        },
    },
    components: { RouterLink }
}

</script>