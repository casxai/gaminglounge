<template>
  <!-- scroll: h-full overflow-y-scroll -->
  <div class="grid grid-cols-3 md:gap-6">
    <!-- inbox -->
    <div
      class="main-left md:col-span-1 flex flex-col bg-purple_main rounded-full overflow-auto h-134 py-4 border-2 border-gray-400"
    >
      <label
        for=""
        class="rounded-full font-semibold hide-on-mobile text-xl tracking-wide pl-7 mb-3"
        >Messages</label
      >

      <a
        class="flex items-center md:justify-between border-gray-200 hover:bg-[#120719] rounded-full md:text-left"
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
                class=" h-12 w-12 rounded-img aspect-square object-cover"
              />
              <p class="hide-on-mobile font-semibold text-base pl-3">{{ user.name }}</p>
            </div>
          </div>
        </div>

        <span class="text-xs text-gray-400 font-light pr-6 hide-on-mobile">{{
          conversation.modified_at_formatted
        }}</span>
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
            <div
              class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
              v-if="message.created_by.id == userStore.user.id"
            >
              <div>
                <div
                  class="bg-[#120719] text-white p-3 rounded-l-full rounded-br-full"
                >
                  <p class="sub">{{ message.body }}</p>
                </div>
                <span class="text-xs text-gray-400 font-light leading-none">
                  {{ message.created_at_formatted }} ago</span
                >
              </div>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img
                  :src="message.created_by.get_avatar"
                  class="w-[40px] rounded-full object-cover aspect-square"
                />
              </div>
            </div>

            <div class="flex w-full mt-2 space-x-3 max-w-md" v-else>
              <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                <img
                  :src="message.created_by.get_avatar"
                  class="w-[40px] rounded-full object-cover aspect-square"
                />
              </div>
              <div>
                <div class="bg-[#4B2E75] p-3 rounded-r-full rounded-bl-full">
                  <p class="sub">{{ message.body }}</p>
                </div>
                <span class="text-xs text-gray-400 font-light leading-none"
                  >{{ message.created_at_formatted }} ago</span
                >
              </div>
            </div>
          </template>
        </div>
      </div>

      <form v-on:submit.prevent="submitForm">
        <!-- <label for="chat" class="sr-only ">your message</label> -->
        <div
          class="flex items-center p-4 rounded-full bg-gray-50 dark:bg-purple_main bg-purple_main border-2 border-gray-400"
        >
          <input
            class="form-control block mx-2 p-4 w-full rounded-img bg-transparent dark:bg-transparent"
            v-model="body"
            id="chat"
            placeholder="write a message"
          />
          <!-- <textarea v-model="body" id="chat" rows="1"
                        class="block mx-2 p-4 w-full rounded-img dark:bg-transparent"
                        placeholder="your message.."></textarea> -->
          <button
            type="submit"
            class="inline-flex justify-center p-3 text-blue-600 rounded-img cursor-pointer hover:bg-blue-100 text-blue-500 dark:text-blue-500 dark:hover:bg-purple-900 hover:bg-purple-900"
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

<style scoped>
ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
@media (max-width: 768px) {
  .hide-on-mobile {
    display: none; /* Hide the logo on smaller screens */
  }
  .convoimg{
    
    display: flex;
    
  }
  .username {
    font-size: 16px;
    justify-self: start;
    display: flex;
  }
  .main {
    font-size: 16px;
  }
  .sub {
    font-size: 14px;
  }

}
</style>
<script>
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
</script>
<!-- <script>
import axios from 'axios';
import { ref, onMounted, watch } from 'vue';
import Pusher from 'pusher-js';
import { useUserStore } from '@/stores/user';

export default {
    name: 'Chat',

    setup() {
        const userStore = useUserStore();
        const conversations = ref([]);
        // const activeConversation = ref({});
        const activeConversation = ref({}); // Initialize as null
        const body = ref('');
        const message = ref('');
        const pusherChannel = ref(null);

        const setActiveConversation = (id) => {
            activeConversation.value = id;
            getMessages();
        };

        const getConversations = () => {
            axios
                .get(`/api/chat/`)
                .then((response) => {
                    conversations.value = response.data;

                if (conversations.value.length) {
                    // activeConversation.value = conversations.value[0].id;
                    setActiveConversation(conversations.value[0].id);
                }
                // getMessages();
            })
                .catch((error) => {
                    console.log(error);
            });
    };

        const getMessages = () => {
            if (!activeConversation.value) // Ensure activeConversation is valid before fetching messages
            return;
            axios
                .get(`api/chat/${activeConversation.value}/`)
                .then((response) => {
                    activeConversation.value = response.data;
                })
                .catch((error) => {
                    console.log(error);
                });
    };

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

        onMounted(() => {
            getConversations();
            initializePusher();
    });

        watch(activeConversation, () => {
            if (pusherChannel.value) {
            pusherChannel.value.unbind(); // Unbind previous channel events
            pusherChannel.value.unsubscribe(); // Unsubscribe from previous channel
            }
            initializePusher();
            getMessages();
        });

        const initializePusher = () => {
            if (activeConversation.value && activeConversation.value.id) {
                Pusher.logToConsole = true;
                const pusher = new Pusher('122926f4663427b23929', {
                    cluster: 'ap1',
                });

                pusherChannel.value = pusher.subscribe(
                    `conversation_${activeConversation.value}`
                );

                pusherChannel.value.bind('new_message', (data) => {
                    activeConversation.value.messages.push(data);
                });
            }
        };
    return {
        userStore,
        conversations,
        activeConversation,
        body,
        message,
        setActiveConversation,
        submitForm,
    };
  },
};
</script> -->
