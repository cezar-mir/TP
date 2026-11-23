
# Laboratorul 9 - A1: Citirea fisierelor SUID

import argparse
import json
import os

def citeste_linii(cale):
    with open(cale, encoding="utf-8") as f:
        return [
            linie.strip()
            for linie in f
            if linie.strip() and not linie.strip().startswith("#")
        ]

cai = citeste_linii("start/suid.txt")

print("linii SUID:", len(cai))

#A2 - Nume unice folosind multimi
def nume(cale):
    return cale.rsplit("/", 1)[-1]

nume_unice = {nume(c) for c in cai}
print ("SUID distincte:", len(nume_unice))

# A3 - Clasificarea fisierelor SUID

GTFO = {
    "find", "vim.basic", "vim", "nmap", "cp",
    "bash", "less", "awk", "python3", "perl"
}

def suid_constatari(cale):
    cai = citeste_linii(cale)
    rezultat = []

    for c in sorted(set(cai)):
        risc = "mare" if nume(c) in GTFO else "normal"

        rezultat.append({
            "cale": c,
            "nume": nume(c),
            "risc": risc
        })
    return rezultat
suid = suid_constatari("start/suid.txt")
mari = [c for c in suid if c["risc"] == "mare"]
print(len(suid), "SUID,", len(mari), "cu risc mare")
print(sorted([c["nume"] for c in mari]))

#A4 - Analiza sudo si cron
def sudo_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
        user, drept = ln.split(":", 1)
        out.append({
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": "mare" if "NOPASSWD" in drept else "normal"
        })
    return out
def cron_constatari(cale):
    out = []
    for ln in citeste_linii(cale):
       campuri = ln.split()

       user = campuri[5]
       comanda = " ".join(campuri[6:])

       out.append({
           "user": user.strip(),
           "comanda": comanda.strip(),
           "risc": "mare" if comanda.strip() else "normal"
       })
    return out

def enumereaza(d):
   return{
    "suid": suid_constatari(os.path.join(d, "suid.txt")),
    "sudo": sudo_constatari(os.path.join(d, "sudo.txt")),
    "cron": cron_constatari(os.path.join(d, "crontab.txt"))
   }


raport = enumereaza("start")

print("\n--- A4: Analiza sudo si cron---")
print("Reguli sudo:", len(raport["sudo"]))
print("Sarcini cron:", len(raport["cron"]))

#A5 - Raport JSON si rezumat pe categorii
def main():
    p = argparse.ArgumentParser()
    p.add_argument("capturi")
    p.add_argument("--json", action="store_true")
    a=p.parse_args()

    raport=enumereaza(a.capturi)

    if a.json:
        print(json.dumps(raport, indent=2, ensure_ascii=False))
        return

    for categorie, lista in raport.items():
        mari = [c for c in lista if c.get("risc") =="mare"]
        print(f"{categorie}: {len(lista)} gasite, {len(mari)} cu risc mare")

    utilizatori = (
            {c["user"] for c in raport["sudo"]}
            | {c["user"] for c in raport["cron"]}
        )

    print("utilizatori implicati:", ",".join(sorted(utilizatori)))
    with open("enum.json","w", encoding="utf-8") as f:
        json.dump(raport,f,indent=2, ensure_ascii=False)
    print("Raport salvat in enumerare.json")

if __name__ == "__main__":
        main()