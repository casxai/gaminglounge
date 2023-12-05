<template>
    <!-- scroll: h-full overflow-y-scroll -->
    <div class="max-w-screen mx-auto grid grid-cols-4 gap-4 px-12 pt-4">
        <!-- inbox -->
        <div class="main-left col-span-1 flex flex-col bg-purple_main rounded-full p-6 overflow-auto h-full">
            
            <label for="" class="text-center text-xl font-semibold border-b pb-4">messages</label>

                        <a 
                            class="mt-4 flex justify-between items-center" 
                            v-for="conversation in conversations"
                            v-bind:key="conversation.id"
                           
                            v-on:click="setActiveConversation(conversation.id)"
                        >
                            <div class="flex  p-2 ">
                                <div
                                    v-for="user in conversation.users"
                                    v-bind:key="user.id"
                                    class=""
                                >
                                    <div class="flex flex-row items-center">
                                        <img :src="user.get_avatar" class="w-[45px] rounded-img ">

                                        <p 
                                            class="font-semibold text-base pr-8"
                                            v-if="user.id !== userStore.user.id"
                                            >
                                            {{ user.name }} 
                                        </p>
                                    </div>
                                
                                </div>
                            </div>    
                            <span class="text-xs text-white font-light ">{{ conversation.modified_at_formatted }}</span>
                            
                        </a>

        </div>
        <!-- messages -->
        <div class="main-center col-span-3 space-y-4">
            <div class="bg-purple_main rounded-full">
                <div class="flex flex-col flex-grow p-6">
                    
                        <template 
                            v-for="message in activeConversation.messages" 
                            v-bind:key="message.id"
                        >
                            <div 
                                class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
                                v-if="message.created_by.id == userStore.user.id"
                            >
                                <div>
                                    <div class="bg-[#181327] text-white p-3 rounded-l-full rounded-br-full">
                                        <p class="text-sm">{{ message.body }}</p>
                                    </div>
                                    <span class="text-xs text-gray-400 font-light leading-none"> {{ message.created_at_formatted }} ago</span>
                                </div>
                                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                    <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full">
                                </div>
                            </div>

                            <div 
                                class="flex w-full mt-2 space-x-3 max-w-md"
                                v-else
                            >
                                    <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                        <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full">
                                    </div>
                                    <div>
                                        <div class="bg-[#181327] p-3 rounded-r-full rounded-bl-full">
                                            <p class="text-sm">{{ message.body }}</p>
                                        </div>
                                        <span class="text-xs text-gray-400 font-light leading-none">{{ message.created_at_formatted }} ago</span>
                                    </div>
                            </div>
                        </template>
                        
                 
                </div>
            </div>
      
                 <form v-on:submit.prevent="submitForm">
                    <label for="chat" class="sr-only ">your message</label>
                        <div class="flex items-center p-4 rounded-large bg-gray-50 dark:bg-purple_main">
                 
                            <textarea v-model="body" id="chat" rows="1" class="block mx-2 p-4 w-full rounded-img dark:bg-transparent" placeholder="your message.."></textarea>
                            <button type="submit" class="inline-flex justify-center p-3 text-blue-600 rounded-img cursor-pointer hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-purple-900">

                                <svg class="w-8 h-8 rotate-90" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="white" viewBox="0 0 18 20">
                                    <path d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z"/>
                                </svg>
                                <span class="sr-only">send message</span>
                            </button>
                        </div>
                </form>
                    
            
            
        </div>
    </div>

</template>

<style>

ul{
    list-style: none;
    padding: 0;
    margin: 0;
}
</style>
<script>
import axios from 'axios'
import { useUserStore } from '@/stores/user'

export default {
    name: 'chat',

    setup() {
        const userStore = useUserStore()

        return {
            userStore
        }
    },

    data() {
        return{
            conversations: [],
            activeConversation: {},
            body: ''
        }
    },

    mounted(){
        this.getConversations()
    },

    methods: {
        setActiveConversation(id) {
            console.log('setActiveConversation', id)

            this.activeConversation = id
            this.getMessages()
        },
        getConversations(){
            console.log('getConversations')

            axios
                .get(`/api/chat/`)
                .then(response =>{
                    console.log(response.data)

                    this.conversations = response.data

                    if (this.conversations.length) {
                        this.activeConversation = this.conversations[0].id //show first in the list of conversations
                    }

                    this.getMessages()

                })
                .catch(error =>{
                    console.log(error)
                })
        },

        getMessages() {
            console.log('getMessages')

            axios
                .get(`api/chat/${this.activeConversation}/`)
                .then(response =>{
                    console.log(response.data)

                    this.activeConversation = response.data
                })
                .catch(error =>{
                    console.log(error)
                })

        },

        submitForm(){
            console.log('submitForm', this.body)

            axios
                .post(`api/chat/${this.activeConversation.id}/send/`, {
                    body: this.body
                })
                .then(response =>{
                    console.log(response.data)

                    this.activeConversation.messages.push(response.data)
                })
                .catch(error =>{
                    console.log(error)
                })
        }
    }

}
</script>