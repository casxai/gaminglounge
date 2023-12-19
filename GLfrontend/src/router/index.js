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
import connectView from '../views/connectView.vue'
import TournamentsView from '../views/TournamentsView.vue'
import MarketplaceView from '../views/MarketplaceView.vue'
import BetatestingView from '../views/BetatestingView.vue'
import EditProfileView from '../views/EditProfileView.vue'
import EditPasswordView from '../views/EditPasswordView.vue'
import NotificationsView from '../views/NotificationsView.vue'
import GamePopupView from '../views/GamePopupView.vue'
import VerificationView from '../views/VerificationView.vue'
import PopularGamesView from '../views/PopularGamesView.vue'
import PopupView from '../views/PopupView.vue'
import ChatTest from '../views/ChatTest.vue'

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
      component: connectView
    },
    {
      path: '/tournaments',
      name: 'tournaments',
      component: TournamentsView
    },
    {
      path: '/marketplace',
      name: 'marketplace',
      component: MarketplaceView
    },
    {
      path: '/betatesting',
      name: 'betatesting',
      component: BetatestingView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView
    },
    {
      path: '/chat',
      name: 'chat',
      component: ChatView
    },
    {
      path: '/verify',
      name: 'verify',
      component: VerificationView
    },
    {
      path: '/gametitle',
      name: 'gametitle',
      component: GamePopupView
    },
    {
      path: '/popup',
      name: 'popup',
      component: PopupView
    },
    {
      path: '/populargames/:id',
      name: 'PopularGamesView',
      component: PopularGamesView
    },
    {
      path: '/chattest',
      name: 'ChatTest',
      component: ChatTest
    },

    
  ]
})

export default router
