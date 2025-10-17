async function carregarFilme() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id_filme");
  if (!id) return;

  try {
    const resposta = await fetch("/listar_filmes");
    const filmes = await resposta.json();
    const filme = filmes.find(f => f.id_filme == id);

    if (filme) {
      document.getElementById("titulo").textContent = filme.titulo;
      document.getElementById("ano").textContent = filme.ano;
      document.getElementById("duracao").textContent = filme.tempo_duracao;
      document.getElementById("linguagem").textContent = filme.linguagem;
    } else {
      document.querySelector(".dadosFilme").innerHTML = `
        <p>❌ Filme não encontrado.</p>
      `;
    }
  } catch (erro) {
    console.error("Erro ao carregar filme:", erro);
    document.querySelector(".dadosFilme").innerHTML = `
      <p>⚠️ Ocorreu um erro ao buscar o filme. Tente novamente.</p>
    `;
  }
}

carregarFilme();
