#playfair.py
#Burada Playfair algoritmasının çalışma mantığına göre tablomuz oluşuyor.


# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*- coding: latin-1 -*-

def playfair_alfabe_olustur(key):
    turkce_alfabe = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ.,;!?:&"
    key = key.upper()
    seen = set()
    key_unique = ""
    for char in key:
        if char not in seen and char in turkce_alfabe:
            seen.add(char)
            key_unique += char
    
    # Anahtar kelimenin harflerinden sonra gelen harfleri ekleyin
    playfair_alfabe = key_unique
    for char in turkce_alfabe:
        if char not in seen:
            playfair_alfabe += char
    return playfair_alfabe

def metin_hazirla(metin, yerine_koyulan='&'):
    metin = metin.upper().replace(" ", "")
    hazir_metin = ""
    i = 0
    while i < len(metin):
        if i + 1 < len(metin) and metin[i] == metin[i + 1]:
            hazir_metin += metin[i] + yerine_koyulan
            i += 1
        else:
            hazir_metin += metin[i]
            if i + 1 < len(metin):
                hazir_metin += metin[i + 1]
            i += 2
    if len(hazir_metin) % 2 != 0:
        hazir_metin += yerine_koyulan
    return hazir_metin


def playfair_tablosu(alfabe):
    if len(alfabe) != 36:
        raise ValueError("Alfabe boyutu hatalı, 36 karakter olmalı.")
    tablo = []
    for i in range(6):
        satir = []
        for j in range(6):
            satir.append(alfabe[i * 6 + j])
        tablo.append(satir)
    return tablo



# Kullanıcıdan anahtar kelimeyi alın
key = input("Anahtar kelimeyi girin: ") # !!! ---- default bir key koyup daha sonra key doğrulama koyabiliriz ---- !!!

# Playfair alfabesini oluşturun
playfair_alfabe = playfair_alfabe_olustur(key)


alfabe = playfair_alfabe
tablo = playfair_tablosu(alfabe)

# Tabloyu yazdırma
for satir in tablo:
  print(" ".join(satir))