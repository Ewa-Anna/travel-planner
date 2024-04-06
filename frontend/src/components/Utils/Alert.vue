<template>
  <div
    v-if="showAlert"
    id="alert"
    class="alert"
    :style="{ backgroundColor: backgroundColor, color: textColor }"
  >
    <span>{{ alertMessage }}</span>
    <button @click="hideAlert" id="closeAlert">&times;</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showAlert: false,
      alertMessage: "",
      backgroundColor: "#f44336",
      textColor: "white",
    };
  },
  created() {
    try {
      if (this.$root.$options.eventBus) {
        this.$root.$options.eventBus.on("showAlert", this.show);
      }
    } catch (error) {
      console.error("Error in created hook:", error);
    }
  },
  methods: {
    show(message, backgroundColor = "#f44336", textColor = "white") {
      this.alertMessage = message;
      this.backgroundColor = backgroundColor;
      this.textColor = textColor;
      this.showAlert = true;

      setTimeout(() => {
        this.hideAlert();
      }, 5000);
    },
    hideAlert() {
      this.showAlert = false;
    },
  },
};
</script>

<style scoped>
.alert {
  background-color: #f44336;
  color: white;
  padding: 15px;
  margin-bottom: 20px;
  position: relative;
}

.alert button {
  position: absolute;
  top: 0;
  right: 0;
  background-color: transparent;
  border: none;
  color: white;
  font-weight: bold;
  cursor: pointer;
}
</style>
