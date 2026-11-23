# Laboratorul 6 – Informații invizibile: forensics și steganografie

**Disciplina:** Tehnici de programare

## Lucrarea A – Decoder universal

În această lucrare am utilizat Python pentru recunoașterea și decodarea mesajelor în formatele Base64, HEX și URL encoding.

Am implementat funcții pentru identificarea tipului de codare, decodarea mesajelor și verificarea caracterelor imprimabile.

**Rezultatele obținute:**
- Base64: `U2FsdXQ=` → `Salut`
- HEX: `48656c6c6f` → `Hello`
- URL encoding: `%2Fetc%2Fpasswd` → `/etc/passwd`
- Cheia XOR identificată: `128`
- Mesajul XOR: `FLAG{xor_un_octet}`
- Algoritmul hash identificat: `MD5`
- Parola identificată prin dicționar: `password`

Am utilizat și biblioteca `argparse` pentru prelucrarea argumentelor din terminal și `json` pentru salvarea rezultatelor.

## Lucrarea B – Forensics și steganografie

În această lucrare am analizat structura fișierelor binare, metadatele imaginilor și tehnicile de ascundere a informațiilor.

**Rezultatele obținute:**
- Tipul real al fișierului `foto.jpg`: JPEG
- Tipul real al fișierului `ascuns.png`: PNG
- Dispozitivul din metadatele EXIF: Apple iPhone 13
- Data fotografiei: 14.09.2026, 10:30
- Coordonate GPS: 47.016667, 28.8575
- Fișier extras prin file carving: `secret.txt`
- Mesaj din arhiva ascunsă: `FLAG{ascuns_prin_carving}`
- Mesaj ascuns și extras prin LSB: `FLAG{ascuns_in_pixeli}`

## Concluzie

În cadrul laboratorului am studiat prelucrarea datelor binare în Python și utilizarea acestora în analiza forensic. Am aplicat metode de decodare Base64, HEX și URL, operații XOR, identificarea hash-urilor și căutarea prin dicționar.

De asemenea, am învățat să identificăm formatele fișierelor după semnătura binară, să extragem metadate EXIF și GPS și să descoperim informații ascunse în imagini.

Laboratorul mi-a permis să înțeleg mai bine utilizarea limbajului Python în securitatea informațională.