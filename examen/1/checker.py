# Folosim requests ca să putem trimite cereri către site-uri.
import requests

# Site-urile pe care le vom verifica în exercițiu.
SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

# Acestea sunt antetele de securitate pe care le căutăm mai jos.
SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    # Scoatem slash-urile de la capătul gazdei și începutul căii.
    while host.endswith("/"):
        host = host[:-1]
    while path.startswith("/"):
        path = path[1:]

    return "https://" + host + "/" + path


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    # Verificăm primele 8 caractere; lower face verificarea indiferent de majuscule.
    return url[:8].lower() == "https://"


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    try:
        # Așteptăm cel mult 5 secunde pentru răspunsul site-ului.
        response = requests.get(url, timeout=5)
        # Afișăm statusul primit, de exemplu 200 dacă pagina s-a deschis.
        print(f"Status: {response.status_code}")
        # Unele site-uri nu trimit Content-Type; în cazul acesta afișăm "unknown".
        print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")
    except requests.RequestException as error:
        # Dacă site-ul nu răspunde, spunem ce s-a întâmplat și continuăm programul.
        print(f"Eroare la cerere: {error}")


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        # Încercăm să deschidem pagina și nu așteptăm mai mult de 5 secunde.
        response = requests.get(url, timeout=5)
        return {
            # Păstrăm codul HTTP primit de la site.
            "status": response.status_code,
            # Aici aflăm ce fel de conținut a trimis site-ul.
            "content_type": response.headers.get("Content-Type"),
            # Măsurăm mărimea conținutului primit, în octeți.
            "length": len(response.content),
            # Dacă nu aflăm numele serverului, trecem "unknown".
            "server": response.headers.get("Server", "unknown"),
        }
    except requests.RequestException:
        # Nu am primit un status HTTP, așa că îl marcăm cu None și păstrăm mesajul erorii.
        return {"status": None, "error": "Eroare de conexiune sau timeout."}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    results = []
    for url in SITES:
        # Verificăm fiecare adresă și ținem minte atât URL-ul, cât și rezultatul.
        result = check_site(url)
        result["url"] = url
        results.append(result)

    # Pentru această listă, considerăm reușite doar răspunsurile cu status 200.
    successful_sites = []
    for result in results:
        if result["status"] == 200:
            successful_sites.append(result)

    # Comparăm lungimile și punem pagina mai mare înaintea celei mai mici.
    for i in range(len(successful_sites)):
        for j in range(i + 1, len(successful_sites)):
            if successful_sites[j]["length"] > successful_sites[i]["length"]:
                successful_sites[i], successful_sites[j] = successful_sites[j], successful_sites[i]

    # Afișăm site-urile care au răspuns cu 200.
    print("Site-uri cu status 200 (ordonate după lungime):")
    for result in successful_sites:
        print(f"{result['url']} - {result['length']} bytes")

    # Orice rezultat care nu e 200 intră la celelalte: de exemplu 404, 500 sau o eroare de conexiune.
    failed_count = len(results) - len(successful_sites)
    print(f"Site-uri reușite: {len(successful_sites)}")
    print(f"Site-uri eșuate: {failed_count}")
    # Returnăm și toate rezultatele, ca să le poată folosi și partea care a apelat funcția.
    return results


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        # Cerem pagina ca să putem vedea ce antete ne-a trimis.
        response = requests.get(url, timeout=5)
    except requests.RequestException:
        # Dacă cererea nu reușește, nu avem antete de verificat.
        return {"status": None, "error": "Eroare de conexiune sau timeout."}

    # La HTTP, majusculele nu contează aici, așa că punem numele în litere mici.
    response_header_names = []
    for name in response.headers:
        response_header_names.append(name.lower())

    # Trecem prin lista noastră, astfel antetele găsite rămân în ordinea inițială.
    present = []
    for header in SECURITY_HEADERS:
        if header.lower() in response_header_names:
            present.append(header)

    # Ce nu am găsit ajunge în lista missing.
    missing = []
    for header in SECURITY_HEADERS:
        if header not in present:
            missing.append(header)

    # Calculăm ce procent din antete am găsit și îl rotunjim în jos la un întreg.
    score = int(len(present) / len(SECURITY_HEADERS) * 100)
    return {"present": present, "missing": missing, "score": score}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    # Ținem numărul cererilor trimise, inclusiv pe cele care dau eroare.
    requests_sent = 0
    # Dacă nu primim niciun răspuns HTTP, statusul va rămâne None.
    last_status = None
    # Ne ajută să aflăm dacă toate încercările au eșuat din cauza conexiunii.
    connection_errors = 0

    # Folosim numărul cerut de încercări; o valoare negativă înseamnă zero încercări.
    for _ in range(attempts):
        requests_sent += 1
        try:
            # La fiecare încercare așteptăm cel mult 5 secunde.
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            # Dacă am primit un status sub 500, nu mai încercăm din nou (nici la 404).
            if last_status < 500:
                return {"status": last_status, "attempts": requests_sent}
        except requests.RequestException:
            # La o eroare de rețea trecem la următoarea încercare, dacă mai avem.
            connection_errors += 1

    result = {"status": last_status}
    # Adăugăm eroarea doar când n-am reușit să primim niciun răspuns HTTP.
    if requests_sent > 0 and connection_errors == requests_sent:
        result["error"] = "Eroare de conexiune sau timeout."
    result["attempts"] = requests_sent
    return result
