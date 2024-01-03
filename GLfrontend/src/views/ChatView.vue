<template>
  <div class="max-w-screen-2xl mx-auto grid grid-cols-3 gap-6 pt-4">
    <!-- inbox -->
    <div v-if="activeConversation" class="main-left col-span-1 flex flex-col bg-purple_main rounded-full overflow-auto h-134 py-4 border-2 border-gray-400">
      <label class="rounded-full font-semibold text-xl tracking-wide pl-7 mb-3">inbox</label>
      <a
        class="flex items-center justify-between border-gray-200 hover:bg-[#120719] rounded-full text-left"
        v-for="conversation in conversations"
        v-bind:key="conversation.id"
        v-on:click="setActiveConversation(conversation.id)"
      >
          <div class="justify-self-start flex flex-col-2 items-center my-3 px-6">
                <div v-for="user in conversation.users" v-bind:key="user.id" class="">
                  <div
                      class="flex flex-row items-center"
                      v-if="user.id !== userStore.user.id"
                  >
                      <img
                          :src="user.get_avatar"
                          class="h-12 w-12 rounded-img object-cover"
                      />
                      <p class="font-semibold text-base">{{user.name}}</p>
                  </div>
              </div>
            </div>
        <span class="text-xs text-gray-400 font-light pr-6">{{ conversation.modified_at_formatted }}</span>
      </a>
    </div>
    <!-- messages -->
    <div class="main-center col-span-2 space-y-4">
      <div class="bg-purple_main rounded-full border-2 border-gray-400">
        <div
          class="flex flex-col h-128 p-6 overflow-hidden hover:overflow-y-auto"
        >
          <template
            v-for="message in activeConversation.messages"
            v-bind:key="message.id" 
          >
            <!-- message sent -->
            <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end" v-if="message.created_by.id == userStore.user.id"> 
                <div class="message-sent">
                  <div class="bg-[#120719] text-white p-3 rounded-l-full rounded-br-full">
                    <p>{{ message.body }}</p>
                  </div>
                  <span class="text-xs text-gray-400 font-light leading-none">
                    {{ message.created_at_formatted }} ago </span>
                </div>
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                  <img
                    :src="message.created_by.get_avatar"
                    class="w-[40px] rounded-full"
                  />
                </div>
            </div>
            <!-- message received -->
            <div class="flex w-full mt-2 space-x-3 max-w-md" v-else>
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                  <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full"/>
                </div>
                <div>
                  <div class="bg-[#120719] p-3 rounded-r-full rounded-bl-full">
                    <p>{{ message.body }}</p>
                  </div>
                    <span class="text-xs text-gray-400 font-light leading-none">{{ message.created_at_formatted }} ago</span>
                </div>
            </div>

          </template>
        </div>
      </div>

      <form v-on:submit.prevent="submitForm">
        <!-- <label for="chat" class="sr-only ">your message</label> -->
        <div
          class="flex items-center p-4 rounded-full bg-gray-50 dark:bg-purple_main border-2 border-gray-400"
        >
          <input
            class="form-control block mx-2 p-4 w-full rounded-img dark:bg-transparent"
            v-model="body"
            id="chat"
            placeholder="write a message"
          />
  
          <button
            type="submit"
            class="inline-flex justify-center p-3 text-blue-600 rounded-img cursor-pointer hover:bg-blue-100 dark:text-blue-500 dark:hover:bg-purple-900"
          >
            <svg
              class="w-8 h-8 rotate-90"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="white"
              viewBox="0 0 18 20"
            >
              <path
                d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z"
              />
            </svg>
            <span class="sr-only">send message</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<style>
ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
</style>
<!-- <script>
// import {ref} from 'vue';
// import Pusher from 'pusher-js';
import axios from "axios";
import { useUserStore } from "@/stores/user";

