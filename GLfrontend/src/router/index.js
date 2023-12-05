import { createRouter, createWebHistory } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import SignupView from '../views/SignupView.vue'
import LoginView from '../views/LoginView.vue'
import FeedView from '../views/FeedView.vue'
import ProfileView from '../views/ProfileView.vue'
import SearchView from '../views/SearchView.vue'
import FriendsView from '../views/FriendsView.vue'
import PostView from '../views/PostView.vue'
import ChatView from '../views/ChatView.vue'
import EditProfileView from '../views/EditProfileView.vue'
import EditPasswordView from '../views/EditPasswordView.vue'
import NotificationsView from '../views/NotificationsView.vue'
import GamePopupView from '../views/GamePopupView.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // {
    //   path: '/',
    //   name: 'home',
    //   component: HomeView
    // },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/feed',
      name: 'feed',
      component: FeedView
    },

    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/notifications',
      name: 'notifications',
      component: NotificationsView
    },

    {
      path: '/profile/edit',
      name: 'editprofile',
      component: EditProfileView
    },    
    {
      path: '/profile/edit/password',
      name: 'editpassword',
      component: EditPasswordView
    },
    {
      path: '/profile/:id',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/:id',
      name: 'postview',
      component: PostView
    },
    {
      path: '/profile/:id/friends',
      name: 'friends',
      component: FriendsView
    },


    {
      path: '/connect',
      name: 'connect',
      component: () => import('../views/connectView.vue')
    },
    {
      path: '/tournaments',
      name: 'tournaments',
      component: () => import('../views/TournamentsView.vue')
    },
    {
      path: '/marketplace',
      name: 'marketplace',
      component: () => import('../views/MarketplaceView.vue')
    },
    {
      path: '/betatesting',
      name: 'betatesting',
      component: () => import('../views/BetatestingView.vue')
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('../views/SearchView.vue')
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('../views/ChatView.vue')
    },
    {
      path: '/verify',
      name: 'verify',
      component: () => import('../views/VerificationView.vue')
    },
    {
      path: '/gametitle',
      name: 'gametitle',
      component: () => import('../views/GamePopupView.vue')
    },
    {
      path: '/popup',
      name: 'popup',
      component: () => import('../views/PopupView.vue')
    },


    
  ]
})

export default router
