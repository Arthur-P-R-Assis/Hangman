# Integrantes: Arthur Assis, Pamella Pio, Larissa Costa

import speech_recognition as sr
import pyttsx3
import smtplib
from email.mime.text import MIMEText
import random
import string
import sqlite3

def ouvir():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    with sr.Microphone() as source:
        print("\n\nFale 'Letra ... '")
        audio = r.listen(source, timeout = 10, phrase_time_limit = 3)

    try:
        text = r.recognize_google(audio, language='pt-BR')
        string = text.split(" ")
        letra = string[1]    

        return letra
    
    except sr.UnknownValueError:
        return 'nao entendi'

def falar(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  
    engine.setProperty('volume', 1.0)  
    engine.say(text)
    engine.runAndWait()

def gerar_senha():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres) for _ in range(5))
    return senha

#Nome para usar no email
def nome_jogador2(emaill):
        conexao = sqlite3.connect('src/jogo_forca.db')
        cursor = conexao.cursor()
        cursor.execute("""SELECT * FROM Jogador WHERE Email = ? """, (emaill,))
        verificar = cursor.fetchone()
        conexao.close()
        nome = verificar[1]
            
        return nome

def mudar_senha(senhaa,emaill):
        conexao = sqlite3.connect('src/jogo_forca.db')
        cursor = conexao.cursor()
        cursor.execute(f"UPDATE Jogador SET Senha = ? WHERE Email = ?", (senhaa, emaill))
        conexao.commit()
        conexao.close()

def mandar_email(emaill):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    email = 'arthurpaivaassis@gmail.com'
    senha = 'zutertciiazfvqqu'

    senhaa = gerar_senha()
    
    remetente = email
    destinatario = str(emaill)
    assunto = "Recuperação Senha"

    mensagem =  f"Oi {nome_jogador2(emaill)}, sua nova senha é {senhaa}."

    msg = MIMEText(mensagem)
    msg['Subject'] = assunto
    msg['From'] = remetente
    msg['To'] = destinatario
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email, senha)
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()
    
    except Exception as e:
         return print("Ocorreu um erro ao enviar o e-mail:", str(e))

    mudar_senha(senhaa,emaill)
    return print("Sua nova senha foi enviada para o seu email.\n")