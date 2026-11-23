#B1 - Magic bytes
def tip_real(cale):
    with open(cale, 'rb') as f:
        cap = f.read(8)
    if cap.startswith(b"%PDF"):
        return "PDF"
    elif cap.startswith(b"\x89PNG"):
        return "PNG"
    elif cap.startswith(b"\xff\xd8"):
        return "JPEG"
    elif cap.startswith(b"PK\x03\x04"):
        return "ZIP/DOCX"
    return "Necunoscut: " + cap.hex()

print("--- B1: Identificarea tipului real --- ")

print("foto.jpg: ", tip_real("probe/foto.jpg"))
print("ascuns.png: ", tip_real("probe/ascuns.png"))

#B2 - Extragerea texului dintr-un fisier binar
import re
print("\n--- B2: Extragerea textului dintr-un fisier binar --- ")
with open("probe/ascuns.png", 'rb') as f:
    date = f.read()

for m in re.findall(rb"[ -~]{4,}", date):
    print(m.decode())

# B3 - Extragerea metadatelor EXIF si GPS

from PIL import Image
from PIL.ExifTags import TAGS
print ("\n--- B3: Extragerea metadatelor EXIF si GPS --- ")
img = Image.open("probe/foto.jpg")
exif = img.getexif()

for id, val in exif.items():
    print(TAGS.get(id, id), "=", val)

gps = exif.get_ifd(34853)
if gps:
    lat = gps[2]
    lon = gps[4]

    latitudine = float(lat[0]) + float(lat[1])/60 + float(lat[2])/3600
    longitudine = float(lon[0]) + float(lon[1])/60 + float(lon[2])/3600
    if gps[1] == 'S':
        latitudine = -latitudine
    if gps[3] == 'W':
        longitudine = -longitudine
    print("Latitudine:", round(latitudine, 6))
    print("Longitudine:", round(longitudine, 6))
else:
    print("Nu s-au gasit date GPS in imagine.")

# B4 - File carving
import zipfile
print("\n--- B4: File carving --- ")

with open("probe/ascuns.png", 'rb') as f:
    date = f.read()
i = date.find(b"PK\x03\x04")
if i != -1:
    with open("gasit.zip", 'wb') as f:
        f.write(date[i:])
    print("Arhiva extrasa de la octetul:", i)

    with zipfile.ZipFile("gasit.zip", 'r') as arhiva:
        print("Fisiere gasite: ", arhiva.namelist())

        mesaj = arhiva.read("secret.txt").decode()
        print("Mesajul gasit in arhiva: ", mesaj)
else:
        print("Nu a fost gasita o arhiva ZIP.")

# B5 - Ascunderea unui mesaj prin LSB

from PIL import Image
print("\n--- B5: Ascunderea unui mesaj prin LSB --- ")
img = Image.open("probe/foto.jpg").convert("RGB")
px = list(img.getdata())
mesaj = b"FLAG{ascuns_in_pixeli}" + b"\x00"
biti = "".join(f"{x:08b}" for x in mesaj)

#Transformam pixelii in canale de culoare
canale = []
for r, g, b in px:
    canale.extend([r, g, b])    
if len(biti) > len(canale):
    raise ValueError("Mesajul este prea lung pentru a fi ascuns in imagine.")
#Ascundem fiecare bit in ultimul bit al unui canal
for i,bit in enumerate(biti):
    canale[i] = (canale[i] & ~1) | int(bit)

#Reconstruim pixelii
px_nou = []
for i in range(0, len(canale), 3):
    px_nou.append(tuple(canale[i:i+3]))
img.putdata(px_nou)
img.save("stego.png")
print("Mesaj ascuns: ", mesaj[:-1].decode())
print("imaginea stego.png a fost creata cu succes.")


#B6 - Extragerea mesajului ascuns prin LSB
print("\n--- B6: Extragerea mesajului ascuns prin LSB --- ")
img = Image.open("stego.png").convert("RGB")
px = list(img.getdata())

biti = ""
for r, g, b in px:
    biti += str(r & 1)
    biti += str(g & 1)
    biti += str(b & 1)
mesaj_extras = bytearray()
for i in range(0, len(biti) -7, 8):
    octet = int(biti[i:i+8], 2)
    if octet == 0:
        break
    mesaj_extras.append(octet)
print("Mesajul extras: ", mesaj_extras.decode())