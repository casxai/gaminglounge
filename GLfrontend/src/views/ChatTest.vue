<template>
<!-- component -->
<!-- This is an example component -->
<div class="container mx-auto shadow-lg rounded-lg">
    <!-- Chatting -->
    <div class="flex flex-row justify-between">
      <!-- left panel -->
      <div class="flex flex-col w-2/5 border-r-2 overflow-y-auto">
        <div
          class="flex flex-row py-4 px-2 justify-center items-center border-b-2"
        >
          <div class="w-1/4">
            <img
              src="https://source.unsplash.com/_7LbC5J-jw4/600x600"
              class="object-cover h-12 w-12 rounded-img"
              alt=""
            />
          </div>
            <input class="ml-2 text-base w-full font-semibold bg-transparent"/>
            <!-- <div class="text-base w-full font-semibold">Luis1994</div> -->
     
            <span class="text-xs text-gray-400 mr-6">1hour</span>
        </div>
      </div>
    
      <!-- message main panel-->
      <div class="w-full px-5 flex flex-col justify-between">
        <div class="flex flex-col mt-5"
        
        >
        <!-- starting message me -->
          <div class="flex justify-end mb-4" >
            <div
              class="mr-2 py-3 px-4 bg-blue-400 rounded-bl-3xl rounded-br-3xl rounded-tl-3xl text-white"
            >
        
            </div>
            <img
              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
              class="object-cover h-12 w-12 rounded-img"
              alt=""
            />
          </div>
        <!-- end message me -->
        <!-- starting message you -->
          <div class="flex justify-start mb-4">
            <img
              src="https://source.unsplash.com/vpOeXr5wmR4/600x600"
              class="object-cover h-12 w-12 rounded-img"
              alt=""
            />
            <div
              class="ml-2 py-3 px-4 bg-gray-400 rounded-br-3xl rounded-tr-3xl rounded-bl-3xl text-white"
            >
     
            </div>
          </div>
          <!-- end message you -->
        </div>
        <!-- end whole message -->
        <!-- input message -->
        <form @submit.prevent="">
            <div class="flex items-center py-5">
                <label for="chat" class="sr-only ">your message</label>
                <input
                class="form-control w-full bg-transparent border-2 border-gray-400 py-5 px-3 rounded-img"
                 id="chat" placeholder="write a message"/>
                <button type="submit"
                        class="inline-flex justify-center p-3 text-blue-600 rounded-img cursor-pointer hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-purple-900">

                    <svg class="w-8 h-8 rotate-90" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="white"
                            viewBox="0 0 18 20">
                        <path
                            d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z" />
                    </svg>
                    <span class="sr-only">send message</span>
                </button>
            </div>
        </form>
        
        <!-- input end message -->
      </div>
      <!-- end message -->
      </div>
      
    </div>

</template>

<!-- <script>
// import {ref} from 'vue';
// import Pusher from 'pusher-js';
import axios from 'axios';
import { useUserStore } from '@/stores/user';

export default {
    name: 'chat',

    setup() {
        // const username = ref('username')
        // const messages = ref([])
        // const message = ref('')
        const userStore = useUserStore()

        return {
            // username,
            // messages,
            // message,
            userStore
        }
    },

    data() {
        return {
            conversations: [],
            activeConversation: {},
            body: ''
        }
    },

    mounted() {
    this.getConversations() // Consider calling this function if required

},



    methods: {
        setActiveConversation(id) {
            console.log('setActiveConversation', id)

            this.activeConversation = id
            this.getMessages()
        },
        getConversations() {
            console.log('getConversations')

            axios
                .get(`/api/chat/`)
                .then(response => {
                    console.log(response.data)

                    this.conversations = response.data

                    if (this.conversations.length) {
                        this.activeConversation = this.conversations[0].id //show first in the list of conversations
                    }

                    this.getMessages()

                })
                .catch(error => {
                    console.log(error)
                })
        },

        getMessages() {
            console.log('getMessages')

            axios
                .get(`api/chat/${this.activeConversation}/`)
                .then(response => {
                    console.log(response.data)

                    this.activeConversation = response.data
                })
                .catch(error => {
                    console.log(error)
                })

        },

        submitForm() {
            console.log('submitForm', this.body);

            axios.post(`api/chat/${this.activeConversation.id}/send/`, {
                body: this.body
            })
                .then(response => {
                    console.log(response.data);

                    // Add the message received from the response to the messages array
                    this.activeConversation.messages.push(response.data);

                    this.body = '';
                })
                .catch(error => {
                    console.log(error);
                });
        }
    }

}
</script> -->