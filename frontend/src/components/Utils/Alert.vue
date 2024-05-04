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
  mounted() {
    this.emitter.on("showAlert", ({ message, backgroundColor, textColor }) => {
      this.alertMessage = message;
      this.backgroundColor = backgroundColor;
      this.textColor = textColor;
      this.showAlert = true;

      setTimeout(() => {
        this.hideAlert();
      }, 10000);
    });
  },
  methods: {
    hideAlert() {
      this.showAlert = false;
    },
  },
};
</script>

<style scoped>
.alert {
  position: fixed; 
  top: 0;
  left: 50%;
  transform: translateX(-50%); 
  z-index: 9999;
  background-color: #e1f5fe;
  color: #0d47a1;
  padding: 15px;
  text-align: center;
  min-width: 400px;
  max-width: 1200px;
  border-radius: 10px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
}

.alert button {
  position: absolute;
  top: 5px;
  right: 5px;
  background-color: transparent;
  border: none;
  color: #000000;
  font-weight: bold;
  cursor: pointer;
}
</style>
