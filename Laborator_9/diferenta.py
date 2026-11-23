
# B1 - Compararea a doua multimi

from enumerare import citeste_linii

def cai(fisier):
    return set(citeste_linii(fisier))


baza = cai("start/baza_suid.txt")
acum = cai("start/suid.txt")

print("baza:", len(baza), "acum:", len(acum))


# B2 - Identificarea fisierelor SUID noi

noi = acum - baza

print("\n--- B2: Fisiere SUID noi ---")
print(len(noi), "SUID noi fata de sistemul curat")

for c in sorted(noi):
    print(" ", c)


# B3 - Dictionar de risc si filtrarea fisierelor

from enumerare import nume, GTFO

risc = {
    nume(c): ("mare" if nume(c) in GTFO else "normal")
    for c in noi
}

periculoase = [
    c for c in sorted(noi)
    if nume(c) in GTFO
]

print("\n--- B3: Clasificarea riscurilor ---")
print("Dictionar de risc:", risc)
print("periculoase NOI:", periculoase)

