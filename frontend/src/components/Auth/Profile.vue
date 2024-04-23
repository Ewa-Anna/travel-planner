<template>
  <v-container class="justify-center">
    <v-card class="mx-auto" max-width="800">
      <v-card-title id="profile" class="primary">
        <span class="headline">Profile</span>
        <router-link to="/editprofile" class="edit-profile"
          >Edit Profile</router-link
        >
      </v-card-title>
      <v-card-text>
        <div v-if="profile" class="profile-info">
          <img :src="profile.photo" alt="Profile Photo" class="profile-photo" />
          <p class="welcome">
            Hi {{ profile.user.first_name }} {{ profile.user.last_name }}!
          </p>
          <p><strong>Profile info:</strong></p>
          <p class="bio">{{ profile.bio }}</p>
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
          console.log(response.data);
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
  max-width: 300px;
  max-height: 200px;
  border-radius: 50%;
  margin-bottom: 30px;
}

.edit-profile {
  display: inline-block;
  background-color: #007bff;
  border-radius: 6px;
  padding: 8px 16px;
  border: none;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  padding: 8px;
}

.edit-profile:hover {
  text-decoration: none;
  background-color: #0056b3;
}

#profile {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.welcome {
  margin-bottom: 20px;
}

.bio {
  text-align: justify;
}
</style>
