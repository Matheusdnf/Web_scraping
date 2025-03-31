<template>
  <div class="error-message">Ocorreu um erro: {{ message }}</div>
</template>

<script>
export default {
  name: "ErrorMessage",
  props: {
    message: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.error-message {
  color: red;
  margin: 10px 0;
  font-weight: bold;
}
</style>
