<template>
<div class=" grid grid-cols-4 gap-4">

        <!-- left side 
        col-span-1: takes 1 of the 4 columns -->
        <div class="main-left md:col-span-1"> 
        </div>
    <!-- center -->
        <!-- col-span-2: takes 2 of the 4 columns
            space-y-4: 6 spaces each post -->
    <div class="md:px-4 main-center md:col-span-2 col-span-4 space-y-6">
        <!-- write something -->
        <!-- post area -->     
        <div class="p-4 bg-purple_main rounded-full"
                v-for="notification in notifications" 
                v-bind:key="notification.id"
                v-if="notifications.length"
            > <!-- loop ng notifications -->
                
                    <p class="notification">{{ notification.body }}

                    <button class="underline notification" @click="readNotification(notification)">
                        view
                    </button>
                    </p>    
               
 
        </div>

        <div class="p-6 bg-purple_main rounded-full notification"
                v-else
        >
            you don't have any unread notifications!
        </div> 
    
    </div>
    <div class="main-left md:col-span-1"> 
        </div>

</div> 

</template>
<style scoped>
@media (max-width: 768px) {
  .hide-on-mobile {
    display: none; /* Hide the logo on smaller screens */
  }
  .notification {
    font-size: 14px;
  }
}
</style>
<script>
import axios from 'axios'

export default{
    name: 'notifications', 
    
    components: {
 

    },
    data(){
        return {
            notifications: []
        }
    },

    mounted(){
        this.getNotifications()
    },
    methods: {
        getNotifications() 
        {
            axios
                .get('api/notifications/')
                .then(response => {
                    console.log(response.data)
                    this.notifications = response.data
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
        },

        async readNotification(notification){
            console.log('readNotification', notification.id)

            await axios
                .post(`/api/notifications/read/${notification.id}/`)
                .then(response => {
                    console.log(response.data)

                    if (notification.type_of_notification == 'post_like' || notification.type_of_notification == 'post_comment') {
                        //redirect user to post page
                        this.$router.push({name: 'postview', params: {id: notification.post_id}})
                    }
                    else{
                        //redirect to friends page
                        this.$router.push({name: 'friends', params: {id: notification.created_for_id}})
                    }
                })
                .catch(error => {
                    console.log('Error: ', error)
                })
    
        }
    },
}
</script>