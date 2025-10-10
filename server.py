import os
import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import mysql.connector  # pip install mysql-connector-python

# Conectar ao banco de dados
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="senai",
    database="webserver_filmes_anacg"  # Adicionando o nome do banco de dados
)

# Função auxiliar para carregar filmes do banco de dados
def carregar_filmes():
    cursor = mydb.cursor(dictionary=True)  # Usar dictionary=True para retornar como dicionários
    cursor.execute("SELECT * FROM Filme")
    result = cursor.fetchall()
    return result

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
    
    # Rota GET para retornar filmes do banco de dados como JSON
    def do_GET(self):
        if self.path == "/listar_filmes":
            filmes = carregar_filmes()  # Puxa filmes do banco de dados
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(filmes, ensure_ascii=False).encode('utf-8'))  # Retorna os filmes em formato JSON
        else:
            super().do_GET()

# Função principal para rodar o servidor
def main():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandle)
    print("Server Running in http://localhost:8000")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
