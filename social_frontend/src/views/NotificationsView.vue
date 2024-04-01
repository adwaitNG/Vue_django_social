<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-center col-span-3 space-y-4">
            <div class="main-center col-span-2 space-y-4">
                <div
                    class="p-4 bg-white border border-gray-200 rounded-lg"
                    v-for="notifiy in notifications"
                    v-bind:key="notifiy.id"
                >
                    {{ notifiy.body }}
                    <template
                        v-if="
                            notifiy.type_of_notification == 'postLike' || notifiy.type_of_notification == 'postComment'
                        "
                    >
                        <button class="underline" @click="readNotification(notifiy)">Check the post</button>
                    </template>

                    <template v-else>
                        <button class="underline" @click="readNotification(notifiy)">Check the request</button>
                    </template>
                </div>
            </div>
        </div>
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>
<script>
import axios from "axios";
import PeopleYouMayKnow from "@/components/peopleYouMayKnow.vue";
import Trends from "@/components/Trends.vue";
import { compileScript } from "vue/compiler-sfc";
import FriendsView from "./FriendsView.vue";

export default {
    name: "NotificationView",
    components: { PeopleYouMayKnow, Trends },
    data() {
        return {
            notifications: [],
        };
    },

    mounted() {
        this.getNotifications(), this.add2;
    },

    methods: {
        getNotifications() {
            axios
                .get("api/notifications/")
                .then((response) => {
                    // console.log("data in Notification", response.data);
                    this.notifications = response.data;
                })
                .catch((error) => {
                    console.log("Error in Notifications", error);
                });
        },
        add2() {
            console.log("Second Method can also be added to the mounted");
        },
        async readNotification(notifiy) {
            await axios
                .post(`/api/notifications/read/${notifiy.id}/`)
                .then((response) => {
                    console.log("reponse for readin noti", response.data);
                    if (notifiy.type_of_notification == "postLike" || notifiy.type_of_notification == "postComment") {
                        //redirect to post
                        this.$router.push({ name: "postDetails", params: { id: notifiy.post.id } });
                    } else {
                        // redirect to friendship request
                        this.$router.push({ name: "friends", params: { id: notifiy.created_for } });
                    }
                })
                .catch((error) => {
                    console.log("error in reading noti", error);
                });
        },
    },
};
</script>
