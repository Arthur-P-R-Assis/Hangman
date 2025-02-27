# Integrantes: Arthur Assis, Pamella Pio, Larissa Costa

from classes import Jogador,Admin,Pergunta,Banco
import bibliotecas
import os


if __name__ == '__main__':
  
  while True:
    print("\n\n--------------- Menu Principal ---------------\n")
    print("    1 - Jogar\n")
    print("    2 - Cadastrar Novo Jogador\n")
    print("    3 - Recuperar Senha\n")
    print("    4 - Entrar como Administrador\n")
    print("    5 - Sair \n\n")
    print("  Digite sua opção:\n")

    if not os.path.exists('src/jogo_forca.db'):
      banco = Banco()
      banco.criar_tabela()

    resposta = input()

    if resposta == '1':
      print('------ Login ------\n')
      cpf = input("Cpf: \n")
      senha = input("Senha: \n")

      cpf_salvar = cpf
      jogador = Jogador()
      login = jogador.login(cpf,senha)
     
      if login == 'login':
        while True:
          jogador = Jogador()
          print(f"\n\n--------------- Menu Jogo da Forca - {jogador.nome_jogador(cpf)} ---------------\n")
          print("    1 - Jogar\n")
          print("    2 - Atualizar Dados\n")
          print("    3 - Voltar ao Menu Principal\n\n")
          print("  Digite sua opção:\n")
          jogador = Jogador()
          bibliotecas.falar(f"Bem-Vindo{jogador.nome_jogador(cpf)}")
          resposta_jogar = input()

          if resposta_jogar == '1':
            pergunta = Pergunta()
            tupla = pergunta.pergunta_aleatoria()
            palavra = pergunta.mostrar_(tupla)
            tentativas = int(tupla[4])
              
            while True:
              print("\n\n--------------- Jogo Da Forca ---------------\n")
              print(f'Dica:{tupla[2]} \n')
              print(f"Palavra: {palavra}")
              print(f"Tentativas: {tentativas} de {tupla[4]}")
              text = bibliotecas.ouvir()
              print(text)

              if text == 'nao entendi':
                tentativas +=1
                print("Não entendi, repita por favor.\n")
                
              pergunta = Pergunta()
              resposta = pergunta.mudar_(text,tupla,palavra)
              if resposta == 'perdeu':
                tentativas -= 1
              else:
                palavra = resposta

              pergunta = Pergunta()
              vitoria = pergunta.vitoria(palavra)

              if vitoria == 'vitoria':
                print("Parabéns você acertou.")
                break

              if tentativas == 0:
                print("Você Perdeu. \n")
                break

          elif resposta_jogar == '2':
            jogador = Jogador()
            tupla = jogador.ver_perfil(cpf)
            print(f"Nome = {tupla[1]}  CPF = {tupla[2]} Senha = {tupla[3]}  Email: {tupla[4]}")
            nome = input("Nome: \n")
            cpf = input("Cpf: \n")
            senha = input("Senha: \n")
            email = input("Email: \n")
            if len(cpf) == 0:
              cpf = cpf_salvar

            jogador = Jogador()
            jogador.atualizar_Dados(tupla, nome,cpf,senha,email)


          elif resposta_jogar == '3':
            break

          else:
            print("Opção Inválida.")

      else:
          print('Login Inválido')

    elif resposta == '2':
      print("\n\n--------------- Cadastro ---------------\n")
      cpf = input("Informe seu CPF: \n")
      nome = input("Nome: \n")
      email = input("Email: \n")
      senha = input("Senha: \n")
      jogador = Jogador()
      jogador.cadastro(nome,cpf,senha,email)
      

    elif resposta == '3':
      print("\n\n--------------- Recuperar Senha ---------------\n")
      emaill = input("Email: \n")
      bibliotecas.mandar_email(emaill)
      

    elif resposta == '4':
      login = input("Login: \n")
      senha = input("Senha: \n")
      admin = Admin()

      if  admin.login_admin(login, senha) == 'Login':
        while True:
          print(f"\n\n--------------- Menu Administrador ---------------\n")
          print("    1 - Cadastrar Nova Pergunta \n")
          print("    2 - Atualizar Pergunta \n")
          print("    3 - Remover Pergunta \n")
          print("    4 - Listar Perguntas \n")
          print("    5 - Voltar ao Menu Principal \n")
          print("  Digite sua opção:\n")
          
          resposta_admin = input()
          
          if resposta_admin == '1':
            codigo = input("Codigo: \n")
            dica = input("Dica: \n")
            palavra = input("Palavra: \n")
            tentativas = input("Nº de Tentativas: \n") 
            admin = Admin() 
            admin.cadastrar_palavra(codigo,dica,palavra,tentativas)
            
          elif resposta_admin == '2':
            codigo = input("Codigo: \n")
            admin = Admin()
            if admin.verificar_palavra(codigo) == 'existe':
              admin.conexao.close()
              print(f"\n\n-------------- Atualizar ---------------\n")
              admin = Admin()
              admin.mostrar_palavra(codigo)
              dica = input("Dica: \n")
              palavra = input("Palavra: \n")
              tentativas = input("Nº de Tentativas: \n")
              admin = Admin()
              admin.atualizar_palavra(codigo, dica,palavra,tentativas)

          elif resposta_admin == '3':
            codigo = input("Codigo: \n")
            admin = Admin()
            admin.remover_palavra(codigo)

          elif resposta_admin == '4':
            print(f"\n\n-------------- Lista de Perguntas ---------------\n")
            admin = Admin()
            admin.listar_palavras()
            csv = input("Deseja exportar os dados das perguntas em formato Comma-Separated Values CSV ?")
            if csv == "sim":
               admin = Admin()
               admin.exportar_csv()

          elif resposta_admin == '5':
            break        

          else:
            print("Opção Inválida. \n")
      
    elif resposta == '5':
      print("Saindo...")
      break
    
    else:
      print("Opção Inválida.")