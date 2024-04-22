<template>
  <div class="total-users">
    <p class="title">Total users</p>
    <p class="users">{{ users }}</p>
  </div>
</template>

<script>
import apiClient from "../../utils/apiClient";

export default {
  data() {
    return {
      users: Number,
    };
  },
  mounted() {
    this.fetchTotalUsers();
  },
  methods: {
    fetchTotalUsers() {
      apiClient
        .get("http://127.0.0.1:8000/analytics/total-users/")
        .then((response) => {
          this.users = response.data.total_users;
        })
        .catch((error) => {
          console.error("Error fetching total users:", error);
        });
    },
  },
};
</script>

<style scoped>
.total-users {
  padding: 20px;
}

.title {
  text-align: center;
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 20px;
}
</style>
