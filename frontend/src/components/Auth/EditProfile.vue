<template>
  <v-container class="justify-center">
    <v-card class="mx-auto" max-width="800">
      <v-card-title class="primary">Edit profile</v-card-title>
      <form @submit.prevent="submitForm" class="profile-form">
        <div class="form-group">
          <label for="first_name">First Name</label>
          <input
            type="text"
            id="first_name"
            v-model="formData.first_name"
            required
          />
        </div>
        <div class="form-group">
          <label for="last_name">Last Name</label>
          <input
            type="text"
            id="last_name"
            v-model="formData.last_name"
            required
          />
        </div>
        <div class="form-group">
          <label for="birthdate">Birthdate</label>
          <input
            type="date"
            id="birthdate"
            v-model="formData.birthdate"
            required
          />
        </div>
        <div class="form-group">
          <label for="photo">Photo URL</label>
          <input type="text" id="photo" v-model="formData.photo" />
        </div>
        <div class="form-group">
          <label for="bio">Bio</label>
          <textarea id="bio" v-model="formData.bio"></textarea>
        </div>
        <button type="submit" class="primary">Submit</button>
      </form>
    </v-card>
  </v-container>
</template>

<script>
import apiClient from "../../utils/apiClient";
import { mapActions } from "vuex";
import Alert from "../../components/Utils/Alert.vue";

export default {
  components: {
    Alert,
  },
  data() {
    return {
      formData: {
        first_name: "",
        last_name: "",
        birthdate: "",
        bio: "",
        photo: "",
      },
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
    ...mapActions(["fetchProfile"]),
    isAuthenticated() {
      const token = localStorage.getItem("token");
      return token !== null;
    },
    fetchProfile() {
      apiClient
        .get(`http://localhost:8000/authx/profile/`)
        .then((response) => {
          const profileData = response.data;
          this.formData = {
            first_name: profileData.user.first_name,
            last_name: profileData.user.last_name,
            birthdate: profileData.birthdate,
            bio: profileData.bio,
            photo: profileData.photo,
          };
        })
        .catch((error) => {
          console.error("Error fetching profile data:", error);
        });
    },
    submitForm() {
      apiClient
        .patch(`http://localhost:8000/authx/profile/`, this.formData)
        .then((response) => {
          console.log("Form data:", response.data);
          this.$router.push("/profile");
          this.emitter.emit("showAlert", {
            message: response.data.message,
            backgroundColor: "#4CAF50",
            textColor: "white",
          });
          this.formData = {
            name: "",
          };
        })
        .catch((error) => {
          console.error("Error submitting form:", error);
          this.emitter.emit("showAlert", {
            message: "An unexpected error occurred",
            backgroundColor: "#f44336",
            textColor: "white",
          });
        });
    },
  },
};
</script>

<style scoped>
.primary {
  background-color: #1976d2;
  color: white;
  padding: 10px 20px;
  text-decoration: none;
  border-radius: 4px;
}

.primary:hover {
  background-color: #1565c0;
}

.profile-form {
  padding: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
}

input[type="text"],
input[type="date"],
textarea,
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  cursor: pointer;
}
</style>
