async function carregarFilmes() {
  try {
    // Agora busca na rota correta (API JSON)
    const resposta = await fetch("/listar_filmes");
    const filmes = await resposta.json();

    const container = document.getElementById("listaFilmes");
    container.innerHTML = "";

    if (!filmes || filmes.length === 0) {
      container.innerHTML = `
        <article class="mensagemVazia">
          <p>Não há filmes cadastrados no momento.</p>
          <p>Comece adicionando seu primeiro filme!</p>
        </article>
      `;
      return;
    }

    filmes.forEach(f => {
      const card = document.createElement("div");
      card.classList.add("cardFilme");

      card.innerHTML = `
        <h3>${f.titulo} <span class="anoFilme">(${f.ano})</span></h3>
        <p><strong>Diretor:</strong> ${f.diretor}</p>
        <p><strong>Atores:</strong> ${f.atores}</p>
        <p><strong>Gênero:</strong> ${f.genero}</p>
        <p><strong>Idioma:</strong> ${f.linguagem}</p>
        <p><strong>País:</strong> ${f.pais}</p>
        <p><strong>Produtora:</strong> ${f.produtora}</p>
        <p><strong>Duração:</strong> ${f.tempo_duracao}</p>
      `;

      container.appendChild(card);
    });

  } catch (erro) {
    console.error("Erro ao carregar filmes:", erro);
  }
}

carregarFilmes();
