<template>
    <form v-on:submit.prevent="submitPost" method="post">
        <div class="p-4">
            <textarea
                v-model="body"
                class="p-4 w-full bg-gray-100 rounded-lg"
                placeholder="What are you thinking about?"
            ></textarea>
            <label> <input type="checkbox" v-model="is_private" /> Make it private </label>
            <div id="preview" v-if="url">
                <img :src="url" class="w-[100] mt-2 rounded-lg" />
            </div>
        </div>

        <div class="p-4 border-t border-gray-100 flex justify-between">
            <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">
                <input type="file" ref="file" @change="onFileChnage" />Attach image
            </label>
            <button href="#" class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
        </div>
    </form>
</template>
<script>
import axios from "axios";

export default {
    name: "FeedForm",
    props: {
        user: Object,
        posts: Array,
    },

    data() {
        return {
            body: "",
            url: null,
            is_private: false,
        };
    },
    methods: {
        submitPost() {
            console.log("Submit Form ", this.body);
            let formData = new FormData();
            formData.append("image", this.$refs.file.files[0]);
            formData.append("body", this.body);
            formData.append("is_private", this.is_private);

            axios
                .post("api/posts/create/", formData, { headers: { "Content-Type": "multipart/form-data" } })
                .then((response) => {
                    console.log("data", response.data);

                    this.posts.unshift(response.data);
                    this.body = "";
                    this.url = null;
                    if (this.user) {
                        this.user.post_count += 1;
                    }
                    this.is_private = false;
                })
                .catch((error) => {
                    console.log("error", error);
                });
        },
    },
};
</script>
