<template>
  <v-container class="justify-center">
    <v-card class="mx-auto" max-width="400">
      <v-card-title class="primary">
        <span class="headline">Login</span>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="login">
          <v-text-field
            v-model="username"
            label="Username"
            required
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Password"
            type="password"
            required
          ></v-text-field>
          <v-btn variant="tonal" color="primary" type="submit">Login</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post(
          "http://localhost:8000/authx/token/",
          {
            username: this.username,
            password: this.password,
          },
        );
        const token = response.data.access;
        localStorage.setItem("token", token);
        this.$router.push({ name: "Home" });
        this.$router.go(0);
      } catch (error) {
        console.error("Login failed:", error);
      }
    },
  },
};
</script>

<style>
.primary {
  background-color: #1976d2;
  color: white;
}
</style>
