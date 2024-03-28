<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img :src="user.get_avatar" class="mb-6 mx-auto rounded-full" />

                <p>
                    <strong>{{ user.name }}</strong>
                </p>

                <div class="mt-6 flex space-x-8 justify-around" v-if="user.id">
                    <RouterLink :to="{ name: 'friends', params: { id: user.id } }" class="text-xs text-gray-500"
                        >{{ user.friends_count }} friends</RouterLink
                    >
                    <p class="text-xs text-gray-500">{{ user.post_count }} posts</p>
                </div>

                <div class="mt-6" v-if="userStore.user.isAuthenticated">
                    <button
                        v-if="userStore.user.id !== user.id && can_send_friend_req"
                        class="inline-block py-4 px-3 bg-purple-600 test-xs text-white rounded-lg"
                        @click="sendFriendshipRequest"
                    >
                        Send Friend Request
                    </button>
                    <button
                        v-if="userStore.user.id !== user.id"
                        class="inline-block py-4 mt-4 px-3 bg-purple-600 test-xs text-white rounded-lg"
                        @click="sendDirectMessage"
                    >
                        Send Direct Message
                    </button>
                    <button
                        v-if="userStore.user.id === user.id"
                        class="inline-block mr-4 py-4 px-3 bg-yellow-600 test-xs text-white rounded-lg"
                        @click="logout"
                    >
                        Logout
                    </button>
                    <RouterLink
                        to="/profile/edit"
                        v-if="userStore.user.id === user.id"
                        class="inline-block py-4 mr-4 px-3 bg-purple-600 test-xs text-white rounded-lg"
                    >
                        Edit Profile
                    </RouterLink>
                </div>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4" v-if="userStore.user.isAuthenticated">
            <div class="main-center col-span-2 space-y-4">
                <div class="bg-white border border-gray-200 rounded-lg" v-if="userStore.user.id === user.id">
                    <FeedForm v-bind:user="user" v-bind:posts="posts" />
                </div>

                <div class="p-4 bg-white border border-gray-200 rounded-lg" v-for="post in posts" v-bind:key="post.id">
                    <FeedItem v-bind:post="post" />
                </div>
            </div>
        </div>
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>
<style>
input[type="file"] {
    display: none;
}
.custom-file-upload {
    border: 1px solid #ccc;
    display: inline-block;
    padding: 6px 12px;
    cursor: pointer;
}
</style>

<script>
import PeopleYouMayKnow from "@/components/peopleYouMayKnow.vue";
import Trends from "@/components/Trends.vue";
import FeedItem from "@/components/FeedItem.vue";
import FeedForm from "@/components/FeedForm.vue";

import axios from "axios";
import { useUserStore } from "@/stores/user";
import { useToastStore } from "@/stores/toast";

export default {
    name: "ProfileView",

    setup() {
        const userStore = useUserStore();
        const toastStore = useToastStore();
        return {
            userStore,
            toastStore,
        };
    },

    components: {
        PeopleYouMayKnow,
        Trends,
        FeedItem,
        FeedForm,
    },
    data() {
        return {
            posts: [],
            user: {
                id: null,
            },
            can_send_friend_req: null,
        };
    },
    mounted() {
        this.getFeed();
    },
    watch: {
        "$route.params.id": {
            handler: function () {
                this.getFeed();
            },
            deep: true,
            immediate: true,
        },
    },
    methods: {
        onFileChnage(e) {
            // console.log(e.target.file);
            const file = e.target.files[0];
            this.url = URL.createObjectURL(file);
        },
        getFeed() {
            axios
                .get(`api/posts/profile/${this.$route.params.id}/`)
                .then((response) => {
                    // console.log("data", response.data);

                    this.posts = response.data.posts;
                    this.user = response.data.user;
                    this.can_send_friend_req = response.data.can_send_friend_req;
                  
                    // console.log(this.user.get_avatar);
                })
                .catch((error) => {
                    console.log("error", error);
                });
        },
        sendDirectMessage() {
            axios
                .get(`api/chat/${this.$route.params.id}/get-or-create/`)
                .then((response) => {
                    console.log("data", response.data);
                    this.$router.push("/chat");
                })
                .catch((error) => {
                    console.log("error", error);
                });
        },

        sendFriendshipRequest() {
            axios
                .post(`api/friends/${this.$route.params.id}/request/`)
                .then((response) => {
                    console.log("data", response.data);
                    this.can_send_friend_req = false;
                    if (response.data.message == "Request already sent") {
                        this.toastStore.showToast(5000, "The request has already been sent!", "bg-yellow-300");
                    } else {
                        this.toastStore.showToast(5000, "The request was sent!", "bg-emerald-300");
                    }
                })
                .catch((error) => {
                    console.log("error", error);
                });
        },
        logout() {
            this.userStore.removeToken();

            this.$router.push("/login");
        },
    },
};
</script>
