import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from socket1 import wifi_ipv4_address
from playfair import playfair_alfabe_olustur, playfair_tablosu, metin_hazirla
from desifrele import playfair_decrypt, desifreli_metin_temizle
from server import key, playfair_encrypt

HOST = wifi_ipv4_address
PORT = 5050
FORMAT = 'utf-8'


KOYU_GRI = '#121212'
GRI = '#1F1B24'
MAVI = '#464EB8'
BEYAZ= "white"
FONT = ("Helvatica",17)
BUTON_FONT = ("Helvatica", 15)
KUCUK_FONT = ("Helvatica", 13)
kullanici = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def mesaj_ekle(mesaj):
    m_kutusu.config(state=tk.NORMAL)
    m_kutusu.insert(tk.END, mesaj + '\n')
    m_kutusu.config(state=tk.DISABLED)
    m_kutusu.see(tk.END)  # Automatically scroll to the bottom to show the latest message.

def baglan():
    try:
        kullanici.connect((HOST, PORT))
        print("Sunucuya başarılı bir şekilde bağlandı.")
        mesaj_ekle("[SERVER] Sunucuya başarılı bir şekilde bağlandı.")
    except:
        messagebox.showerror("Sunucuya bağlanılamıyor.",f"Sunucuya bağlanılamıyor {HOST} {PORT}")


    kullaniciadi = k_textbox.get()
    if kullaniciadi != '':
        kullanici.sendall(f"{kullaniciadi} ".encode())
    else:
        messagebox.showerror("Geçersiz kullanıcı adı","Kullanıcı adı boş olamaz")


    threading.Thread(target=serverden_mesaji_al, args=(kullanici,)).start()

    k_textbox.config(state=tk.DISABLED)
    k_buton.config(state=tk.DISABLED)
    
    m_textbox.bind("<Return>", lambda event: mesaj_gonder())

def mesaj_gonder(event=None):
    mesaj = m_textbox.get()
<<<<<<< HEAD
    if mesaj != '':
        kullanici.sendall(f"{mesaj} ".encode())
=======
    if mesaj.strip() != '':
        kullanici.sendall(mesaj.encode())
>>>>>>> 68ce8dd9bae6f292fcc7e6aa859c76dac71f3100
        m_textbox.delete(0, 'end')
    else:
        messagebox.showerror("Boş mesaj","Mesaj boş olamaz")



cerceve = tk.Tk()
cerceve.geometry("600x600")
cerceve.title("Mesajlaşma uygulaması")
cerceve.resizable(False, False)#Pencerenin boyunun oynatılamamasını sağlar.

cerceve.grid_rowconfigure(0, weight=1)
cerceve.grid_rowconfigure(1, weight=4)
cerceve.grid_rowconfigure(2, weight=1)

ust_kisim = tk.Frame(cerceve, width=600, height=100, bg=KOYU_GRI)
ust_kisim.grid(row=0, column=0, sticky=tk.NSEW)

orta_kisim = tk.Frame(cerceve, width=600, height=400, bg=GRI)
orta_kisim.grid(row=1, column=0, sticky=tk.NSEW)

alt_kisim = tk.Frame(cerceve, width=600, height=100, bg=KOYU_GRI)
alt_kisim.grid(row=2, column=0, sticky=tk.NSEW)

k_etiket = tk.Label(ust_kisim, text="Kullanici adi giriniz:", font=FONT, bg=KOYU_GRI, fg=BEYAZ)
k_etiket.pack(side=tk.LEFT, padx=10)

k_textbox=tk.Entry(ust_kisim, font=FONT, bg=GRI, fg=BEYAZ, width=23)
k_textbox.pack(side=tk.LEFT)

k_buton = tk.Button(ust_kisim, text="Giriş", font=BUTON_FONT, bg=MAVI, fg=BEYAZ, command=baglan)
k_buton.pack(side=tk.LEFT, padx=15)

m_textbox = tk.Entry(alt_kisim, font=FONT, bg=GRI, fg=BEYAZ, width=38)
m_textbox.pack(side=tk.LEFT, padx=10)

m_buton = tk.Button(alt_kisim, text="Gönder", font=BUTON_FONT, bg=MAVI, fg=BEYAZ, command=mesaj_gonder)
m_buton.pack(side=tk.LEFT, padx=10)

m_kutusu = scrolledtext.ScrolledText(orta_kisim, font=KUCUK_FONT, bg=GRI, fg=BEYAZ, width=67, height=26.5)
m_kutusu.config(state=tk.DISABLED)#Kullanıcının mesaj görüntüleme bölgesine yazmasını engeller.
m_kutusu.pack(side=tk.TOP)

  
playfair_alfabe = playfair_alfabe_olustur(key) # Must be the same key as the server
tablo = playfair_tablosu(playfair_alfabe)


def serverden_mesaji_al(kullanici):
    while 1:
        encrypted_data = kullanici.recv(2048).decode(FORMAT)
        if encrypted_data.strip():
            encrypted_username, encrypted_message = encrypted_data.split(' ', 1)
            username = playfair_decrypt(encrypted_username, tablo)
            message_content = playfair_decrypt(encrypted_message, tablo)
            temiz_username = desifreli_metin_temizle (username)
            temiz_metin = desifreli_metin_temizle(message_content)
            mesaj_ekle(f"[{temiz_username}] {' '} {temiz_metin}")
        else:
            messagebox.showerror("Error", "Received an empty message.")



def main():

    cerceve.mainloop()


if __name__ == '__main__':
    main()