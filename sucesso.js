async function carregarFilme() {
  const params = new URLSearchParams(window.location.search);
  const id = params.get("id_filme");
  if (!id) return;


  const posterContainer = document.getElementById("posterSucessoContainer");
  const posterImg = document.getElementById("posterFilme");

  try {
    const resposta = await fetch("/listar_filmes");
    const filmes = await resposta.json();
    const filme = filmes.find(f => f.id_filme == id);

    if (filme) {
      document.getElementById("titulo").textContent = filme.titulo;
      document.getElementById("ano").textContent = filme.ano;
      document.getElementById("duracao").textContent = filme.tempo_duracao;
      document.getElementById("linguagem").textContent = filme.linguagem;


      if (filme.poster) {
        posterImg.src = filme.poster;
        posterImg.alt = `Poster de ${filme.titulo}`;
      } else {
        posterContainer.style.display = "none";
      }

    } else {
      document.querySelector(".dadosFilme").innerHTML = `
        <p> Filme não encontrado.</p>
      `;
      posterContainer.style.display = "none";
    }
  } catch (erro) {
    console.error("Erro ao carregar filme:", erro);
    document.querySelector(".dadosFilme").innerHTML = `
      <p>Ocorreu um erro ao buscar o filme! Tente novamente.</p>
    `;
    posterContainer.style.display = "none"; 
  }
}

carregarFilme();