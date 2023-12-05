<template>
    <!-- comment-->
    <div class="mb-2 flex items-center justify-between">
        <!-- username nd pfp -->
            <div class="flex items-center space-x-3">
                <img 
                data-te-lazy-load-init
				:src="comment.created_by.get_avatar" alt="logo"
				data-te-lazy-placeholder="https://place-hold.it/1321x583?text=Loading"
                class="w-[40px] rounded-img">
                    
                        <RouterLink class="font-medium text-base" :to="{name: 'profile', params:{'id': comment.created_by.id}}">{{ comment.created_by.name }}</RouterLink>
                   
            </div>
                    <!-- time posted -->
                    <p class="text-gray-400 text-xs font-light">{{ comment.created_at_formatted}}</p> 
    </div>

    <p class="text-base/7 font-light">{{ comment.body }}</p>
 
</template>

<script>
import { RouterLink } from 'vue-router'

export default{
    props: {
        comment: Object
    },
    components: { RouterLink }
}
</script>