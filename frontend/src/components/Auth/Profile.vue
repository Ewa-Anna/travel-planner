<template>
  <v-container class="justify-center">
    <v-card class="mx-auto" max-width="800">
      <v-card-title class="primary">
        <span class="headline">Profile</span>
      </v-card-title>
      <v-card-text>
        <div v-if="profile" class="profile-info">
          <img :src="profile.photo" alt="Profile Photo" class="profile-photo" />
          <p><strong>Bio:</strong> {{ profile.bio }}</p>
          <p><strong>Birthdate:</strong> {{ profile.birthdate }}</p>
        </div>
        <div v-else>
          <p>Loading...</p>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import apiClient from "../../utils/apiClient";

export default {
  data() {
    return {
      profile: null,
    };
  },
  created() {
    if (!this.isAuthenticated()) {
      this.$router.push("/login");
    } else {
      this.fetchProfile();
    }
  },
  methods: {
    isAuthenticated() {
      const token = localStorage.getItem("token");
      return token !== null;
    },
    fetchProfile() {
      apiClient
        .get("http://localhost:8000/authx/profile/", {})
        .then((response) => {
          this.profile = response.data;
        })
        .catch((error) => {
          console.error("Error fetching profile:", error);
        });
    },
  },
};
</script>

<style scoped>
.profile-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin: 20px;
  padding: 20px;
}

.profile-photo {
  max-width: 80%;
  max-height: 80%;
  border-radius: 50%;
}
</style>
