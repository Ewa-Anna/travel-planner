<template>
    <v-container class="justify-center">
      <v-card class="mx-auto" max-width="800">
        <v-card-title id="journal-title" class="primary">
          <span class="headline">All Journal Entries</span>
          <router-link to="/addjournal" class="new-journal">Add new entry</router-link>
        </v-card-title>
  
            <v-card-text>
                <v-list>
          <v-list-item v-for="entry in journalEntries" :key="entry.id">
            <v-list-item-content>
              <v-list-item-title>{{ entry.title }}</v-list-item-title>
              <v-list-item-subtitle>{{ entry.notes }}</v-list-item-subtitle>
              <v-list-item-subtitle>Created: {{ entry.created }}</v-list-item-subtitle>
              <v-list-item-subtitle>Updated: {{ entry.updated }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>

        <v-pagination
          v-if="totalPages > 1"
          v-model="currentPage"
          :length="totalPages"
          @input="fetchJournalEntries"
        ></v-pagination>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import apiClient from "../../utils/apiClient";

export default {
  data() {
    return {
      journalEntries: [],
      itemsPerPage: 9,
      totalPages: 1,
      currentPage: 1,
    };  },

    created() {
    if (!this.isAuthenticated()) {
      this.$router.push("/login");
    } else {
      this.fetchJournalEntries();
    }
  },

  methods: {
    isAuthenticated() {
      const token = localStorage.getItem("token");
      return token !== null;
    },
    fetchJournalEntries() {
      const limit = this.itemsPerPage;
      const offset = (this.currentPage - 1) * limit;

      apiClient
        .get("http://localhost:8000/journal/travel-journal/", {
          params: {
            limit: limit,
            offset: offset,
          },
        })
        .then((response) => {
          this.journalEntries = response.data.results;
          this.totalPages = Math.ceil(response.data.count / this.itemsPerPage);
        })
        .catch((error) => {
          console.error("Error fetching journal entries:", error);
        });
    },
  },
};
</script>


<style>
.primary {
  background-color: #1976d2;
  color: white;
}


.new-journal {
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

.new-journal:hover {
  text-decoration: none;
  background-color: #0056b3;
}

#journal-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>