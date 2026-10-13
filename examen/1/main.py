# Importăm funcțiile din checker.py ca să le putem testa aici.
from checker import (build_url, check_headers, check_site, is_https, retry_check, scan_sites, show_response)

if __name__ == "__main__":
    # Folosim un site care răspunde și unul care nu există.
    functional_url = "https://example.com"
    unreachable_url = "http://this-site-does-not-exist.invalid"

    # Partea 1: apeluri pentru build_url
    # Încercăm o cale cu slash la început și una fără.
    print(build_url("example.com", "/login"))
    print(build_url("example.com", "about"))

    # Partea 1: apeluri pentru is_https
    # Primul URL folosește HTTPS, iar al doilea folosește HTTP.
    print(f"https://example.com: {is_https('https://example.com')}")
    print(f"http://example.com: {is_https('http://example.com')}")

    # Partea 2: apeluri pentru show_response
    # Funcția afișează statusul și Content-Type sau mesajul de eroare.
    print(f"Test pentru site din SITES: {functional_url}")
    show_response(functional_url)
    print(f"Test pentru site inaccesibil din SITES: {unreachable_url}")
    show_response(unreachable_url)

    # Partea 3: apeluri pentru check_site
    # Afișăm dicționarul cu detaliile primite de la fiecare site.
    print(f"Rezultat pentru {functional_url}: {check_site(functional_url)}")
    print(f"Rezultat pentru {unreachable_url}: {check_site(unreachable_url)}")

    # Partea 4: apeluri pentru scan_sites
    # scan_sites verifică toate adresele din lista SITES și ne returnează rezultatele.
    scan_results = scan_sites()
    # Mai afișăm separat orice adresă care nu a avut statusul 200.
    print("Rezultatele site-urilor din SITES care nu au status 200:")
    for result in scan_results:
        if result["status"] != 200:
            # Status None înseamnă că nu am primit deloc un răspuns HTTP.
            if result["status"] is None:
                print(f"Inaccesibil (eroare de conexiune/timeout): {result['url']}")
            # Dacă există un status, site-ul a răspuns, dar cu alt cod decât 200.
            else:
                print(f"Răspuns HTTP {result['status']}: {result['url']}")

    # Partea 5: apeluri pentru check_headers
    # Comparăm antetele de securitate ale unui site funcțional și ale unuia inaccesibil.
    print(f"Rezultat pentru {functional_url}: {check_headers(functional_url)}")
    print(f"Rezultat pentru {unreachable_url}: {check_headers(unreachable_url)}")



    # Partea 6: apeluri pentru retry_check
    print("\n=== Partea 6: retry_check ===")
    # Afișăm apelul, apoi rezultatul returnat de funcție.
    print('retry_check("https://httpbin.org/status/200")')
    print("#", retry_check("https://httpbin.org/status/200"))

    print('retry_check("https://httpbin.org/status/404")')
    print("#", retry_check("https://httpbin.org/status/404"))

    print('retry_check("https://httpbin.org/status/500")')
    print("#", retry_check("https://httpbin.org/status/500"))

    print('retry_check("https://httpbin.org/status/500", attempts=2)')
    print("#", retry_check("https://httpbin.org/status/500", attempts=2))

    print('retry_check("http://this-site-does-not-exist.invalid")')
    print("#", retry_check("http://this-site-does-not-exist.invalid"))
