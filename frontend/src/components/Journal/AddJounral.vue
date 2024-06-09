<template>
    <v-container class="justify-center">
        <v-card class="mx-auto" max-width="800">
            <v-card-title class="primary">Journal Details</v-card-title>
            <form @submit.prevent="submitForm" class="journal-form">
                <div class="form-group">
                    <label for="title">Title:</label>
                    <input type="text" id="title" v-model="formData.title" required />
                </div>
                <div class="form-group">
                    <label for="notes">Notes:</label>
                    <textarea id="notes" v-model="formData.notes" required></textarea>
                </div>
                <button type="submit" class="primary">Submit</button>
            </form>
        </v-card>
    </v-container>
</template>


<script>
import apiClient from "../../utils/apiClient";
import Alert from "../../components/Utils/Alert.vue";


export default {
    components: {
        Alert,
    },
    data() {
        return {
            formData: {
                id: 0,
                tags: [],
                title: '',
                notes: '',
                created: new Date().toISOString(),
                updated: new Date().toISOString(),
                trip: 0,
                user: 0
            }
        };
    },
    created() {
        this.checkAuthentication();

    },
    methods: {
        checkAuthentication() {
            if (!this.isAuthenticated()) {
                this.$router.push("/login");
            }
        },
        isAuthenticated() {
            const token = localStorage.getItem("token");
            return token !== null;
        },
        submitForm() {
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


.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
}

input[type="text"],
input[type="date"],
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

#scroll-form-group {
    max-height: 200px;
    overflow-y: auto;
}

.add-button {
    background-color: #1976d2;
    color: white;
    padding: 2px 4px;
    text-decoration: none;
    border-radius: 4px;
    display: inline-block;
}

.add-button:hover {
    background-color: #1565c0;
}

.journal-form {
    padding: 20px;
}
</style>