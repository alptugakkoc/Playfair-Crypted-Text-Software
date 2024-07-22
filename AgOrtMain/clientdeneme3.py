import socket
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QScrollArea, QVBoxLayout, QWidget
from socket1 import wifi_ipv4_address
from playfair import playfair_alfabe_olustur, playfair_tablosu
from desifrele import playfair_decrypt, desifreli_metin_temizle
from server import key


HOST = ""
PORT = 5050
FORMAT = 'utf-8'


class ChatClient(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.kullanici = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.uzunluk = 0  # Başlangıçta uzunluk sıfır olacak
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 600, 600)
        self.setWindowTitle('Mesajlaşma Uygulaması')
        self.setFixedSize(600, 600)
        self.setStyleSheet("""
            QWidget {
                background-color: #121212;
                color: white;
                font-size: 16px;
            }
            QLineEdit, QTextEdit {
                background-color: #1F1B24;
                border: 1px solid #464EB8;
                padding: 10px;
                color: white;
            }
            QPushButton {
                background-color: #464EB8;
                border: 1px solid #5a5fcf;
                padding: 10px;
                font-size: 15px;
                color: white;
            }
            QPushButton:hover {
                background-color: #5a5fcf;
            }
            QLabel {
                font-size: 17px;
                color: white;
            }
            QScrollArea {
                background-color: #1F1B24;
            }
        """)

        layout = QtWidgets.QVBoxLayout()

        self.ust_kisim = QtWidgets.QFrame(self)
        self.ust_kisim.setFixedHeight(100)

        hbox = QtWidgets.QHBoxLayout(self.ust_kisim)
        self.k_etiket = QtWidgets.QLabel('Kullanıcı Adı Giriniz:', self.ust_kisim)
        hbox.addWidget(self.k_etiket)

        self.k_textbox = QtWidgets.QLineEdit(self.ust_kisim)
        hbox.addWidget(self.k_textbox)

        self.k_buton = QtWidgets.QPushButton('Giriş', self.ust_kisim)
        self.k_buton.clicked.connect(self.baglan)
        hbox.addWidget(self.k_buton)

        layout.addWidget(self.ust_kisim)

        self.orta_kisim = QScrollArea(self)
        self.orta_kisim.setWidgetResizable(True)

        self.m_kutusu = QtWidgets.QTextEdit(self.orta_kisim)
        self.m_kutusu.setReadOnly(True)

        self.scroll_area_widget_contents = QWidget()
        self.orta_kisim.setWidget(self.scroll_area_widget_contents)
        self.scroll_area_layout = QVBoxLayout(self.scroll_area_widget_contents)
        self.scroll_area_layout.addWidget(self.m_kutusu)

        layout.addWidget(self.orta_kisim)

        self.alt_kisim = QtWidgets.QFrame(self)
        self.alt_kisim.setFixedHeight(100)

        hbox2 = QtWidgets.QHBoxLayout(self.alt_kisim)
        self.m_textbox = QtWidgets.QLineEdit(self.alt_kisim)
        hbox2.addWidget(self.m_textbox)

        self.m_buton = QtWidgets.QPushButton('Gönder', self.alt_kisim)
        self.m_buton.clicked.connect(self.mesaj_gonder)
        hbox2.addWidget(self.m_buton)

        layout.addWidget(self.alt_kisim)

        self.setLayout(layout)

    def mesaj_ekle(self, mesaj):
        self.m_kutusu.append(mesaj)

    def baglan(self):
        try:
            self.kullanici.connect((HOST, PORT))
            self.mesaj_ekle("[SERVER] Sunucuya başarılı bir şekilde bağlandı.")
        except:
            QMessageBox.critical(self, "Sunucuya bağlanılamıyor.", f"Sunucuya bağlanılamıyor {HOST} {PORT}")

        kullaniciadi = self.k_textbox.text()
        if kullaniciadi != '':
            self.kullanici.sendall(f"{kullaniciadi} ".encode())
        else:
            QMessageBox.critical(self, "Geçersiz kullanıcı adı", "Kullanıcı adı boş olamaz")

        threading.Thread(target=self.serverden_mesaji_al, args=(self.kullanici,)).start()

        self.k_textbox.setDisabled(True)
        self.k_buton.setDisabled(True)

        self.m_textbox.returnPressed.connect(self.mesaj_gonder)

    def mesaj_gonder(self):
        mesaj = self.m_textbox.text()

        if mesaj != '':
            self.kullanici.sendall(f"{mesaj} ".encode())
            self.m_textbox.clear()
        else:
            QMessageBox.critical(self, "Boş mesaj", "Mesaj boş olamaz")

    def serverden_mesaji_al(self, kullanici):
        playfair_alfabe = playfair_alfabe_olustur(key)  # Server ile aynı anahtar olmalı
        tablo = playfair_tablosu(playfair_alfabe)
        while True:
            encrypted_data = kullanici.recv(2048).decode(FORMAT)
            if encrypted_data.strip():
                encrypted_username, encrypted_message = encrypted_data.split(' ', 1)
                username = playfair_decrypt(encrypted_username, tablo)
                message_content = playfair_decrypt(encrypted_message, tablo)
                temiz_username = desifreli_metin_temizle(username)
                temiz_metin = desifreli_metin_temizle(message_content)
                self.mesaj_ekle(f"[{temiz_username}] {temiz_metin}")
            else:
                QMessageBox.critical(self, "Error", "Received an empty message.")


def main():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ex = ChatClient()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
