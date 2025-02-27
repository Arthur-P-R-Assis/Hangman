# Integrantes: Arthur Assis, Pamella Pio, Larissa Costa

import sqlite3
import random

#Classe para abrir o banco de dado e criar as tabelas.
class Banco:
    def __init__(self):
        self.conexao = sqlite3.connect('src/jogo_forca.db')
        self.cursor = self.conexao.cursor()

    def criar_tabela(self):
    
        #Administrador
        nome = "Arthur"
        email = 'arthurpaivaassis@gmail.com'
        login = "admin"
        senha = "admin"
        #=======================================#

        Admin = """
            CREATE TABLE Administrador (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL,
                Email TEXT NOT NULL,
                Login TEXT NOT NULL,
                Senha TEXT NOT NULL
        );
        """
        
        Jogador = """
            CREATE TABLE Jogador (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                Nome TEXT NOT NULL ,
                CPF varchar(15) NOT NULL ,
                Senha TEXT NOT NULL ,
                Email TEXT NOT NULL 
        );
        """

        Perguntas = """
        CREATE TABLE Perguntas (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            Codigo TEXT NOT NULL,
            Dica TEXT NOT NULL,
            Palavra TEXT NOT NULL,
            Tentativas TEXT NOT NULL
        );
        """
            
        self.cursor.execute(Admin)
        self.cursor.execute(Jogador)
        self.cursor.execute(Perguntas)
        self.cursor.execute(""" INSERT INTO Administrador(Nome, Email,Login, Senha) VALUES (?,?,?,?) """, (nome,email,login,senha))
        self.conexao.commit()
        self.conexao.close()


class Jogador:
    def __init__(self):
        self.conexao = sqlite3.connect('src/jogo_forca.db')
        self.cursor = self.conexao.cursor()

    def cadastro(self,nome = None ,cpf = None,senha = None,email = None): 
        self.cursor.execute("""SELECT CPF FROM Jogador WHERE CPF = ?""", (cpf,))
        verificar = self.cursor.fetchone()
        
        if not verificar:
            self.cursor.execute(""" INSERT INTO Jogador(Nome, CPF, Senha, Email) VALUES (?,?,?,?) """, (nome,cpf,senha,email))
            self.conexao.commit()
            self.conexao.close()
            return print("Cadastro feito com Sucesso! \n")
        
        else:
            self.conexao.close()
            return print("CPF já cadastrado.")
        
    def login(self,cpf,senha):
        self.cursor.execute("""SELECT CPF,Senha FROM Jogador WHERE CPF = ? AND Senha = ?""", (cpf,senha))
        verificar = self.cursor.fetchone()
        
        if verificar is not None:
            self.conexao.close()
            return 'login'
        
        else:
            self.conexao.close()
            return 'Login Inválido'
        
    def nome_jogador(self,cpf):
        self.cursor.execute("""SELECT * FROM Jogador WHERE CPF = ? """, (cpf,))
        verificar = self.cursor.fetchone()
        self.conexao.close()
        nome = verificar[1]
        
        return nome

    #Mostrar informações do jogador
    def ver_perfil(self,cpf):
        self.cursor.execute("""SELECT * FROM Jogador WHERE CPF = ? """, (cpf,))
        verificar = self.cursor.fetchone()
        self.conexao.close()
        return verificar
    
    def atualizar_Dados(self,tupla, nome , cpf, senha , email):
        atualizacoes = []
        parametros = [] 
        if len(nome) > 0:
            atualizacoes.append("Nome = ?")
            parametros.append(nome)
        
        if len(cpf) > 0:
            atualizacoes.append("CPF = ?")
            parametros.append(cpf)
        
        if len(senha) > 0:
            atualizacoes.append("Senha = ?")
            parametros.append(senha)
        
        if len(email) > 0:
            atualizacoes.append("Email = ?")
            parametros.append(email)

        
        if not atualizacoes:
            return print("Nenhuma alteração realizada. \n")
        
        atualizacao = ', '.join(atualizacoes)
        comando = f"UPDATE Jogador SET {atualizacao} WHERE CPF = ?"
        parametros.append(tupla[2])
        
        self.cursor.execute(comando, tuple(parametros))
        self.conexao.commit()
        self.conexao.close()

        if len(atualizacoes) > 0:
            return print("Dados Atualizados.")
    
