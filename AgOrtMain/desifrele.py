from pozisyonBul import pozisyon_bul

def playfair_decrypt(ciphertext, table):
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        row1, col1 = pozisyon_bul(ciphertext[i], table)
        row2, col2 = pozisyon_bul(ciphertext[i + 1], table)
        
        if row1 == row2:
            plaintext += table[row1][(col1 - 1) % 6] + table[row2][(col2 - 1) % 6]
        elif col1 == col2:
            plaintext += table[(row1 - 1) % 6][col1] + table[(row2 - 1) % 6][col2]
        else:
            plaintext += table[row1][col2] + table[row2][col1]
    return plaintext

def desifreli_metin_temizle(metin, yerine_koyulan="&"):
    temizlenmis_metin = ""
    skip_next = False
    for i in range(len(metin) - 1):
        if skip_next:
            skip_next = False
            continue
        if metin[i] == yerine_koyulan and metin[i + 1] == yerine_koyulan:
            continue  # Skip solitary padding characters
        if metin[i] == yerine_koyulan and i > 0 and metin[i - 1] == metin[i + 1]:
            continue  # Skip padding characters inserted to split duplicates
        temizlenmis_metin += metin[i]

    # Append the last character if it's not a padding character
    if metin[-1] != yerine_koyulan:
        temizlenmis_metin += metin[-1]
        
    return temizlenmis_metin.lower()