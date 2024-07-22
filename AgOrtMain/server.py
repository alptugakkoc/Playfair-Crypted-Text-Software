import socket
import threading
from playfair import playfair_alfabe_olustur, playfair_tablosu, key
from sifrele import playfair_encrypt
from socket1 import wifi_ipv4_address
FORMAT='utf-8'
HOST = wifi_ipv4_address
PORT = 5050
KULLANICI_LIMITI = 5
aktif_kullanicilar = []

playfair_alfabe = playfair_alfabe_olustur(key)
tablo = playfair_tablosu(playfair_alfabe)

def mesajlari_al(kullanici, kullanici_adi):

    while 1:
        mesaj = kullanici.recv(2048).decode(FORMAT)
        if mesaj.strip():

            final_msj = f"{kullanici_adi} {mesaj.strip()}"
            send_messages_to_all(final_msj)
        else:
            print(f"{kullanici_adi} gönderdiği mesaj boş. ")

def kullaniciya_mesaj_gonder(kullanici, mesaj):

    kullanici.sendall(mesaj.encode())

def send_messages_to_all(full_message):
    if ' ' in full_message:
        username, mesaj = full_message.split(' ', 1)
        encrypted_username = playfair_encrypt(username, tablo)
        encrypted_message = playfair_encrypt(mesaj.strip(), tablo)
        final_message = f"{encrypted_username} {encrypted_message}"
    else:
        # If there is no ' ', encrypt the entire message assuming it's a system message
        final_message = playfair_encrypt(full_message, tablo)

    for _, kullanici_socket in aktif_kullanicilar:
        kullaniciya_mesaj_gonder(kullanici_socket, final_message)




def k_isleyici(kullanici):

    while 1:
        kullaniciadi = kullanici.recv(2048).decode('utf-8')
        if kullaniciadi != '':
            aktif_kullanicilar.append((kullaniciadi, kullanici))
            bilgi_mesaji = f"SERVER {kullaniciadi} sohbete katıldı."
            send_messages_to_all(bilgi_mesaji)
            break
        else:
            print("Kullanici adi boş")


    threading.Thread(target=mesajlari_al, args=(kullanici, kullaniciadi,)).start()

def main():

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        server.bind((HOST,PORT))
        print(f"Server bu konumda çalışıyor {HOST} {PORT}")
    except:
        print(f"{HOST} ana bilgisayarına ve {PORT} bağlantı noktasına bağlanılamıyor")

    server.listen(KULLANICI_LIMITI)

    while 1:

        kullanici, adres = server.accept()
        print(f"{adres[0]} {adres[1]} istemcisine başarıyla bağlanıldı")

        threading.Thread(target = k_isleyici, args=(kullanici, )).start()

if __name__ == '__main__':
    main()