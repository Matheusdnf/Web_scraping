export const fetchOperatorData = async (aumentarQuantidade = 40) => {
  const response = await fetch(
    `http://localhost:8000/tudo?aumentar_quantidade=${aumentarQuantidade}`
  );

  if (!response.ok) {
    throw new Error(`Erro HTTP: ${response.status}`);
  }

  return await response.json();
};
