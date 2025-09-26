import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# Caminho absoluto do arquivo JSON (sempre na mesma pasta do server.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_JSON = os.path.join(BASE_DIR, "filmes.json")

# Função auxiliar para carregar filmes do JSON
def carregar_filmes():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []


# Função auxiliar para salvar filmes no JSON
def salvar_filmes(filmes):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(filmes, f, ensure_ascii=False, indent=4)


# Classe do servidor
class MyHandle(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            f = open(os.path.join(path, 'index.html'), encoding='utf-8')
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            f.close()
            return None
        except FileNotFoundError:
            pass
        return super().list_directory(path)

    def account_user(self, login, password):
        loga = "anacg"
        senha = 12345

        if login == loga and senha == password:
            return "Usuário Logado"
        else:
            return "Usuário não existe"

    # Rotas GET
    def do_GET(self):
        if self.path == "/login":
            self.serve_html("login.html")
        elif self.path == "/cadastro":
            self.serve_html("cadastro.html")
        elif self.path == "/listarfilmes":
            self.serve_filmes()
        else:
            super().do_GET()

    def serve_html(self, filename):
        try:
            with open(os.path.join(os.getcwd(), filename), encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "File Not Found")

    def serve_filmes(self):
        filmes = carregar_filmes()
        print(filmes)
        html = """
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>Filmes Cadastrados</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <header>
                <h1>Filmes</h1>
            </header>
            <main>
                <section class="containerPrincipalCadastro">
                    <h2>Filmes Cadastrados</h2>
        """

        if filmes:
            html += '<div class="listaFilmes">'
            for f in filmes:
                html += f"""
                <div class="cardFilme">
                    <h3>{f['filme']} <span class="anoFilme">({f['ano']})</span></h3>
                    <p><strong>Diretor:</strong> {f['diretor']}</p>
                    <p><strong>Gênero:</strong> {f['genero']}</p>
                    <p><strong>Produtora:</strong> {f['produtora']}</p>
                    <p><strong>Atores:</strong> {f['atores']}</p>
                    <p><strong>Sinopse:</strong> {f['sinopse']}</p>
                </div>
                """
            html += "</div>"  # fecha listaFilmes
        else:
            html += """
            <article class="mensagemVazia">
                <p>Não há filmes cadastrados no momento.</p>
                <p>Comece adicionando seu primeiro filme ao sistema!</p>
            </article>
            """

        html += """
                    <nav class="navegacao">
                        <a href="/cadastro" class="botaoSecundario">Cadastrar Novo Filme</a>
                        <a href="/" class="botaoSecundario">Voltar à Página Inicial</a>
                    </nav>
                </section>
            </main>
            <footer>
                <p>&copy; 2025 Filmes - Sistema de Gerenciamento de Filmes</p>
                <p>Criado por Ana Clara Grizotto</p>
            </footer>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))


    # Rotas POST
    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            login = form_data.get('usuario', [""])[0]
            password = int(form_data.get('senha', ["0"])[0])
            logou = self.account_user(login, password)

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(logou.encode('utf-8'))

        elif self.path == '/cadastro':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            # Captura dos dados
            filme = form_data.get('filme', [""])[0]
            atores = form_data.get('atores', [""])[0]
            diretor = form_data.get('diretor', [""])[0]
            ano = form_data.get('ano', [""])[0]
            genero = form_data.get('genero', [""])[0]
            produtora = form_data.get('produtora', [""])[0]
            sinopse = form_data.get('sinopse', [""])[0]

            # Carregar filmes existentes e adicionar novo
            filmes = carregar_filmes()
            filmes.append({
                "filme": filme,
                "atores": atores,
                "diretor": diretor,
                "ano": ano,
                "genero": genero,
                "produtora": produtora,
                "sinopse": sinopse
            })
            salvar_filmes(filmes)

            # Resposta ao usuário
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("Filme cadastrado com sucesso!".encode('utf-8'))

        else:
            super(MyHandle, self).do_POST()


# Função principal para rodar o servidor
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server Running in http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
