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
        """Sempre abre o index.html como página inicial"""
        try:
            with open(os.path.join(path, 'index.html'), encoding='utf-8') as f:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f.read().encode('utf-8'))
                return None
        except FileNotFoundError:
            pass
        return super().list_directory(path)

    def account_user(self, login, password):
        loga = "anacg"
        senha = 12345
        return "Usuário Logado" if login == loga and senha == password else "Usuário não existe"

    # Rotas GET
    def do_GET(self):
        if self.path == "/login":
            self.serve_html("login.html")
        elif self.path == "/cadastro":
            self.serve_html("cadastro.html")
        elif self.path == "/listarfilmes":
            self.serve_html("listar_filmes.html")
        else:
            super().do_GET()

    def serve_html(self, filename):
        try:
            with open(os.path.join(os.getcwd(), filename), encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except FileNotFoundError:
            self.send_error(404, "File Not Found")

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

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write("Filme cadastrado com sucesso!".encode('utf-8'))

        elif self.path == '/delete':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            index = int(form_data.get('index', [-1])[0])
            filmes = carregar_filmes()

            if 0 <= index < len(filmes):
                removido = filmes.pop(index)
                salvar_filmes(filmes)
                resposta = f"Filme '{removido['filme']}' deletado com sucesso!"
            else:
                resposta = "Filme não encontrado."

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(resposta.encode('utf-8'))

        elif self.path == '/edit':
            content_length = int(self.headers['Content-length'])
            body = self.rfile.read(content_length).decode('utf-8')
            form_data = parse_qs(body)

            index = int(form_data.get('index', [-1])[0])
            filmes = carregar_filmes()

            if 0 <= index < len(filmes):
                filmes[index] = {
                    "filme": form_data.get('filme', [""])[0],
                    "atores": form_data.get('atores', [""])[0],
                    "diretor": form_data.get('diretor', [""])[0],
                    "ano": form_data.get('ano', [""])[0],
                    "genero": form_data.get('genero', [""])[0],
                    "produtora": form_data.get('produtora', [""])[0],
                    "sinopse": form_data.get('sinopse', [""])[0]
                }
                salvar_filmes(filmes)
                resposta = "Filme editado com sucesso!"
            else:
                resposta = "Filme não encontrado."

            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(resposta.encode('utf-8'))

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
