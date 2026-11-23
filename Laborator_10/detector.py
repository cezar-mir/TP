
# B1 - Identificarea adreselor IP suspecte

from collections import Counter

def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")

    rezultat = [
        (ip, n)
        for ip, n in counts.items()
        if n >= prag
    ]

    return sorted(rezultat, key=lambda x: x[1], reverse=True)


# Testarea functiei B1
c = Counter({
    "203.0.113.9": 13,
    "198.51.100.7": 2
})

print(suspecti(c))
print(suspecti(c, prag=2))

# B3 - argparse si raport JSON

import argparse
import json
from parse_auth import citeste_esecuri, pe_ip

def main():
    p = argparse.ArgumentParser()

    p.add_argument("log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")

    a = p.parse_args()

    esecuri = citeste_esecuri(a.log)
    counts = pe_ip(esecuri)
    sus = suspecti(counts, a.prag)

    if a.json:
        raport = {
            "esecuri": len(esecuri),
            "pe_ip": dict(counts),
            "suspecti": [
                {"ip": ip, "incercari": n}
                for ip, n in sus
            ]
        }

        print(json.dumps(raport, indent=2))
        return

    print("Esecuri de autentificare:", len(esecuri))

    for ip, n in counts.most_common():
        print(f" {ip}: {n}")

    print(f"Suspecti (prag {a.prag}):")

    for ip, n in sus:
        print(f" {ip} ({n} incercari) BRUTE FORCE")


if __name__ == "__main__":
    main()
