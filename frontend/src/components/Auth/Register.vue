<template>
  <v-container class="justify-center">
    <v-card class="mx-auto" max-width="400">
      <v-card-title class="primary">
        <span class="headline">Register</span>
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="register">
          <v-text-field
            v-model="username"
            label="Username"
            required
          ></v-text-field>
          <v-text-field v-model="email" label="E-mail" required></v-text-field>
          <v-text-field
            v-model="password"
            label="Password"
            type="password"
            required
          ></v-text-field>
          <v-text-field
            v-model="password_confirm"
            label="Confirm password"
            type="password"
            required
          ></v-text-field>
          <v-btn variant="tonal" color="primary" type="submit">Register</v-btn>
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
      email: "",
      password: "",
      password_confirm: "",
    };
  },
  methods: {
    async register() {
      try {
        if (this.password !== this.password_confirm) {
          console.error("Passwords do not match");
          return;
        }
        const response = await axios.post(
          "http://localhost:8000/authx/register/",
          {
            username: this.username,
            email: this.email,
            password: this.password,
            password_confirm: this.password_confirm,
          },
        );
        console.log("User registered successfully:", response.data);
        const token = response.data.access;
        localStorage.setItem("token", token);
        this.$router.push({ name: "Login" });
        this.$router.go(0);
      } catch (error) {
        console.error("Registration failed:", error);
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
