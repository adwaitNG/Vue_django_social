<template>
  <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
    <div class="main-left col-span-1">
      <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
        <img src="https://i.pravatar.cc/300?img=70" class="mb-6 rounded-full" />

        <p>
          <strong>{{ user.name }}</strong>
        </p>

        <div class="mt-6 flex space-x-8 justify-around">
          <p class="text-xs text-gray-500">{{ user.friends_count }} friends</p>
          <p class="text-xs text-gray-500">120 posts</p>
        </div>
      </div>
    </div>
    <div class="main-center col-span-2 space-y-4">
      <div
        class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-3 gap-4"
        v-if="friends.length"
      >
        <div
          class="p-4 text-center bg-gray-100 rounded-lg"
          v-for="user in friends"
          v-bind:key="user.id"
        >
          <img
            src="https://i.pravatar.cc/300?img=70"
            class="mb-6 rounded-full"
          />

          <p>
            <strong>
              <RouterLink :to="{ name: 'profile', params: { id: user.id } }">
                {{ user.name }}
              </RouterLink>
            </strong>
          </p>

          <div class="mt-6 flex space-x-8 justify-around">
            <p class="text-xs text-gray-500">
              {{ user.friends_count }} friends
            </p>
            <p class="text-xs text-gray-500">120 posts</p>
          </div>
        </div>
      </div>

      <div
        class="p-4 bg-white border border-gray-200"
        v-if="friendshipRequest.length"
      >
        <hr />
        <h2 class="text-center text-xl mb-4">Friendship Requests</h2>
        <div
          class="p-4 text-center bg-gray-100 rounded-lg"
          v-for="friendshipRequest in friendshipRequest"
          v-bind:key="friendshipRequest.id"
        >
          <img
            src="https://i.pravatar.cc/100?img=70"
            class="mb-6 mx-auto rounded-full"
          />

          <p>
            <strong>
              <RouterLink
                :to="{
                  name: 'profile',
                  params: { id: friendshipRequest.created_by.id },
                }"
              >
                {{ friendshipRequest.created_by.name }}
              </RouterLink>
            </strong>
          </p>

          <div class="mt-6 flex space-x-8 justify-around">
            <p class="text-xs text-gray-500">
              {{ friendshipRequest.created_by.friends_count }} friends
            </p>
            <p class="text-xs text-gray-500">120 posts</p>
          </div>
          <div class="mt-6 space-x-5">
            <button
              class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg"
              @click="handelRequest('acceped', friendshipRequest.created_by.id)"
            >
              Accept
            </button>
            <button
              class="inline-block py-4 px-6 bg-yellow-600 text-white rounded-lg"
              @click="
                handelRequest('rejected', friendshipRequest.created_by.id)
              "
            >
              Reject
            </button>
          </div>
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
import PeopleYouMayKnow from "@/components/peopleYouMayKnow.vue";
import Trends from "@/components/Trends.vue";
import FeedItem from "@/components/FeedItem.vue";

import axios from "axios";
import { useUserStore } from "@/stores/user";
import { useToastStore } from "@/stores/toast";

export default{
  name: "FriendsView",

  setup() {
    const userStore = useUserStore();
    const toastStore = useToastStore();
    return {
      userStore,
      toastStore,
    };
  },

  components: { PeopleYouMayKnow, Trends, FeedItem },
  data() {
    return {
      user: {},
      friendshipRequest: [],
      friends: [],
    };
  },
  mounted() {
    this.getFriends();
  },
  methods: {
    getFriends() {
      axios
        .get(`api/friends/${this.$route.params.id}/`)
        .then((response) => {
          console.log("data", response.data);

          this.friendshipRequest = response.data.requests;
          this.friends = response.data.friends;
          this.user = response.data.user;
        })
        .catch((error) => {
          console.log("error", error);
        });
    },

    handelRequest(status, id) {
      // console.log("status" , status)

      axios
        .post(`/api/friends/${id}/${status}/`)
        .then((response) => {
          console.log("data", response.data);
        
        })
        .catch((error) => {
          console.log("error", error);
        });
    },
  },
}
</script>
