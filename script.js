async function carregarFilmes() {
  try {
    // Pega os dados do JSON
    const resposta = await fetch("filmes.json");
    const filmes = await resposta.json();

    const container = document.getElementById("listaFilmes");
    container.innerHTML = "";

    if (filmes.length === 0) {
      container.innerHTML = `
        <article class="mensagemVazia">
          <p>Não há filmes cadastrados no momento.</p>
          <p>Comece adicionando seu primeiro filme ao sistema!</p>
        </article>
      `;
      return;
    }

    // Monta os cards
    filmes.forEach(f => {
      const card = document.createElement("div");
      card.classList.add("cardFilme");

      card.innerHTML = `
        <h3>${f.filme} <span class="anoFilme">(${f.ano})</span></h3>
        <p><strong>Diretor:</strong> ${f.diretor}</p>
        <p><strong>Gênero:</strong> ${f.genero}</p>
        <p><strong>Produtora:</strong> ${f.produtora}</p>
        <p><strong>Atores:</strong> ${f.atores}</p>
        <p><strong>Sinopse:</strong> ${f.sinopse}</p>
      `;

      container.appendChild(card);
    });
  } catch (erro) {
    console.error("Erro ao carregar filmes:", erro);
  }
}

// Executa ao abrir a página
carregarFilmes();
