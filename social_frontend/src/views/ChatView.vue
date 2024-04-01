<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 rounded-lg">
                <h3 class="mb-6 text-xl">People</h3>

                <div class="space-y-4">
                    <div
                        class="flex items-center justify-between"
                        v-for="converstion in converstions"
                        v-bind:key="converstion.id"
                    >
                        <div class="flex items-center space-x-2">
                            <div class="flex items-center space-x-2">
                                <div
                                    v-for="user in converstion.users"
                                    v-bind:key="user.id"
                                    v-on:click="getMessages(converstion.id)"
                                >
                                    <img :src="user.get_avatar" class="w-[40px] rounded-full" />
                                    <p class="text-xs font-bold" v-if="user.id !== userStore.user.id">
                                        {{ user.name }}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <span class="text-xs text-gray-500">{{ converstion.modified_at_formatted }} ago</span>
                    </div>
                </div>
            </div>
        </div>
        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
                <div class="flex flex-col flex-grow p-4">
                    <div v-for="message in activeConversation.messages" v-bind:key="message.id">
                        <div
                            class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end"
                            v-if="message.created_by.id == userStore.user.id"
                        >
                            <div>
                                <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                    <p class="text-sm">
                                        {{ message.body }}
                                    </p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none"
                                    >{{ message.created_at_formatted }} ago</span
                                >
                            </div>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full" />
                            </div>
                        </div>

                        <div class="flex w-full mt-2 space-x-3 max-w-md" v-else>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img :src="message.created_by.get_avatar" class="w-[40px] rounded-full" />
                            </div>
                            <div>
                                <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                                    <p class="text-sm">
                                        {{ message.body }}
                                    </p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none"
                                    >{{ message.created_at_formatted }} ago</span
                                >
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="bg-white border border-gray-200 rounded-lg">
                <form v-on:submit.prevent="sendMessage(activeConversation.id)">
                    <div class="p-4">
                        <textarea
                            v-model="body"
                            class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="Write a message"
                        ></textarea>
                    </div>
                    <div class="p-4 border-t border-gray-100 flex justify-between">
                        <button class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Send</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { useUserStore } from "@/stores/user";

export default {
    name: "ChatView",
    setup() {
        const userStore = useUserStore();

        return {
            userStore,
        };
    },
    data() {
        return {
            converstions: [],
            activeConversation: {},
            body: "",
        };
    },

    mounted() {
        this.getConverstaion();
    },

    methods: {
        getConverstaion() {
            axios
                .get("/api/chat/")
                .then((response) => {
                    // console.log("data", response.data);
                    this.converstions = response.data;

                    if (this.converstions.length) {
                        this.activeConversation = this.converstions[0];
                    }

                    this.getMessages(this.activeConversation.id);
                })
                .catch((error) => {
                    console.log("error", error);
                });
        },

        getMessages(id) {
            axios
                .get(`api/chat/${id}/`)
                .then((response) => {
                    // console.log("data", response.data);

                    this.activeConversation = response.data;
                })
                .catch((error) => {
                    console.log("error", error);
                });
        },

        sendMessage(id) {
            console.log("send Messagee", this.body);
            axios
                .post(`api/chat/${id}/send/`, { body: this.body })
                .then((response) => {
                    console.log("data", response.data);

                    this.activeConversation.messages.push(response.data);

                    this.body = " ";
                })
                .catch((error) => {
                    console.log("error", error);
                });
        },
    },
};
</script>
