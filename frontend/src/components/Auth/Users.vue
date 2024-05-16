<template>
  <v-container class="justify-center">
    <v-card class="mx-auto" max-width="800">
      <v-card-title class="primary">Users</v-card-title>

      <v-text-field
        v-model="searchQuery"
        label="Search"
        @input="fetchUsers"
        class="search-bar"
      ></v-text-field>

      <ul>
        <li v-for="user in users" :key="user.id" class="user-item">
          <span class="user-username"
            >{{ user.first_name }} {{ user.last_name }} ({{
              user.username
            }})</span
          >
          <v-btn
            class="add-friend-button"
            v-if="!isFriend(user.id)"
            @click="addFriend(user.id)"
          >
            Add Friend
          </v-btn>
        </li>
      </ul>

      <v-card-title class="primary">Friends</v-card-title>
      <v-text-field
        v-model="searchFriendQuery"
        label="Search"
        @input="fetchFriends"
        class="search-bar"
      ></v-text-field>
      <ul>
        <li v-for="friend in friends" :key="friend.id" class="user-item">
          <span class="user-username"
            >{{ friend.friend.first_name }} {{ friend.friend.last_name }} ({{
              friend.friend.username
            }})</span
          >
        </li>
      </ul>
    </v-card>
  </v-container>
</template>

<script>
import apiClient from "../../utils/apiClient";
import { jwtDecode } from "jwt-decode";

export default {
  data() {
    return {
      users: [],
      searchQuery: "",
      friends: [],
    };
  },
  created() {
    if (!this.isAuthenticated()) {
      this.$router.push("/login");
    } else {
      this.fetchUsers();
      this.fetchFriends();
    }
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    isAuthenticated() {
      const token = localStorage.getItem("token");
      return token !== null;
    },
    fetchUsers() {
      const params = { query: this.searchQuery };
      apiClient
        .get("http://127.0.0.1:8000/authx/users/", { params })
        .then((response) => {
          this.users = response.data;
        })
        .catch((error) => {
          console.error("Error fetching users:", error);
        });
    },
    fetchFriends(query = "") {
      const params = { query: this.searchFriendQuery };
      apiClient
        .get("http://127.0.0.1:8000/contacts/friendships/", { params })
        .then((response) => {
          this.friends = response.data.results;
        })
        .catch((error) => {
          console.error("Error fetching friends:", error);
        });
    },
    addFriend(friendId) {
      const userId = this.getCurrentUserId();
      apiClient
        .post("http://127.0.0.1:8000/contacts/friendships/", {
          user: userId,
          friend: friendId,
        })
        .then((response) => {
          alert("Friend added successfully!");
          this.fetchUsers();
          this.fetchFriends();
        })
        .catch((error) => {
          console.error("Error adding friend:", error);
          alert("Failed to add friend.");
        });
    },
    getCurrentUserId() {
      const token = localStorage.getItem("token");
      if (!token) {
        return null;
      }
      try {
        const decoded = jwtDecode(token);
        return decoded.user_id;
      } catch (error) {
        console.error("Error decoding token:", error);
        return null;
      }
    },
    isFriend(userId) {
      return this.friends.some((friendship) => friendship.friend.id === userId);
    },
  },
};
</script>

<style scoped>
.primary {
  background-color: #1976d2;
  color: white;
  padding: 10px 20px;
  border-radius: 4px;
}

.primary:hover {
  background-color: #1565c0;
}

.user-username {
  margin: 20px;
  padding: 10px;
}

.user-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 20px 0;
}

.add-friend-button {
  background-color: #4caf50;
  color: white;
}

.add-friend-button:hover {
  background-color: #45a049;
}
</style>
