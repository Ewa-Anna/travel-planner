<template>
  <v-app>
    <v-main>
      <div class="navigation">
        <router-link to="/" class="nav-link" exact-active-class="active"
          >Home</router-link
        >
        <router-link to="/about" class="nav-link" exact-active-class="active"
          >About</router-link
        >
        <router-link to="/trips" class="nav-link" exact-active-class="active"
          >All Trips</router-link
        >
        <router-link to="/mytrips" class="nav-link" exact-active-class="active"
          >My Trips</router-link
        >
        <div v-if="!isLoggedIn" class="auth-section">
          <router-link to="/login" class="auth-link">
            <v-btn color="primary" exact-active-class="active">Login</v-btn>
          </router-link>
          <router-link to="/register" class="auth-link">
            <v-btn color="primary" exact-active-class="active">Register</v-btn>
          </router-link>
        </div>
        <div v-else class="auth-section">
          <div v-if="username" class="welcome-message">
            Welcome {{ username }}
          </div>

          <router-link to="/profile" exact-active-class="active">
            <v-btn color="primary">Profile</v-btn>
          </router-link>
          <Logout :isLoggedIn="isLoggedIn" @logged-out="handleLoggedOut" />
        </div>
      </div>

      <Alert ref="alertComponent" />

      <router-view />
      <footer class="footer">
        <a href="https://www.facebook.com/" class="social-link" target="_blank">
          <FontAwesomeIcon :icon="['fab', 'fa-facebook']" :size="iconSize" />
        </a>
        <a
          href="https://github.com/Ewa-Anna/"
          class="social-link"
          target="_blank"
        >
          <FontAwesomeIcon :icon="['fab', 'fa-github']" :size="iconSize" />
        </a>
        <a
          href="https://www.linkedin.com/in/ewa-kucala/"
          class="social-link"
          target="_blank"
        >
          <FontAwesomeIcon :icon="['fab', 'fa-linkedin']" :size="iconSize" />
        </a>
        <a
          href="https://www.instagram.com/?hl=pl"
          class="social-link"
          target="_blank"
        >
          <FontAwesomeIcon :icon="['fab', 'fa-instagram']" :size="iconSize" />
        </a>
        <a href="https://www.youtube.com/" class="social-link" target="_blank">
          <FontAwesomeIcon :icon="['fab', 'fa-youtube']" :size="iconSize" />
        </a>
      </footer>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";

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
  console.log("User logged out");
  router.push({ name: "Home" });
};

const iconSize = "lg";
</script>

<style>
.navigation {
  background-color: #1976d2;
  color: white;
  padding: 10px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 80%;
  margin: 0 auto;
  border-radius: 5px;
}

.nav-link {
  color: white;
  text-decoration: none;
  margin-right: 10px;
  transition: color 0.1s;
}

.nav-link:hover {
  color: #999999;
}

.active {
  color: #999999;
  font-weight: bold;
}

.auth-section {
  display: flex;
  align-items: center;
}

.auth-link {
  text-decoration: none;
  margin-right: 10px;
}

.welcome-message {
  margin: 10px;
  font-size: 16px;
}

.footer {
  background-color: #1976d2;
  color: white;
  padding: 10px;
  text-align: center;
  width: 80%;
  margin: 0 auto;
  border-radius: 5px;
}

.social-link {
  color: white;
  text-decoration: none;
  transition: color 0.1;
  margin: 0 5px;
  padding: 5px;
}

.social-link:hover {
  color: #999999;
}
</style>
