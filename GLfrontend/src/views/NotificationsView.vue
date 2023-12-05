<template>
<div class="max-w-screen mx-auto grid grid-cols-4 gap-4 pt-4">

        <!-- left side 
        col-span-1: takes 1 of the 4 columns -->
        <div class="main-left col-span-1 space-y-6"> 
        </div>
    <!-- center -->
        <!-- col-span-2: takes 2 of the 4 columns
            space-y-4: 6 spaces each post -->
    <div class="px-4 main-center col-span-2 space-y-6">
        <!-- write something -->
        <!-- post area -->     
        <div class="p-4 bg-purple_main rounded-full"
                v-for="notification in notifications" 
                v-bind:key="notification.id"
                v-if="notifications.length"
            > <!-- loop ng notifications -->
            
                {{ notification.body }}

                <button class="underline" @click="readNotification(notification)">
                        read more
                    </button>
        </div>

        <div class="p-6 bg-purple_main rounded-full"
                v-else
        >
            you don't have any unread notifications!
        </div> 
    
    </div>

</div> 

</template>

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