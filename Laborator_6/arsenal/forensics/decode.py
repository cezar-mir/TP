
import re
import base64
import argparse
import json
from urllib.parse import unquote
from pathlib import Path


# A2 - Recunoasterea codarii
def ghici_strat(s):
    if re.search(r'%[0-9A-Fa-f]{2}', s):
        return "URL encoding"

    if len(s) % 2 == 0 and re.fullmatch(r'[0-9A-Fa-f]+', s):
        return "HEX"

    if re.fullmatch(r'[A-Za-z0-9+/]+={0,2}', s):
        return "Base64"

    return "necunoscut"


# A3 - Decodarea mesajului
def desfa(s):
    strat = ghici_strat(s)

    if strat == "Base64":
        rezultat = base64.b64decode(s)
    elif strat == "HEX":
        rezultat = bytes.fromhex(s)
    elif strat == "URL encoding":
        rezultat = unquote(s).encode()
    else:
        rezultat = s.encode()

    return strat, rezultat


# A4 - Verificarea textului
def citibil(b):
    return all(32 <= c < 127 for c in b)


# A7 - argparse si JSON
def main():
    p = argparse.ArgumentParser(
        description="Decoder universal pentru laborator"
    )

    p.add_argument("intrare", help="Sir sau cale catre fisier")
    p.add_argument("--fisier", action="store_true")

    a = p.parse_args()

    if a.fisier:
        with open(a.intrare, "rb") as f:
            date = f.read()

        try:
            intrare = date.decode("utf-8").strip()
        except UnicodeDecodeError:
            print("Fisierul contine date binare, nu text codificat.")
            return
    else:
        intrare = a.intrare

    strat, rezultat = desfa(intrare)

    print("Strat detectat:", strat)
    print("Rezultat:", rezultat)

    fisa = {
        "strat": strat,
        "rezultat": rezultat.decode("utf-8", errors="replace")
    }

    cale_json = Path(__file__).parent / "fisa.json"

    with open(cale_json, "w", encoding="utf-8") as f:
        json.dump(fisa, f, indent=4, ensure_ascii=False)

    print("Rezultatul a fost salvat in fisa.json")


if __name__ == "__main__":
    main()