export default {
  name: "chat",

  setup() {
    // const username = ref('username')
    // const messages = ref([])
    // const message = ref('')
    const userStore = useUserStore();

    return {
      // username,
      // messages,
      // message,
      userStore,
    };
  },

  data() {
    return {
      conversations: [],
      activeConversation: {},
      body: "",
    };
  },

  mounted() {
    this.getConversations(); // Consider calling this function if required
  },

  methods: {
    setActiveConversation(id) {
      console.log("setActiveConversation", id);

      this.activeConversation = id;
      this.getMessages();
    },
    getConversations() {
      console.log("getConversations");

      axios
        .get(`/api/chat/`)
        .then((response) => {
          console.log(response.data);

          this.conversations = response.data;

          if (this.conversations.length) {
            this.activeConversation = this.conversations[0].id; //show first in the list of conversations
          }

          this.getMessages();
        })
        .catch((error) => {
          console.log(error);
        });
    },

    getMessages() {
      console.log("getMessages");

      axios
        .get(`api/chat/${this.activeConversation}/`)
        .then((response) => {
          console.log(response.data);

          this.activeConversation = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },

    submitForm() {
      console.log("submitForm", this.body);

      axios
        .post(`api/chat/${this.activeConversation.id}/send/`, {
          body: this.body,
        })
        .then((response) => {
          console.log(response.data);

          // Add the message received from the response to the messages array
          this.activeConversation.messages.push(response.data);

          this.body = "";
        })
        .catch((error) => {
          console.log(error);
        });
    },
  },
};
</script> -->

<script>

import axios from 'axios';
import { ref, onMounted, watch } from 'vue';
import { useUserStore } from '@/stores/user';
import { pusher } from '@/stores/pusher';

export default {
    name: 'Chat',

    setup() {
        const userStore = useUserStore();
        const conversations = ref([]); //users 
        const activeConversation = ref({}); //current room
        const body = ref('');
        
        let channel = null;

        const initializePusher = () => {
          if (channel) {return;}
          channel = pusher.subscribe(`conversation_${activeConversation.value.id}`);
          channel.bind('new-message', (data) => {
         // activeConversation.messages.push(JSON.stringify(data));
            activeConversation.value.messages.push(JSON.stringify(data));
            });
          };

        // get the list of conversations
        const getConversations = () => {
          axios
            .get(`/api/chat/`) 
            .then((response) => {
                conversations.value = response.data;
                if (conversations.value.length) {
                  setActiveConversation(conversations.value[0].id); //show first in the list of conversations
                }
              })
            .catch((error) => {
                console.log(error);
              });
          };

        // set active
        const setActiveConversation = (id) => {
            // console.log("Before setActiveConversation:", activeConversation.value); 
            activeConversation.value = id;
            // console.log("After setActiveConversation:", activeConversation.value);
            getMessages();
          };

        // get messages for a specific conversation
        const getMessages = () => { // console.log(activeConversation.value)

          const conversationId = typeof activeConversation.value === 'object' ? activeConversation.value.id : activeConversation.value;

          if (!conversationId) { return false; }
          axios
            .get(`api/chat/${conversationId}/`) 
            .then((response) => {
              console.log(response.data)
                activeConversation.value = response.data;   
              })
            .catch((error) => {
                console.log(error);
              });
          };
        
        // submit message
        const submitForm = () => {
          axios
            .post(`api/chat/${activeConversation.value.id}/send/`, {
                body: body.value,
              })
            .then((response) => {
                activeConversation.value.messages.push(response.data);
                body.value = '';
              })
            .catch((error) => {
                console.log(error);
              });
          };
        
        
        // on mounted
        onMounted(() => {
            getConversations();
            initializePusher();
          });
        
        // watch function
        // watch(activeConversation, () => {
        //     if (pusher.value) {
        //       pusher.value.unbind(); 
        //       pusher.value.unsubscribe();
        //       }
        //     initializePusher();
        //     getMessages();
        //   });

    return {
        userStore,
        conversations,
        activeConversation,
        body,
        setActiveConversation,
        submitForm,
      };
    },
  };
</script>
