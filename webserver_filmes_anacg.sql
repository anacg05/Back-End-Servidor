-- Criar o banco de dados

CREATE DATABASE webserver_filmes_anacg;

-- DROP DATABASE  webserver_filmes_anacg;

USE webserver_filmes_anacg;
 
-- Ator

CREATE TABLE Ator (
    id_ator INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    sobrenome VARCHAR(255),
    nacionalidade VARCHAR(255),
    genero ENUM('Masculino', 'Feminino', 'Outro', 'Não Informar') NOT NULL
);
 
-- Diretor

CREATE TABLE Diretor (
    id_diretor INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    sobrenome VARCHAR(255),
    nacionalidade VARCHAR(255),
    genero ENUM('Masculino', 'Feminino', 'Outro', 'Não Informar') NOT NULL
);
 
-- Produtora

CREATE TABLE Produtora (
    id_produtora INT AUTO_INCREMENT PRIMARY KEY,
    produtora VARCHAR(255) NOT NULL
);
 
-- País

CREATE TABLE Pais (
    id_pais INT AUTO_INCREMENT PRIMARY KEY,
    pais VARCHAR(255) NOT NULL

);
 
-- Linguagem

CREATE TABLE Linguagem (
    id_linguagem INT AUTO_INCREMENT PRIMARY KEY,
    linguagem VARCHAR(255) NOT NULL

);
 
-- Gênero

CREATE TABLE Genero (
    id_genero INT AUTO_INCREMENT PRIMARY KEY,
    genero VARCHAR(255) NOT NULL
);
 
-- Filme

CREATE TABLE Filme (
    id_filme INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    tempo_duracao TIME,
    ano YEAR,
    poster BLOB,
    id_linguagem INT,
    FOREIGN KEY (id_linguagem) REFERENCES Linguagem(id_linguagem)

);
 
-- TABELAS INTERMEDIARIAS

-- Filme_Ator

CREATE TABLE Filme_Ator (
    id_filme_ator INT AUTO_INCREMENT PRIMARY KEY,
    id_filme INT NOT NULL,
    id_ator INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES Filme(id_filme),
    FOREIGN KEY (id_ator) REFERENCES Ator(id_ator)
);
 
-- Filme_Diretor

CREATE TABLE Filme_Diretor (
    id_filme_diretor INT AUTO_INCREMENT PRIMARY KEY,
    id_filme INT NOT NULL,
    id_diretor INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES Filme(id_filme),
    FOREIGN KEY (id_diretor) REFERENCES Diretor(id_diretor)
);
 
-- Filme_Produtora

CREATE TABLE Filme_Produtora (
    id_filme_produtora INT AUTO_INCREMENT PRIMARY KEY,
    id_filme INT NOT NULL,
    id_produtora INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES Filme(id_filme),
    FOREIGN KEY (id_produtora) REFERENCES Produtora(id_produtora)
);
 
-- Filme_Pais

CREATE TABLE Filme_Pais (
    id_filme_pais INT AUTO_INCREMENT PRIMARY KEY,
    id_filme INT NOT NULL,
    id_pais INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES Filme(id_filme),
    FOREIGN KEY (id_pais) REFERENCES Pais(id_pais)
);
 
-- Filme_Genero 

CREATE TABLE Filme_Genero (
    id_filme_genero INT AUTO_INCREMENT PRIMARY KEY,
    id_filme INT NOT NULL,
    id_genero INT NOT NULL,
    FOREIGN KEY (id_filme) REFERENCES Filme(id_filme),
    FOREIGN KEY (id_genero) REFERENCES Genero(id_genero)
);
 
 
 INSERT INTO Linguagem (linguagem) VALUES
('Inglês'),
('Português'),
('Espanhol'),
('Francês'),
('Alemão'),
('Italiano'),
('Japonês'),
('Chinês'),
('Russo'),
('Árabe'),
('Coreano'),
('Hindi'),
('Bengali'),
('Holandês'),
('Sueco'),
('Polonês'),
('Turco'),
('Grego'),
('Tailandês'),
('Vietnamita');
 
 
INSERT INTO Filme (titulo, tempo_duracao, ano, id_linguagem) VALUES 
('The Matrix', '02:16:00', 1999, 1),
('O Rei Leão', '01:28:00', 1994, 1),
('Vingadores: Ultimato', '03:02:00', 2019, 1),
('Titanic', '03:14:00', 1997, 1),
('Tropa de Elite', '01:55:00', 2007, 2),
('O Segredo dos Seus Olhos', '02:09:00', 2009, 3),
('O Poderoso Chefão', '02:55:00', 1972, 6),
('A Intocáveis', '01:52:00', 2011, 4),
('A Lista de Schindler', '03:15:00', 1993, 5),
('O Homem que Vendeu sua Pele', '01:44:00', 2020, 8),
('O Hospedeiro', '02:05:00', 2006, 9),
('O Café da Manhã', '01:45:00', 2019, 10),
('Filme de Terror', '01:42:00', 2012, 19),
('Ida', '01:22:00', 2013, 16),
('A Caça', '01:55:00', 2012, 17),
('O Sol Enganador', '02:13:00', 1994, 11),
('Os Homens que Não Amavam as Mulheres', '02:32:00', 2009, 12),
('Milagre na Cela 7', '02:12:00', 2019, 14),
('3 Idiotas', '02:50:00', 2009, 13),
('A Viagem de Chihiro', '02:05:00', 2001, 7);

