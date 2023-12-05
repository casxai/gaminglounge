<template>

    <div class="bg-[#120719] rounded-full p-4 border-2">
      
      <form 
        v-on:submit.prevent="submitForm"
            method="post">
                <h1 class="text-center font-semibold tracking-wider text-xl h-11">share your gaming thoughts</h1>
                <hr class="pb-4 border-t-2">

                <div class="grid grid-cols-2">

                  <div class="justify-self-start self-center">
                    <input checked id="checked-checkbox" type="checkbox" v-model="is_private" class="w-6 h-6 text-purple-600 bg-gray-100 border-purple-300 rounded focus:ring-gray-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-purple-200 dark:border-gray-600 "><label class="ms-2 font-medium text-purple-900 dark:text-purple-300">show to friends only</label></div>
              
                    <div class="space-x-2">
                    
                          <select v-model="menu" class="mb-2 p-2 bg-purple_main rounded-full  text-white">
                            <option value="" disabled>where to post</option>
                            <option v-for="choice in menuChoices">{{ choice }}</option>
                              </select>
                              <select v-model="game_title" class="mb-2 p-2  bg-purple_main rounded-full  text-align">
                              <option value="" disabled>pick your game topic</option>
                          <option v-for="title in gameTitles" :key="title.id" :value="title.id">{{ title.title }}</option>
                      </select>
                    </div>
                  
                </div>
                   
              
          
                 <textarea v-model="body" class="p-4 w-full bg-purple_main rounded-full" placeholder="let's talk gaming.."></textarea>
              <div  class="text-red-400 mb-2">
                <p v-if="gameTitleError">select a game before posting</p>
                <p v-if="contentError">please provide a description about your post.</p>
              </div>
              <div class="">
                    <div class="flex justify-between md:justify-between">
                      <label class="">
                            <input type="file" ref="file" @change="onFileChange">
                            <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 24 24"><g fill="none"><path stroke="#f9f9f9" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M22 12c0 5.523-4.477 10-10 10S2 17.523 2 12S6.477 2 12 2m7 0v3m0 3V5m0 0h3m-3 0h-3"/><path fill="#f9f9f9" fill-rule="evenodd" d="M6.978 6.488A2.674 2.674 0 0 1 8.5 6c.41 0 1.003.115 1.522.488c.57.41.978 1.086.978 2.012c0 .926-.408 1.601-.978 2.011A2.674 2.674 0 0 1 8.5 11c-.41 0-1.003-.115-1.522-.489C6.408 10.101 6 9.427 6 8.5c0-.926.408-1.601.978-2.012zm9.353 15.456C18.611 21.177 23 18.143 23 12a1 1 0 0 0-1-1h-1c-4.803 0-8.21 1.072-10.555 2.622c2.035.662 4.076 1.82 5.63 3.751a1 1 0 0 1-1.56 1.254c-1.515-1.884-3.65-2.912-5.796-3.41a15.464 15.464 0 0 0-3.531-.388c-.784.003-1.477.066-2.024.157a1.005 1.005 0 0 1-.232.012l-.096.016a1 1 0 0 0-.76 1.367c.652 1.584 2.135 3.723 4.51 5.097c2.42 1.399 5.684 1.958 9.745.466z" clip-rule="evenodd"/></g></svg>
                      </label>
                    
                    <button @click="close" class=""><svg xmlns="http://www.w3.org/2000/svg" width="45" height="40" viewBox="0 0 15 16"><path fill="#f9f9f9" d="M12.49 7.14L3.44 2.27c-.76-.41-1.64.3-1.4 1.13l1.24 4.34c.05.18.05.36 0 .54l-1.24 4.34c-.24.83.64 1.54 1.4 1.13l9.05-4.87a.98.98 0 0 0 0-1.72Z"/></svg></button>
                  </div>

                  <div class="grid text-center space-y-2 italic">
                    <div v-if="fileName">
                    {{ fileName }}
                    </div>
                    <img v-if="url" :src="url" class="md:object-contain justify-self-center object-contain h-60 w-96">
                  </div>
            </div>
               
         

                  
       
    </form>

  </div>
    
</template>

<script>
import axios from 'axios'
// profcheck
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'

export default {
  setup() { //profcheck
        const toastStore = useToastStore()
        const userStore = useUserStore()
        return {
            toastStore,
            userStore,

        }
    },
  props: {
    user: Object,
    posts: Array
  },
  data() {
    return {
      body: '',
      is_private: false,
      fileName: null,
      url: null,
      game_title: '',
      gameTitles: [],
      
      menuChoices: ['Discussions', 'Marketplace', 'Connect', 'Tournament', 'Beta Testing'],
      menu: '',
      gameTitleError: false, // Added error flag for game title validation
      contentError: false, // New error flag for post content
      // error: null, //profcheck
    }
  },

  mounted() {
    this.userStore.initStore();
    this.fetchGameTitles();
  },

  methods: {

    onFileChange(e) {
      const file = e.target.files[0];
      
      this.fileName = file.name;

      const reader = new FileReader();
      reader.onload = e => {
        this.url = e.target.result;  
      };
      
      reader.readAsDataURL(file); 
  
    },
    removeFile() {
      this.fileName = null;
      this.url = null; 
    },
    submitForm() {
      console.log('submitForm', this.body);
      this.gameTitleError = false;
      this.contentError = false;

      // Check if game title is selected
      if (!this.game_title) {
        this.gameTitleError = true;
      }

      // Check if body/content is provided
      if (!this.body.trim()) {
        this.contentError = true;
      }

      // Prevent form submission if either check fails
      if (this.gameTitleError || this.contentError) {
        return;
      }

      let formData = new FormData();
      formData.append('image', this.$refs.file.files[0]);
      formData.append('body', this.body);
      formData.append('is_private', this.is_private);
      formData.append('game_title', this.game_title);
      formData.append('menu', this.menu);

      axios
        .post('/api/posts/create/', formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          }
      })
        .then(response => {
        
        this.toastStore.showToast(5000, 'critical hit! your post landed cleanly thanks for sharing your wisdom with the community! ˚ʚ♡ɞ˚ ', 'bg-emerald-700') //profcheck

        this.posts.unshift(response.data);
        this.resetForm();
        if (this.user) {
          this.user.posts_count += 1;
        }
      })
        .catch(error =>{//profcheck
          if (error.response.status === 400) {//profcheck
          const message = error.response.data.error//profcheck

          this.toastStore.showToast(//profcheck
            5000,  //profcheck
            'easy there partner! our foul word sheriff caught some offensive language. rework your post and giddy up again.  ✧˖°. ',//profcheck
            'bg-red-400' //profcheck
          )//profcheck
        }//profcheck
    });
    },
    resetForm() {
            this.body = '';
            this.is_private = false;
            this.$refs.file.value = null;
            this.url = null;
            this.game_title = ''; // Reset to null instead of empty string
            this.menu = '';
        },
        async fetchGameTitles() {
            try {
                const response = await axios.get(`/api/posts/get_gametitle/`);
                this.gameTitles = response.data.sort((a, b) => a.title.localeCompare(b.title));
                console.log('Game Titles:', this.gameTitles);
            } catch (error) {
                console.error('Error fetching game titles:', error);
            }
          },
  }
}
</script>

<style>

</style>