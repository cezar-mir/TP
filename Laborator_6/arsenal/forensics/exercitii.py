
# Exercitiile A1-A6

import hashlib
from pathlib import Path
from decode import ghici_strat, desfa, citibil

PROBE = Path(__file__).resolve().parents[2] / "probe"

# A1
s = "Salut"
b = s.encode()

print("Octeti:", b)
print("Primul octet:", b[0])

hex_text = b.hex()
print("Hex:", hex_text)

original = bytes.fromhex(hex_text)
print("Refacut:", original)


# A2
print("\n--- A2: Recunoasterea codarii ---")
print(ghici_strat("%2Fetc"))
print(ghici_strat("48656c6c6f"))
print(ghici_strat("U2FsdXQ="))
print(ghici_strat("Salut lume!"))


# A3
print("\n--- A3: Decodarea mesajelor ---")
print(desfa("U2FsdXQ="))
print(desfa("48656c6c6f"))
print(desfa("%2Fetc%2Fpasswd"))


# A4
print("\n--- A4: Decodarea mai multor straturi ---")

val = "NTM1OTU3NTk="

for i in range(8):
    strat, b = desfa(val)
    print("Pasul", i + 1, "- Strat:", strat, "- Rezultat:", b)

    if citibil(b):
        print("Text citibil:", b.decode())
        break

    val = b.decode()


# A5
print("\n--- A5: Spargerea XOR cu o cheie de octet ---")

date = (PROBE / "xor.bin").read_bytes()

for k in range(256):
    clar = bytes(b ^ k for b in date)

    if citibil(clar) and b"FLAG{" in clar:
        print("Cheie:", k)
        print("Mesaj:", clar.decode())
        break


# A6
print("\n--- A6: Spargerea unui hash prin dictionar ---")

tinta = (PROBE / "hashuri.txt").read_text().splitlines()[0].strip()

print("Lungimea hash-ului:", len(tinta))

if len(tinta) == 32:
    print("Algoritm identificat: MD5")
elif len(tinta) == 40:
    print("Algoritm identificat: SHA1")
elif len(tinta) == 64:
    print("Algoritm identificat: SHA256")

with open(PROBE / "wordlist.txt", encoding="latin1") as f:
    for cuv in f:
        cuv = cuv.strip()

        if hashlib.md5(cuv.encode()).hexdigest() == tinta:
            print("Cuvant gasit:", cuv)
            break



# A4 - Decodarea completa a mesajului din fisier

import base64
from pathlib import Path

print("\n--- A4: Mesajul ascuns in straturi ---")

cale = Path(__file__).resolve().parents[2] / "probe" / "mesaj.txt"

mesaj = cale.read_text().strip()

pas1 = base64.b64decode(mesaj)
print("Primul strat Base64:", pas1)

pas2 = base64.b64decode(pas1)
print("Al doilea strat Base64:", pas2)

pas3 = bytes.fromhex(pas2.decode())
print("Mesaj final:", pas3.decode())
