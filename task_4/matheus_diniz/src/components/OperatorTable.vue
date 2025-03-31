<template>
  <table class="operator-table">
    <thead>
      <tr>
        <th>Registro ANS</th>
        <th>CNPJ</th>
        <th>Razão Social</th>
        <th>Nome Fantasia</th>
        <th>Modalidade</th>
        <th>Cidade</th>
        <th>UF</th>
        <th>Telefone</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in data" :key="index">
        <td>{{ item.registro_ans }}</td>
        <td>{{ formatCNPJ(item.cnpj) }}</td>
        <td>{{ item.razao_social }}</td>
        <td>{{ item.nome_fantasia || "-" }}</td>
        <td>{{ item.modalidade }}</td>
        <td>{{ item.cidade }}</td>
        <td>{{ item.uf }}</td>
        <td>
          {{
            item.ddd ? `(${item.ddd}) ${item.telefone}` : item.telefone || "-"
          }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "OperatorTable",
  props: {
    data: {
      type: Array,
      required: true,
    },
  },
  methods: {
    formatCNPJ(cnpj) {
      if (!cnpj) return "-";
      return cnpj.replace(
        /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
        "$1.$2.$3/$4-$5"
      );
    },
  },
};
</script>

<style scoped>
.operator-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  font-size: 0.9em;
}

.operator-table th,
.operator-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.operator-table th {
  background-color: #4caf50;
  color: white;
  position: sticky;
  top: 0;
}

.operator-table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.operator-table tr:hover {
  background-color: #e6f7e6;
}
</style>
