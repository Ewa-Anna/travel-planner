<template>
    <v-container class="justify-center">
        <v-card class="mx-auto" max-width="800">
            <v-card-title class="primary">Users</v-card-title>

            <v-text-field v-model="searchQuery" label="Search" @input="fetchUsers" class="search-bar"></v-text-field>

            <ul>
                <li v-for="user in users" :key="user.id">
                    <span class="user-username">{{ user.first_name }} {{ user.last_name }} ({{ user.username }})</span>
                </li>
            </ul>
        </v-card>
    </v-container>
</template>

<script>
import apiClient from "../../utils/apiClient";

export default {
    data() {
        return {
            users: [],
            searchQuery: '',
        };
    },
    created() {
        if (!this.isAuthenticated()) {
            this.$router.push("/login");
        } else {
            this.fetchUsers();
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
            apiClient.get('http://127.0.0.1:8000/authx/users/', { params })
                .then(response => {
                    this.users = response.data;
                })
                .catch(error => {
                    console.error('Error fetching users:', error);
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
    border-radius: 4px;
}

.primary:hover {
    background-color: #1565c0;
}

.user-username {
    margin: 20px;
    padding: 10px;
}
</style>