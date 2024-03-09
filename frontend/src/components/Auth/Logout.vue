<template>
  <div>
    <v-btn v-if="isLoggedIn" color="primary" @click="logout">Logout</v-btn>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";

export default {
  props: {
    isLoggedIn: Boolean,
  },
  data() {
    return {
      username: "",
    };
  },
  methods: {
    async logout() {
      try {
        const token = localStorage.getItem("token");
        await axios.post("http://localhost:8000/authx/logout/", null, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        localStorage.removeItem("token");
        this.$emit("logged-out");
        this.$router.push({ name: "Home" });
        this.$router.go(0);
      } catch (error) {
        console.error("Logout failed:", error);
      }
    },
  },
  //   async mounted() {
  //     if (this.isLoggedIn) {
  //       try {
  //         const response = await axios.get('http://localhost:8000/authx/profile/');
  //         this.username = response.data.username;
  //       } catch (error) {
  //         console.error('Failed to fetch user data:', error);
  //       }
  //     }
  //   }
};
</script>
