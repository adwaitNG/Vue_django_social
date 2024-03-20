import { createRouter, createWebHistory } from "vue-router";
import FeedView from "../views/FeedView.vue";
import HomeView from "../views/HomeView.vue";
import SignupView from "../views/SignupView.vue";
import LoginView from "../views/LoginView.vue";
import SearchView from "../views/SearchView.vue";
import ProfileView from "../views/ProfileView.vue";
import FriendsView from "../views/FriendsView.vue";
import PostDetailView from "../views/PostDetailView.vue";
import ChatView from "@/views/ChatView.vue";
import TrendView from "@/views/TrendView.vue";
import EditProfile from "@/views/EditProfile.vue";
import EditPassword from "@/views/EditPasswordView.vue";
import NotificationView from "@/views/NotificationsView.vue"

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "home",
            component: HomeView,
        },
        {
            path: "/feed",
            name: "feed",
            component: FeedView,
        },
        {
            path: "/trend/:id",
            name: "TrendView",
            component: TrendView,
        },
        {
            path: "/search",
            name: "search",
            component: SearchView,
        },
        {
            path: "/signup",
            name: "signup",
            component: SignupView,
        },
        {
            path: "/login",
            name: "login",
            component: LoginView,
        },
        { 
            path: "/profile/:id", 
            name: "profile", 
            component: ProfileView 
        },
        {
            path:"/notifications",
            name:"notifications",
            component: NotificationView
        },
        {   
            path: "/profile/edit", 
            name: "profileEdit", 
            component: EditProfile 
        },
        {   
            path: "/profile/edit/Password", 
            name: "editPassword", 
            component: EditPassword 
        },
        {
            path: "/profile/:id/friends",
            name: "friends",
            component: FriendsView,
        },
        {
            path: "/:id/postDetail",
            name: "postDetails",
            component: PostDetailView,
        },
        {
            path: "/chat",
            name: "chat",
            component: ChatView,
        },
        {
            path: "/about",
            name: "about",
            component: () => import("../views/AboutView.vue"),
        },
    ],
});

export default router;
