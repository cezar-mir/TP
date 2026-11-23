
# A1 - Identificarea autentificarilor esuate

import re

TIPAR = re.compile(
    r"Failed password for (?:invalid user )?(\S+) from (\S+) port"
)

def esec(linie):
    m = TIPAR.search(linie)

    if m is None:
        return None

    return (m.group(1), m.group(2))


print(esec("Failed password for root from 203.0.113.9 port 51230 ssh2"))
print(esec("<linie stricata fara structura>"))

#A2 - Citirea esecurilor dint auth.log

def citeste_esecuri(cale):
    esecuri=[]

    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("Fisierul nu exista", cale)
        return esecuri

    with f:
        for linie in f:
            r = esec(linie)

            if r is not None:
                esecuri.append({
                    "user": r[0],
                    "ip": r[1]
                })
    return esecuri
esecuri = citeste_esecuri("start/auth.log")
print("esecuri:", len(esecuri))

#A3 - Numararea esecurilor pe IP

from collections import Counter
def pe_ip(esecuri):
    return Counter([e["ip"] for e in esecuri])

counts = pe_ip(esecuri)
print("\n--- A3: Numararea esecurilor pe IP ---")

for ip, n in counts.most_common():
    print(f"{ip}: {n}")

#A4 - Rezumatul autentificarilor esuate
import argparse
def main():
    p =argparse.ArgumentParser()
    p.add_argument("log")
    a = p.parse_args()

    esecuri = citeste_esecuri(a.log)
    counts = pe_ip(esecuri)

    print("Esecuri de autentificare:", len(esecuri))

    for ip, n in counts.most_common():
        print(F"{ip}:{n}")

    if __name__ == "__main__":
        main()