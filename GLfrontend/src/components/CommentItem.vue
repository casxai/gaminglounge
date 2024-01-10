<template>
    <!-- comment -->
    <div class="mb-2 flex items-center justify-between">
        <!-- username and profile picture -->
        <div class="flex items-center space-x-3">
            <img data-te-lazy-load-init :src="comment.created_by.get_avatar" alt="logo"
                data-te-lazy-placeholder="https://place-hold.it/1321x583?text=Loading" class="w-[40px] rounded-img aspect-square">
            <RouterLink class="font-medium text-base" :to="{ name: 'profile', params: { 'id': comment.created_by.id } }">{{
                comment.created_by.name }}</RouterLink>
        </div>
        <p class="text-gray-400 text-xs font-light">{{ comment.created_at_formatted }}</p>

        <!-- Three dots icon -->
        <div @click="toggleExtraModal" class="cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor"
                width=30>
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z">
                </path>
            </svg>
        </div>
    </div>
    <p class="text-base/7 font-light">{{ comment.body }}</p>
    <!-- Extra modal with delete button -->
    <div v-if="showExtraModal">
        <button @click="deleteComment(comment.id)" class="flex mt-2 space-x-6 items-center">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"
                class="w-6 h-6 text-red-500">
                <path stroke-linecap="round" stroke-linejoin="round"
                    d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
            </svg>
            <span class="text-red-500 text-xs">delete comment</span>
        </button>
    </div>
</template>

<script>
import axios from 'axios'
import { RouterLink } from 'vue-router'

export default {

    emits: ['commentDeleted'],

    props: {
        comment: Object,
        postId: String,
    },

    components: { RouterLink },
    data() {
        return {
            showExtraModal: false,
            post: {
                comments: [], // Initialize with an empty array
            },
        }
    },
    methods: {
        deleteComment(commentId) {
            axios
                .delete(`/api/posts/delete_comment/${this.postId}/${commentId}/`)
                .then(response => {
                    this.$emit('commentDeleted', commentId);
                    // Update the client-side state
                    this.post.comments = this.post.comments.filter(comment => comment.id !== commentId);
                })
                .catch(error => {
                    console.error('Error deleting comment:', error);
                });
        },
        toggleExtraModal() {
            this.showExtraModal = !this.showExtraModal;
        },
    },
}
</script>