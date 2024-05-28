<template>
    <v-container class="justify-center">
      <v-card class="mx-auto" max-width="800">
        <v-card-title id="journal-title" class="primary">
          <span class="headline">All Journal Entries</span>
          <router-link to="/addjournal" class="new-journal">Add new entry</router-link>
        </v-card-title>
  
            <v-card-text>
            </v-card-text>  
        </v-card>  
    </v-container>
</template>

<script>
import apiClient from "../../utils/apiClient";

export default {
  data() {
    return {
        
};
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