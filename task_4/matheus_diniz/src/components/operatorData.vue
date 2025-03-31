<template>
  <div>
    <h2 v-if="termo">Termo pesquisado: {{ termo }}</h2>

    <div class="controls">
      <button @click="fetchData">Carregar Dados</button>
      <button
        @click="addMoreData"
        :disabled="timeoutActive"
        :class="{ 'button-timeout': timeoutActive }"
      >
        {{
          timeoutActive
            ? `Aguarde... (${timeoutCountdown}s)`
            : "Adicionar mais informações"
        }}
      </button>
      <p>Itens Carregados {{ visibleData.length }}</p>
    </div>

    <loading-spinner v-if="loading" />
    <error-message v-if="error" :message="error" />

    <operator-table v-if="visibleData.length > 0" :data="visibleData" />
  </div>
</template>

<script>
import { fetchOperatorData } from "../services/apiService";
import OperatorTable from "./OperatorTable.vue";
import LoadingSpinner from "./LoadingSpinner.vue";
import ErrorMessage from "./ErrorMessage.vue";

export default {
  name: "OperatorData",
  components: {
    OperatorTable,
    LoadingSpinner,
    ErrorMessage,
  },
  data() {
    return {
      termo: "",
      data: [],
      loading: false,
      error: null,
      visibleLimit: 10,
      timeoutActive: false,
      timeoutCountdown: 0,
      timeoutInterval: null,
    };
  },
  computed: {
    filteredData() {
      return this.data.filter(
        (item) => item.nome_fantasia && item.nome_fantasia.trim() !== "-"
      );
    },
    visibleData() {
      return this.filteredData.slice(0, this.visibleLimit);
    },
  },
  methods: {
    async fetchData() {
      this.loading = true;
      this.error = null;
      this.visibleLimit = 10;

      try {
        const response = await fetchOperatorData(40); // 40 é o aumentar_quantidade
        this.termo = response.termo;
        this.data = response.resultados || response.dados || [];
      } catch (err) {
        this.error = err.message;
        this.data = [];
      } finally {
        this.loading = false;
      }
    },
    addMoreData() {
      if (this.timeoutActive) return;
      this.startTimeout();
      this.visibleLimit += 10;
    },
    startTimeout() {
      this.timeoutActive = true;
      this.timeoutCountdown = 3;

      this.timeoutInterval = setInterval(() => {
        this.timeoutCountdown--;

        if (this.timeoutCountdown <= 0) {
          clearInterval(this.timeoutInterval);
          this.timeoutActive = false;
        }
      }, 1000);
    },
  },
  beforeDestroy() {
    if (this.timeoutInterval) {
      clearInterval(this.timeoutInterval);
    }
  },
};
</script>

<style scoped>
.controls {
  margin: 20px 0;
}

.button-timeout {
  background-color: #cccccc !important;
  color: #666666 !important;
  cursor: not-allowed;
}
</style>
