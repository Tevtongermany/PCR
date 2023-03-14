import socket
import threading
import os
import configparser
import tkinter
import customtkinter
import string

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
settingsfilename = "config.ini"
if os.path.exists(settingsfilename): # check if config file
    config = configparser.ConfigParser()
    config.read(settingsfilename)
    Username = config.get('Settings', 'Username')
else: # config file doesn't exit creating one
    config = configparser.ConfigParser()
    config['Settings'] = {'Username': 'user1'}
    with open(settingsfilename, 'w') as f:
        config.write(f)



client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
class Chatroom(customtkinter.CTkToplevel):
    def __init__(self,host,port):
        super().__init__()
        self.geometry("300x200")
        self.title("Chat PCR")
        print(host,port)
        client_socket.connect((str(host), int(port)))
        rec = threading.Thread(target=self.recieve).start()
        self.Chat = customtkinter.CTkTextbox(master=self, width=200,height=100, corner_radius=0)
        self.Chat.place(relx=0.5, rely=0.3,anchor=tkinter.CENTER)
        self.input = customtkinter.CTkEntry(master=self,width=200)
        self.input.place(relx=0.5, rely=0.9,anchor=tkinter.CENTER)
        self.sendmessage = customtkinter.CTkButton(master=self,text=">>>",width=10,command=self.send)
        self.sendmessage.place(relx=0.9, rely=0.9,anchor=tkinter.CENTER)

    def insertmessage(self,text):
        self.Chat.insert(0.0,f"{text}\n")

    def send(self):
        rawinput = self.input.get()
        message = f"{str(Username)}> {rawinput}"
        self.Chat.insert("0.0",f"{message}\n")
        client_socket.send(message.encode())

    def recieve(self):
        while True:
            try:
                message = client_socket.recv(1024).decode()
                print(message)
                self.insertmessage(message)
            except:
                client_socket.close()






class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Window Settings
        self.geometry("300x150")
        self.title("Login PCR")
        self.resizable(False, False)

        self.name =customtkinter.CTkEntry(master=self,width=200,placeholder_text="Username")  # User name
        self.name.place(relx=0.5, rely=0.3,anchor=tkinter.CENTER)
        self.password =customtkinter.CTkEntry(master=self,width=200,placeholder_text="password")  # password
        self.password .place(relx=0.5, rely=0.7,anchor=tkinter.CENTER)

        self.ServerAdress =customtkinter.CTkEntry(master=self,width=150,placeholder_text="Server Adress")  # ServerAdress
        self.ServerAdress.place(relx=0.415, rely=0.5,anchor=tkinter.CENTER)
        self.ServerPort =customtkinter.CTkEntry(master=self,width=45,placeholder_text="Port")  # ServerAdress
        self.ServerPort.place(relx=0.75, rely=0.5,anchor=tkinter.CENTER)

        self.joinbutton = customtkinter.CTkButton(master=self,text=">>>",width=10,command=self.open_chatwindow) # Join Button
        self.joinbutton.place(relx=0.9, rely=0.3,anchor=tkinter.CENTER)

        self.chatwindow = None

    def open_chatwindow(self):
        if self.chatwindow is None or not self.chatwindow.winfo_exists():
            host = self.ServerAdress.get()
            port = self.ServerPort.get()
            self.chatwindow = Chatroom(port=port,host=host)  # create window if its None or destroyed
        else:
            self.chatwindow.focus() 
    def on_closed():
        print("")


if __name__ == "__main__":
    app = App()
    app.mainloop()





