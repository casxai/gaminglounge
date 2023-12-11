<template>
  
    <div class="py-4 bg-purple_main border-gray-400 border-2 rounded-full">
            <h3 class="rounded-full font-semibold text-xl tracking-wide pl-7 mb-3">Leaderboards</h3>

    
                <div v-for="user in leaderboard" :key="user.id"
                    class="flex items-center justify-between border-gray-200 hover:bg-[#120719] rounded-full text-left ">

                    <div class="justify-self-start items-center flex my-3 px-6">
                        <img :src="user.avatar" alt="avatar" class="h-12 rounded-img" width="50" height="50">
                        <div class="flex flex-col">
                            <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }"><span class=" font-medium">{{
                                user.name }}</span>
                            </RouterLink>
                            <span class="text-sm text-gray-400">{{ user.charisma_score }} charisma</span>
                        </div>
                    </div>

        
                </div>

        </div>
    <!-- game links -->
    <div class="p-6 bg-purple_main border-gray-400 h-fit border-2 rounded-full ">
        
        <!-- <h3 class="mb-2 font-semibold text-xl tracking-wide ">Useful Links</h3> -->
            <div class="space-y-4">
                <div class="game news ">  
                    <p class="font-semibold">Gaming News:</p>
                   <ul class=" flex flex-wrap justify-between ml-6 mt-1">
                            <li class="hover:underline ">
                                <a href="https://www.gamespot.com/" target="_blank" rel="noopener noreferrer">  
                                    <span>GameSpot</span>
                                </a>
                            </li>

                       

                            <li class="hover:underline">
                                <a href="https://www.polygon.com/" target="_blank" rel="noopener noreferrer"><span>Polygon</span></a>
                            </li>

                            <li class="hover:underline">
                                <a href="https://www.thegamer.com/" target="_blank" rel="noopener noreferrer" ><span>TheGamer</span></a>
                            </li>
                       
                  </ul>
                </div>
                <div class="game gears">  
                    <p class="font-semibold">Gaming Gears:</p>
                    <ul class="ml-6 mt-1 flex flex-wrap justify-between">
                        
                        <li class="hover:underline">
                          <a href="https://www.razer.com/ap-en" target="_blank" rel="noopener noreferrer">
                               
                                <span>Razer</span>
                        </a>
                        </li>

                        <li class="hover:underline">
                            <a href="https://www.logitechg.com/" target="_blank" rel="noopener noreferrer">
                               <span>Logitech</span></a>
                              </li>

                        
                              <li class="hover:underline">
                                  <a href="https://hyperx.com/" target="_blank" rel="noopener noreferrer"><span>HyperX</span></a>
                              </li>
                              <li class="hover:underline">
                                  <a href="https://www.corsair.com/us/en" target="_blank" rel="noopener noreferrer"><span>Corsair</span></a>
                              </li>
                    </ul>
                </div>
               
                <div class="download games">  
                    <p class="font-semibold">Download Games:</p>
                   
                          <ul class="menu flex flex-wrap justify-between ml-6 mt-2 gap-3">
                            
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

              

                     
                          </ul>
                        </div>
                </div>
                
        </div>
  


</template>
<style>

img{
    margin-right: 10px;
}

ul{
    list-style: none;
    padding: 0;
    margin: 0;
}

li{
    display: inline-block;
    margin-right: 10px;
 
}
</style>
<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'

export default {
    data() {
        return {
            users: [],
            leaderboard: [],
        };
    },
    mounted() {

        this.fetchLeaderboard();
    },
    methods: {
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