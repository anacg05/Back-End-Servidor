import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
import mysql.connector
import datetime
import decimal

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
            GROUP_CONCAT(DISTINCT l.linguagem SEPARATOR ', ') AS linguagem,
            GROUP_CONCAT(DISTINCT g.genero SEPARATOR ', ') AS genero,
            GROUP_CONCAT(DISTINCT p.produtora SEPARATOR ', ') AS produtora,
            GROUP_CONCAT(DISTINCT pa.pais SEPARATOR ', ') AS pais,
            GROUP_CONCAT(DISTINCT CONCAT(d.nome, ' ', d.sobrenome) SEPARATOR ', ') AS diretor,
            GROUP_CONCAT(DISTINCT CONCAT(a.nome, ' ', a.sobrenome) SEPARATOR ', ') AS atores
        FROM Filme f
        LEFT JOIN Linguagem l ON f.id_linguagem = l.id_linguagem
        LEFT JOIN Filme_Genero fg ON f.id_filme = fg.id_filme
        LEFT JOIN Genero g ON fg.id_genero = g.id_genero
        LEFT JOIN Filme_Produtora fp ON f.id_filme = fp.id_filme
        LEFT JOIN Produtora p ON fp.id_produtora = p.id_produtora
        LEFT JOIN Filme_Pais fp2 ON f.id_filme = fp2.id_filme
        LEFT JOIN Pais pa ON fp2.id_pais = pa.id_pais
        LEFT JOIN Filme_Diretor fd ON f.id_filme = fd.id_filme
        LEFT JOIN Diretor d ON fd.id_diretor = d.id_diretor
        LEFT JOIN Filme_Ator fa ON f.id_filme = fa.id_filme
        LEFT JOIN Ator a ON fa.id_ator = a.id_ator
        GROUP BY f.id_filme
        ORDER BY f.ano DESC;
    """)
    result = cursor.fetchall()
    return result

# 🔹 Classe do servidor
class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        # ✅ Rota de API (JSON)
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
                self.wfile.write(json.dumps(filmes, ensure_ascii=False, default=default_converter).encode('utf-8'))
            except Exception as e:
                self.send_error(500, f"Erro ao carregar filmes: {str(e)}")
            return

        # ✅ Roteamento das páginas HTML
        if self.path == "/" or self.path == "/index.html":
            arquivo = "index.html"
        elif self.path == "/cadastro":
            arquivo = "cadastro.html"
        elif self.path in ["/listarfilmes", "/listarfilmes.html"]:
            arquivo = "listarfilmes.html"
        elif self.path == "/login":
            arquivo = "login.html"
        else:
            arquivo = self.path.lstrip("/")

        # ✅ Servindo arquivos estáticos
        try:
            with open(arquivo, "rb") as f:
                if arquivo.endswith(".html"):
                    tipo = "text/html"
                elif arquivo.endswith(".css"):
                    tipo = "text/css"
                elif arquivo.endswith(".js"):
                    tipo = "application/javascript"
                else:
                    tipo = "application/octet-stream"

                self.send_response(200)
                self.send_header("Content-type", f"{tipo}; charset=utf-8")
                self.end_headers()
                self.wfile.write(f.read())

        except FileNotFoundError:
            self.send_error(404, f"Arquivo não encontrado: {arquivo}")

# 🔹 Função principal
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print("✅ Servidor rodando em http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
