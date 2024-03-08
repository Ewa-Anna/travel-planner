<template>
  <v-container>
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
          <v-btn color="primary" type="submit">Login</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    login() {
      console.log(
        "Logging in with username:",
        this.username,
        "and password:",
        this.password,
      );
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
