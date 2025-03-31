<template>
  <div id="app">
    <h1>Dados da Operadora de Saúde</h1>
    <operator-data />
  </div>
</template>

<script>
import OperatorData from "./components/OperatorData.vue";

export default {
  name: "App",
  components: {
    OperatorData,
  },
};
</script>
