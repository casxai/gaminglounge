<template>
		<nav style="
		background-size:cover;" 
		class="py-6 sticky z-20 bg-[url('https://api.gaminglounge.online/static/admin/img/header.png')] top-0" v-if="userStore.user.isAuthenticated && userStore.user.id"> 
		<!-- mobile view -->
			<div
				v-if="showMobileNav"
				class="fixed inset-0 w-full pt-6 z-20 bg-[#29172D] md:hidden" 
				>
				<div class="flex flex-col p-4 h-fit">
					<RouterLink @click="toggleNav" to="/feed" class="hover:text-violet1 p-2 dark:hover:text-violet1 dark:text-white dark:hover:text-violet1 dark:hover:text-violet1 dark:hover:bg-transparent">discussions </RouterLink>  
					<RouterLink @click="toggleNav" to="/marketplace" class="hover:text-violet1 p-2 dark:hover:text-violet1 dark:text-white dark:hover:text-violet1 dark:hover:text-violet1 dark:hover:bg-transparent">marketplace</RouterLink>
					<RouterLink @click="toggleNav" to="/connect" class="hover:text-violet1 p-2 dark:hover:text-violet1 dark:text-white dark:hover:text-violet1 dark:hover:text-violet1 dark:hover:bg-transparent">connect</RouterLink>
					<RouterLink @click="toggleNav" to="/tournaments" class="hover:text-violet1 p-2 dark:hover:text-violet1 dark:text-white dark:hover:text-violet1 dark:hover:text-violet1 dark:hover:bg-transparent">tournaments</RouterLink>
					<RouterLink @click="toggleNav" to="/betatesting" class="hover:text-violet1 p-2 dark:hover:text-violet1 dark:text-white dark:hover:text-violet1 dark:hover:text-violet1 dark:hover:bg-transparent">beta testing</RouterLink>
				
				</div>
			</div> 
		<!-- end mobile view -->
			<div 
				:class="{ hidden: showMobileNav }"
				class="w-[92%] mx-auto md:flex items-center flex-wrap justify-between">
				<!-- left menu logo start -->		
					<a href="https://gaminglounge.online/feed" class="flex items-center">			
					 	<img src="/assets/img/logo/gl_logo.png" alt="logo" class="object-none w-25 pr-16 hide-on-mobile"/>	
					</a>

					<!-- div class="justify-between w-full md:flex md:w-auto" id="navbar-use" -->
					<div class="justify-between hidden md:flex " id="navbar-use">
						<ul class="flex items-center font-semibold tracking-wider md:tracking-wider p-4 md:p-0 mt-4 rounded-lg md:flex-row md:space-x-8 md:mt-0">
							<li>
								<RouterLink to="/feed" class="block py-2 pl-3 md:hover:text-violet1 md:p-0 md:dark:hover:text-violet1 dark:text-white dark:hover:text-violet1 dark:hover:text-violet1 md:dark:hover:bg-transparent" >discussions </RouterLink>   
							</li>
							<li>
								<RouterLink to="/marketplace" class="block py-2 pl-3 md:hover:text-violet1 md:p-0 md:dark:hover:text-violet1 dark:text-white dark:hover:text-violet1 dark:hover:text-violet1 md:dark:hover:bg-transparent" >marketplace </RouterLink>
							</li>
							<li>
								<RouterLink to="/connect" class="block py-2 pl-3 md:hover:text-violet1 md:p-0 md:dark:hover:text-violet1 dark:text-white dark:hover:text-violet1 dark:hover:text-violet1 md:dark:hover:bg-transparent " >connect</RouterLink>
							</li>
							<li>
								<RouterLink to="/tournaments" class= "block py-2 pl-3 md:hover:text-violet1 md:p-0 md:dark:hover:text-violet1 dark:text-white dark:hover:text-violet1 dark:hover:text-violet1 md:dark:hover:bg-transparent" >tournaments </RouterLink>
							</li>
							<li>
								<RouterLink to="/betatesting" class="block py-2 pl-3 md:hover:text-violet1 md:p-0 md:dark:hover:text-violet1 dark:text-white dark:hover:text-violet1 dark:hover:text-violet1 md:dark:hover:bg-transparent">beta testing </RouterLink>
							</li>
						</ul>
					</div> 
				<!-- center menu start -->
					<div class="items-center justify-between flex md:w-auto md:order-1 rtl:space-x-reverse">
										
									<div class="flex md:hidden">
										<button @click="toggleNav">
											<svg height="38px" id="Layer_1" fill="#f9f9f9" style="enable-background:new 0 0 32 32;" version="1.1" viewBox="0 0 32 32" width="38px" xml:space="preserve" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><path d="M4,10h24c1.104,0,2-0.896,2-2s-0.896-2-2-2H4C2.896,6,2,6.896,2,8S2.896,10,4,10z M28,14H4c-1.104,0-2,0.896-2,2  s0.896,2,2,2h24c1.104,0,2-0.896,2-2S29.104,14,28,14z M28,22H4c-1.104,0-2,0.896-2,2s0.896,2,2,2h24c1.104,0,2-0.896,2-2  S29.104,22,28,22z"/></svg>
										</button>
									</div>
									<div class="flex">
										<RouterLink to="/search" class="p-2 rounded-img hover:bg-gray-600">
											<svg xmlns="http://www.w3.org/2000/svg" width="38" height="38" viewBox="0 0 24 24"><g fill="none" stroke="#f9f9f9" stroke-width="2"><circle cx="11" cy="11" r="7"/><path stroke-linecap="round" d="M11 8a3 3 0 0 0-3 3m12 9l-3-3"/></g></svg>
										</RouterLink>	
										<RouterLink to="/notifications" class="p-2 rounded-img hover:bg-gray-600">
											<svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 24 24"><g fill="none"><path d="M24 0v24H0V0zM12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035c-.01-.004-.019-.001-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427c-.002-.01-.009-.017-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093c.012.004.023 0 .029-.008l.004-.014l-.034-.614c-.003-.012-.01-.02-.02-.022m-.715.002a.023.023 0 0 0-.027.006l-.006.014l-.034.614c0 .012.007.02.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01l-.184-.092"/><path fill="#f9f9f9" d="M15 19a2 2 0 0 1-1.85 1.995L13 21h-2a2 2 0 0 1-1.995-1.85L9 19zM12 2a7 7 0 0 1 6.996 6.76L19 9v3.764l1.822 3.644a1.1 1.1 0 0 1-.869 1.586l-.115.006H4.162a1.1 1.1 0 0 1-1.03-1.487l.046-.105L5 12.764V9a7 7 0 0 1 7-7"/></g></svg>               
										</RouterLink>								
										<RouterLink to="/chat" class="p-2 rounded-img hover:bg-gray-600">
											<svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 24 24"><g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"><path d="M0 0h24v24H0z"/><path fill="#f9f9f9" d="M22 7.535V17a3 3 0 0 1-2.824 2.995L19 20H5a3 3 0 0 1-2.995-2.824L2 17V7.535l9.445 6.297l.116.066a1 1 0 0 0 .878 0l.116-.066z"/><path fill="#f9f9f9" d="M19 4c1.08 0 2.027.57 2.555 1.427L12 11.797l-9.555-6.37a2.999 2.999 0 0 1 2.354-1.42L5 4z"/></g></svg>
										</RouterLink>									     
							
										<RouterLink :to="{name: 'profile', params:{'id': userStore.user.id}}" class="p-2 rounded-img hover:bg-gray-600" >
												<!-- <img :src="userStore.user.avatar" alt="user.profile"					
												class="w-10 h-10 rounded-img  hover:opacity-80"> -->
											<svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 24 24"><g fill="none"><path d="M24 0v24H0V0zM12.593 23.258l-.011.002l-.071.035l-.02.004l-.014-.004l-.071-.035c-.01-.004-.019-.001-.024.005l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427c-.002-.01-.009-.017-.017-.018m.265-.113l-.013.002l-.185.093l-.01.01l-.003.011l.018.43l.005.012l.008.007l.201.093c.012.004.023 0 .029-.008l.004-.014l-.034-.614c-.003-.012-.01-.02-.02-.022m-.715.002a.023.023 0 0 0-.027.006l-.006.014l-.034.614c0 .012.007.02.017.024l.015-.002l.201-.093l.01-.008l.004-.011l.017-.43l-.003-.012l-.01-.01l-.184-.092"/><path fill="#f9f9f9" d="M12 13c2.396 0 4.575.694 6.178 1.672c.8.488 1.484 1.064 1.978 1.69c.486.615.844 1.351.844 2.138c0 .845-.411 1.511-1.003 1.986c-.56.45-1.299.748-2.084.956c-1.578.417-3.684.558-5.913.558s-4.335-.14-5.913-.558c-.785-.208-1.524-.506-2.084-.956C3.41 20.01 3 19.345 3 18.5c0-.787.358-1.523.844-2.139c.494-.625 1.177-1.2 1.978-1.69C7.425 13.695 9.605 13 12 13m0-11a5 5 0 1 1 0 10a5 5 0 0 1 0-10"/></g></svg>
										</RouterLink> 	
									</div>
								
					</div>  
			</div>
		</nav>
	<!-- header end -->
	<!-- main view-->
	<Toast /> <!--  shows the alert sa frontend -->
		<main class="pt-6 w-[92%] mx-auto"> 
			<RouterView /> 
		</main>
		<Toast /> <!--  shows the alert sa frontend -->
	
	
	
</template> 
<style scoped>
@media (max-width: 768px) {
  .hide-on-mobile {
    display: none; /* Hide the logo on smaller screens */
  }
}
</style>
<script>

	import axios from 'axios'
    import Toast from '@/components/Toast.vue'
    import { useUserStore } from '@/stores/user'
	// const isModalActive = ref(null)
	// const Profile = defineAsyncComponent();

import { RouterLink } from 'vue-router'

    export default {
		data() {
			return {
				showMobileNav: false
			}
		},
        setup() {
            const userStore = useUserStore()
		

            return {
                userStore,
				
            }
        },
		watch: {
			$route(to, from) {
			this.showMobileNav = false;
			}
		},
		methods:{
			toggleNav() {
				this.showMobileNav = !this.showMobileNav
			},
		},

        components: {
			Toast,
			RouterLink,
			
		},

        beforeCreate() {
            this.userStore.initStore()

            const token = this.userStore.user.access

            if (token) {
                axios.defaults.headers.common["Authorization"] = "Bearer " + token;
            } else {
                axios.defaults.headers.common["Authorization"] = "";
            }
        }
    }
</script>

