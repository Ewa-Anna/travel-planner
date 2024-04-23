<template>
  <div>
    <v-btn v-if="isLoggedIn" color="primary" @click="logout">Logout</v-btn>
  </div>
</template>

<script>
import apiClient from "../../utils/apiClient";
import Alert from "../../components/Utils/Alert.vue";

export default {
  components: {
    Alert,
  },
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
      apiClient
        .post("/authx/logout/")
        .then((response) => {
          localStorage.removeItem("token");
          this.$emit("logged-out");
          this.username = "";
          this.emitter.emit("showAlert", {
            message: response.data.message,
            backgroundColor: "#4CAF50",
            textColor: "white",
          });
          this.$router.push({ name: "Home" });
          this.$router.go(0);
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
