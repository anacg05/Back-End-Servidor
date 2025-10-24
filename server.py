import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
import mysql.connector
import datetime
import decimal
from urllib.parse import parse_qs

# 🔹 Conexão com o banco MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senai",
    database="webserver_filmes_anacg"
)

# 🔹 Função para buscar os filmes no banco
def carregar_filmes():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("""
        SELECT 
            f.id_filme,
            f.titulo,
            f.tempo_duracao,
            f.ano,
            l.linguagem AS linguagem,
            f.id_linguagem,
            f.poster
        FROM Filme f
        LEFT JOIN Linguagem l ON f.id_linguagem = l.id_linguagem
        ORDER BY f.id_filme ASC;
    """)
    return cursor.fetchall()


# 🔹 Classe principal do servidor
class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/listar_filmes":
            try:
                filmes = carregar_filmes()
                def default_converter(obj):
                    if isinstance(obj, (datetime.date, datetime.datetime)):
                        return obj.isoformat()
                    if isinstance(obj, datetime.timedelta):
                        return str(obj)
                    if isinstance(obj, decimal.Decimal):
                        return float(obj)
                    return str(obj)
                self.send_response(200)
                self.send_header("Content-type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(filmes, ensure_ascii=False, default=default_converter).encode("utf-8"))
            except Exception as e:
                self.send_error(500, f"Erro ao carregar filmes: {str(e)}")
            return


        elif self.path == "/sucesso" or self.path.startswith("/sucesso?"):
            arquivo = "sucesso.html"

        elif self.path in ["/", "/index.html"]:
            arquivo = "index.html"
        elif self.path == "/cadastro":
            arquivo = "cadastro.html"
        elif self.path in ["/listarfilmes", "/listarfilmes.html"]:
            arquivo = "listarfilmes.html"
        elif self.path == "/login":
            arquivo = "login.html"
        else:
            arquivo = self.path.lstrip("/")

        try:
            with open(arquivo, "rb") as f:
                tipo = (
                    "text/html" if arquivo.endswith(".html") else
                    "text/css" if arquivo.endswith(".css") else
                    "application/javascript" if arquivo.endswith(".js") else
                    "application/octet-stream"
                )
                self.send_response(200)
                self.send_header("Content-type", f"{tipo}; charset=utf-8")
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_error(404, f"Arquivo não encontrado: {arquivo}")

    def do_POST(self):
        if self.path == "/cadastro":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_length).decode("utf-8")
                dados = parse_qs(post_data)

                titulo = dados.get("filme", [""])[0].strip()
                tempo = dados.get("tempo", ["02:00:00"])[0].strip()
                ano = dados.get("ano", [""])[0].strip()
                linguagem = dados.get("linguagem", ["1"])[0].strip()
                poster = dados.get("poster", [""])[0].strip() 

             
                if not titulo or not ano:
                    self.send_error(400, "Campos obrigatórios não preenchidos.")
                    return
                try:
                    ano_int = int(ano)
                except ValueError:
                    self.send_error(400, "Ano inválido.")
                    return

       
                cursor = mydb.cursor()
                cursor.execute("SELECT id_filme FROM Filme WHERE titulo = %s AND ano = %s", (titulo, ano_int))
                if cursor.fetchone():
                    self.send_error(409, f"O filme '{titulo}' ({ano_int}) já está cadastrado.")
                    return

             
                cursor.execute(
                    "INSERT INTO Filme (titulo, tempo_duracao, ano, id_linguagem, poster) VALUES (%s, %s, %s, %s, %s)",
                    (titulo, tempo, ano_int, linguagem, poster)
                )
                mydb.commit()
                id_filme = cursor.lastrowid

                self.send_response(303)
                self.send_header("Location", f"/sucesso?id_filme={id_filme}")
                self.end_headers()

            except Exception as e:
                self.send_error(500, f"Erro ao cadastrar filme: {str(e)}")
        else:
            self.send_error(404, f"Rota POST não encontrada: {self.path}")


# 🔹 Inicialização do servidor
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("✅ Servidor rodando em http://localhost:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    main()