class Admin:
    def __init__(self):
        self.conexao = sqlite3.connect('src/jogo_forca.db')
        self.cursor = self.conexao.cursor()
        
    def login_admin(self, login, senha):
        self.cursor.execute("""SELECT * FROM Administrador """)
        verificar = self.cursor.fetchone()
        if verificar[3] == login and verificar[4] == senha :
            self.conexao.close()
            return 'Login'
         
        else:
            self.conexao.close()
            return print("Login Inválido")
        
    def cadastrar_palavra(self, codigo ,dica,palavra,tentativas):
        self.cursor.execute("""SELECT Codigo FROM Perguntas WHERE Codigo = ?""", (codigo,))
        verificar = self.cursor.fetchone()
        
        if verificar is None:
            self.cursor.execute(""" INSERT INTO Perguntas(Codigo,Dica,Palavra, Tentativas) VALUES (?,?,?,?) """, (codigo,dica,palavra,tentativas))
            self.conexao.commit()
            self.conexao.close()
            return print("Palavra cadastrada com Sucesso! \n")
        
        else:
            self.conexao.close()
            return print("Codigo de Palavra já existente.")
    
    #Função para ver se a palavra ja foi cadstrada 
    def verificar_palavra(self,codigo):
        self.cursor.execute("""SELECT Codigo FROM Perguntas WHERE Codigo = ?""", (codigo,))
        verificar = self.cursor.fetchone()
        
        if verificar is not None:
            return 'existe'
        
        else:
            return print("Palavra não cadastrada.")
        
    def mostrar_palavra(self,codigo):
        self.cursor.execute(f"""SELECT * FROM Perguntas WHERE Codigo = ? """, (codigo,))
        verificar = self.cursor.fetchone()
        self.conexao.close()
        
        return print(f"Codigo: { verificar[1] }  Dica: { verificar[2]}  Palavra: {verificar[3]}  Tentativas: {verificar[4]} \n\n")  
    
    def atualizar_palavra(self,codigo , dica , palavra ,tentativas):
        atualizacoes = []
        parametros = [] 

        if len(dica) > 0:
            atualizacoes.append("Dica = ?")
            parametros.append(dica)
        
        if len(palavra) > 0:
            atualizacoes.append("Palavra = ?")
            parametros.append(palavra.upper())
        
        if len(tentativas) > 0:
            atualizacoes.append("Tentativas = ?")
            parametros.append(tentativas)
        
        if not atualizacoes:
            return print("Nenhuma alteração realizada. \n")
        
        atualizacao = ', '.join(atualizacoes)
        comando = f"UPDATE Perguntas SET {atualizacao} WHERE Codigo = ?"
        parametros.append(codigo)

        self.cursor.execute(comando, tuple(parametros))
        self.conexao.commit()
        self.conexao.close()

        if len(atualizacoes) > 0:
            return print("Palavra Atualizada.")
    
    def remover_palavra(self,codigo):
        if self.verificar_palavra(codigo) == 'existe':
            self.cursor.execute("""DELETE FROM Perguntas WHERE Codigo = ? """, (codigo,))
            self.conexao.commit()
            self.conexao.close()
            return print("Palavra excluida com sucesso! \n")
        
        else:
            self.conexao.close()
            return print("Código não existente.")
        
    def listar_palavras(self):
        self.cursor.execute("""SELECT COUNT(*) FROM Perguntas""")
        resultado = self.cursor.fetchone()
        numero_linhas = resultado[0]
        print(f"Numero total de Palavras: {numero_linhas}\n")
        self.cursor.execute("SELECT * FROM Perguntas")
        resultados = self.cursor.fetchall()
        self.conexao.close()
        
        for verificar in resultados:
            codigo = verificar[1]
            dica = verificar[2]
            palavra = verificar[3]
            tentativas = verificar[4]
            print(f"Codigo: { codigo }  Dica: { dica }  Palavra: {palavra}  Tentativas: {tentativas} \n") 
    
    #Função para pegar todas as linhas de perguntas
    def pegar_tuplas(self):
        self.cursor.execute("""SELECT * FROM Perguntas""")
        resultado = self.cursor.fetchall()
        self.conexao.close()

        return resultado

    def exportar_csv(self):
        lista =  self.pegar_tuplas()
        with open('CsV', 'w') as arquivo_csv:
            arquivo_csv.write('Codigo;  Dica;  Palavra;  Tentativas\n')  
            
            for tupla in lista:
                linha = f"{tupla[1]};  {tupla[2]};  {tupla[3]};  {tupla[4]}\n" 
                arquivo_csv.write(linha)  
        
        return print(f"Dados exportados para o arquivo CSV com sucesso!")
                
class Pergunta:
    def __init__(self):
        self.conexao = sqlite3.connect('src/jogo_forca.db')
        self.cursor = self.conexao.cursor()
        
    def pergunta_aleatoria(self):
        self.cursor.execute("""SELECT * FROM Perguntas""")
        lista = self.cursor.fetchall()
        self.conexao.close()
        elemento_aleatorio = random.choice(lista)
        return elemento_aleatorio
    
    #Fazer a palavra em versão _
    def mostrar_(self,tupla):
        palavra = ''

        for i in tupla[3]:
            if i == ' ':
                palavra += palavra.join(" ")

            else:
                palavra += palavra.join("_")
            
        return palavra
    
    #pegar a palavra feita de _ e ir trocando conforme os acertos
    def mudar_(self,text,tupla,palavra):
        word = tupla[3]
        x = 0
        for i in range (len(word)):
            if word[i].upper() == text.upper():
                palavra = palavra[:i] + text + palavra[i + 1:]
                x += 1

        if x == 0:
            return 'perdeu'
        
        else:
            return palavra
    
    #Quando nao tiver mais _, vc ganha
    def vitoria(self,palavra):
        contador = 0
        for i in palavra:
            if i == '_':
                contador +=1
                
        if contador == 0:
            return 'vitoria'  