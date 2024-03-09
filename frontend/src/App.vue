<template>
  <v-app>
    <v-main>
      <router-link to="/">Home</router-link> |
      <router-link to="/about">About</router-link> |
      <div v-if="!isLoggedIn">
        <router-link to="/login">
          <v-btn color="primary">Login</v-btn>
        </router-link>
        <router-link to="/register">
          <v-btn color="primary">Register</v-btn>
        </router-link>
      </div>
      <div v-else>
        <p>Welcome {{ username }}</p>
        <Logout :isLoggedIn="isLoggedIn" @logged-out="handleLoggedOut" />
      </div>

      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { computed } from "vue";
import Logout from "./components/Auth/Logout.vue";
import { useRouter } from "vue-router";

const isLoggedIn = computed(() => {
  return localStorage.getItem("token") !== null;
});

const username = computed(() => {
  const token = localStorage.getItem("token");
  if (token) {
    const tokenPayload = JSON.parse(atob(token.split(".")[1]));
    return tokenPayload.username;
  }
  return null;
});
const router = useRouter();

const handleLoggedOut = () => {
  // Logic to handle the "logged-out" event
  console.log("User logged out");
  // You can perform additional actions here, such as updating the UI or redirecting the user
  router.push({ name: "Home" }); // Redirect to Home page after logout
};
</script>
