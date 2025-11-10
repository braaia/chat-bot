import os, threading
from tkinter import *
from dotenv import load_dotenv
from tkinter import scrolledtext
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

load_dotenv()
api_key = os.getenv('api_key')
os.environ['GROQ_API_KEY'] = api_key

chat = ChatGroq(model='llama-3.3-70b-versatile')
msgs = []

def bot_answer(msgs):
    model_msgs = [('')]
    model_msgs += msgs

    template = ChatPromptTemplate.from_messages(model_msgs)
    chain = template | chat
    return chain.invoke({}).content

# Função para processar a entrada do usuário
def send_message(event=None):  # Permite chamar a função pelo botão ou pela tecla Enter
    question = user_input.get()
    if question.strip():  # Verifica se a entrada não está vazia
        chat_box.insert(END, f"\nBraia: {question}\n", "user")
        msgs.append(('user', question))
        
        def get_response():
            answer = bot_answer(msgs)
            msgs.append(('assistant', answer))
            chat_box.insert(END, f"\nBot: {answer}\n", "bot")
            chat_box.yview(END)  # Scroll para a última mensagem
        
        threading.Thread(target=get_response, daemon=True).start()
    
    user_input.delete(0, END)  # Limpa a entrada do usuário

# Criar janela principal
root = Tk()
root.title("MonkeyBot")
root.geometry("1280x720")

# Criar área de texto rolável
chat_box = scrolledtext.ScrolledText(root, wrap=WORD, width=110, height=26, font=("JetBrains Mono", 12))
chat_box.pack(pady=10)
chat_box.tag_config("user", foreground="purple", font=("JetBrains Mono", 12))
chat_box.tag_config("bot", foreground="black", font=("JetBrains Mono", 12))

# Campo de entrada de texto
user_input = Entry(root, width=50, font=("JetBrains Mono", 12))
user_input.pack(pady=5)
user_input.bind("<Return>", send_message)  # Vincula Enter ao envio

# Vincular a tecla ESC para fechar a janela
root.bind("<Escape>", lambda event: root.destroy())

# Botão de envio
send_button = Button(root, text="Enviar", font=("JetBrains Mono", 12, "bold"), command=send_message)
send_button.pack()

# Rodar a janela
root.mainloop()