-- Inserir Ator
INSERT INTO Ator (nome, sobrenome, nacionalidade, genero) VALUES 
('Keanu', 'Reeves', 'Canadense', 'Masculino'),
('Matthew', 'Broderick', 'Americano', 'Masculino'),
('Robert', 'Downey', 'Americano', 'Masculino'),
('Leonardo', 'DiCaprio', 'Americano', 'Masculino'),
('Wagner', 'Moura', 'Brasileiro', 'Masculino'),
('Ricardo', 'Darín', 'Argentino', 'Masculino'),
('Marlon', 'Brando', 'Americano', 'Masculino'),
('Frances', 'McDormand', 'Americana', 'Feminino'),
('Emma', 'Stone', 'Americana', 'Feminino'),
('Marion', 'Cotillard', 'Francesa', 'Feminino'),
('Yalitza', 'Aparicio', 'Mexicana', 'Feminino'),
('Viola', 'Davis', 'Americana', 'Feminino'),
('Natalie', 'Portman', 'Americana', 'Feminino'),
('Jodie', 'Foster', 'Americana', 'Feminino'),
('Angelina', 'Jolie', 'Americana', 'Feminino'),
('Meryl', 'Streep', 'Americana', 'Feminino'),
('Tilda', 'Swinton', 'Britânica', 'Feminino'),
('Gong', 'Li', 'Chinesa', 'Feminino'),
('Emily', 'Blunt', 'Britânica', 'Feminino');

-- Inserir Diretor
INSERT INTO Diretor (nome, sobrenome, nacionalidade, genero) VALUES 
('Lana', 'Wachowski', 'Americana', 'Feminino'),
('Jon', 'Favreau', 'Americano', 'Masculino'),
('Anthony', 'Russo', 'Americano', 'Masculino'),
('James', 'Cameron', 'Canadense', 'Masculino'),
('José', 'Padilha', 'Brasileiro', 'Masculino'),
('Juan', 'José', 'Argentino', 'Masculino'),
('Francis', 'Ford Coppola', 'Americano', 'Masculino'),
('Olivier', 'Nakache', 'Francês', 'Masculino'),
('Steven', 'Spielberg', 'Americano', 'Masculino'),
('Park', 'Chan-wook', 'Sul-Coreano', 'Masculino'),
('Bong', 'Joon-ho', 'Sul-Coreano', 'Masculino'),
('Martin', 'Scorsese', 'Americano', 'Masculino'),
('Christopher', 'Nolan', 'Britânico', 'Masculino'),
('Alfonso', 'Cuarón', 'Mexicano', 'Masculino'),
('Pedro', 'Almodóvar', 'Espanhol', 'Masculino'),
('André', 'Øvredal', 'Norueguês', 'Masculino'),
('Wes', 'Anderson', 'Americano', 'Masculino'),
('Greta', 'Gerwig', 'Americana', 'Feminino'),
('Guillermo', 'del Toro', 'Mexicano', 'Masculino');

-- Inserir Produtora
INSERT INTO Produtora (produtora) VALUES 
('Warner Bros'),
('Disney'),
('Marvel Studios'),
('Paramount'),
('Columbia Pictures'),
('Fox Film'),
('Universal Pictures'),
('Metro-Goldwyn-Mayer'),
('Pixar'),
('Sony Pictures'),
('Legendary Entertainment'),
('A24'),
('Lionsgate'),
('New Line Cinema'),
('Amblin Entertainment'),
('Walt Disney Pictures'),
('New Regency'),
('Studio Ghibli'),
('Searchlight Pictures'),
('Blumhouse Productions');

-- Inserir País
INSERT INTO Pais (pais) VALUES 
('Estados Unidos'),
('Brasil'),
('Argentina'),
('Canadá'),
('França'),
('Reino Unido'),
('Alemanha'),
('Itália'),
('Japão'),
('China'),
('Rússia'),
('México'),
('Coreia do Sul'),
('Indústria Indiana'),
('Espanha'),
('Suécia'),
('Holanda'),
('Polônia'),
('Turquia'),
('Irã');

-- Inserir Gênero
INSERT INTO Genero (genero) VALUES 
('Ação'),
('Aventura'),
('Comédia'),
('Drama'),
('Terror'),
('Suspense'),
('Romance'),
('Ficção Científica'),
('Mistério'),
('Fantasia'),
('Animação'),
('Documentário'),
('Musical'),
('Thriller'),
('Crime'),
('Histórico'),
('Guerra'),
('Policial'),
('Família'),
('Biografia');

-- Inserir Filme_Ator
INSERT INTO Filme_Ator (id_filme, id_ator) VALUES
(1, 1), (1, 2), (2, 3), (2, 4), (3, 5), (3, 6), (4, 7), (4, 8), 
(5, 9), (6, 10), (7, 11), (8, 12), (9, 13), (10, 14), (11, 15), 
(12, 16), (13, 17), (14, 18), (15, 19), (16, 20);

-- Inserir Filme_Diretor
INSERT INTO Filme_Diretor (id_filme, id_diretor) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
(9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15),
(16, 16), (17, 17), (18, 18), (19, 19), (20, 20);

-- Inserir Filme_Produtora
INSERT INTO Filme_Produtora (id_filme, id_produtora) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
(9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15),
(16, 16), (17, 17), (18, 18), (19, 19), (20, 20);

-- Inserir Filme_Pais
INSERT INTO Filme_Pais (id_filme, id_pais) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
(9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15),
(16, 16), (17, 17), (18, 18), (19, 19), (20, 20);

-- Inserir Filme_Genero
INSERT INTO Filme_Genero (id_filme, id_genero) VALUES
(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8),
(9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15),
(16, 16), (17, 17), (18, 18), (19, 19), (20, 20);





