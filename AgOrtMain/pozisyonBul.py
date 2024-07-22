def pozisyon_bul(char, tablo):
    for row_index, row in enumerate(tablo):
        if char in row:
            return row_index, row.index(char)
    raise ValueError(f"Character {char} not found in table")