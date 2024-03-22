<template>
  <div>
    <v-btn v-if="isLoggedIn" color="primary" @click="logout">Logout</v-btn>
  </div>
</template>

<script>
import apiClient from "../../utils/apiClient";

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
        await apiClient.post("/authx/logout/");
        localStorage.removeItem("token");
        this.$emit("logged-out");
        this.$router.push({ name: "Home" });
        this.$router.go(0);
      } catch (error) {
        if (error.response) {
          console.error("Logout failed with status:", error.response.status);
          console.error("Response data:", error.response.data);
        } else if (error.request) {
          console.error("No response received from the server:", error.request);
        } else {
          console.error("Error setting up the request:", error.message);
        }
        console.error("Error details:", error.config);
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
