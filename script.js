async function carregarFilmes() {
  try {
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

      // 1. Cria o HTML do poster (só se f.poster existir)
      const posterHtml = f.poster 
        ? `<img src="${f.poster}" alt="Poster de ${f.titulo}" class="cardPoster">`
        : '';

      card.innerHTML = `
        ${posterHtml} <h3>${f.titulo} <span class="anoFilme">(${f.ano})</span></h3>
        
        <p><strong>Duração:</strong> ${f.tempo_duracao}</p>
        <p><strong>Idioma:</strong> ${f.linguagem}</p>
      `;

      container.appendChild(card);
    });

  } catch (erro) {
    console.error("Erro ao carregar filmes:", erro);
    const container = document.getElementById("listaFilmes");
    container.innerHTML = `
      <article class="mensagemVazia">
        <p> Ocorreu um erro ao carregar os filmes!</p>
        <p>Tente atualizar a página.</p>
      </article>
    `;
  }
}

carregarFilmes();