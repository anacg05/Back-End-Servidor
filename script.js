// Carrega e exibe os filmes
async function carregarFilmes() {
  try {
    const resposta = await fetch("/filmes.json");
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

    filmes.forEach((f, index) => {
      const card = document.createElement("div");
      card.classList.add("cardFilme");

      card.innerHTML = `
        <h3>${f.filme} <span class="anoFilme">(${f.ano})</span></h3>
        <p><strong>Diretor:</strong> ${f.diretor}</p>
        <p><strong>Gênero:</strong> ${f.genero}</p>
        <p><strong>Produtora:</strong> ${f.produtora}</p>
        <p><strong>Atores:</strong> ${f.atores}</p>
        <p><strong>Sinopse:</strong> ${f.sinopse}</p>
        <div class="acoesCard">
          <button class="botaoPequeno" onclick="editarFilme(${index})">Editar</button>
          <button class="botaoPequeno" onclick="deletarFilme(${index})">Excluir</button>
        </div>
      `;

      container.appendChild(card);
    });
  } catch (erro) {
    console.error("Erro ao carregar filmes:", erro);
  }
}

// Função para excluir filme
async function deletarFilme(index) {
  if (!confirm("Tem certeza que deseja excluir este filme?")) return;

  const resposta = await fetch("/delete", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: `index=${index}`
  });

  alert(await resposta.text());
  carregarFilmes();
}

// Função para editar filme
async function editarFilme(index) {
  const resposta = await fetch("/filmes.json");
  const filmes = await resposta.json();
  const filme = filmes[index];

  // cria um prompt rápido para edição (pode ser melhorado com modal/form)
  const novoFilme = prompt("Nome do filme:", filme.filme) || filme.filme;
  const novosAtores = prompt("Atores:", filme.atores) || filme.atores;
  const novoDiretor = prompt("Diretor:", filme.diretor) || filme.diretor;
  const novoAno = prompt("Ano:", filme.ano) || filme.ano;
  const novoGenero = prompt("Gênero:", filme.genero) || filme.genero;
  const novaProdutora = prompt("Produtora:", filme.produtora) || filme.produtora;
  const novaSinopse = prompt("Sinopse:", filme.sinopse) || filme.sinopse;

  const params = new URLSearchParams({
    index,
    filme: novoFilme,
    atores: novosAtores,
    diretor: novoDiretor,
    ano: novoAno,
    genero: novoGenero,
    produtora: novaProdutora,
    sinopse: novaSinopse
  });

  const resp = await fetch("/edit", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: params.toString()
  });

  alert(await resp.text());
  carregarFilmes();
}

// Carrega os filmes ao abrir a página
carregarFilmes();
