
import time
import urllib.request
import requests
from requests import get
import requests as rq

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# EX 1
print(requests.__version__)

# EX 2
try:
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)

    time.sleep(1)
    response = get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)
except requests.RequestException as e:
    print(e)

# EX 3
time.sleep(1)
try:
    response = rq.get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)
except requests.RequestException as e:
    print(e)

# EX 4
time.sleep(1)
try:
    with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as response:
        print(response.status)
        html = response.read().decode("utf-8", errors="replace")
        print(html[:200])
except Exception as e:
    print(e)

# EX 5
print(dir(requests))

# EX 6
help(requests.get)

time.sleep(1)
try:
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print(response.status_code)
except requests.RequestException as e:
    print(e)

# EX 7
time.sleep(1)
try:
    start = time.perf_counter()
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    end = time.perf_counter()

    print(end - start)
    print(response.elapsed.total_seconds())
except requests.RequestException as e:
    print(e)

# EX 8
try:
    import bs4
except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

try:
    response = requests.get(BASE_URL, timeout=TIMEOUT)

    # EX 9
    print(response.status_code)
    print(response.ok)
    print(response.url)
    print(response.encoding)

    # EX 10
    try:
        response.raise_for_status()

        time.sleep(1)
        missing = requests.get(
            BASE_URL + "/this-page-does-not-exist",
            timeout=TIMEOUT
        )
        missing.raise_for_status()
    except requests.HTTPError:
        print("Pagina nu exista sau a returnat o eroare HTTP.")

    # EX 11
    for name, value in response.headers.items():
        print(name, ":", value)

    # EX 12
    print(response.headers.get("Server", "lipseste"))
    print(response.headers.get("Content-Type", "lipseste"))
    print(response.headers.get("content-type", "lipseste"))

    # EX 13
    print(response.text.lower().count("cyber"))

    # EX 14
    html = response.text
    html_lower = html.lower()
    start = html_lower.find("<title>")

    if start != -1:
        start += len("<title>")
        end = html_lower.find("</title>", start)
        title = html[start:end].strip() if end != -1 else "Titlu negasit"
    else:
        title = "Titlu negasit"

    print(title)

    # EX 15
    lines = html.splitlines()
    print(len(lines))

    if lines:
        print(len(max(lines, key=len)))

    # EX 16
    if response.url.startswith("https://"):
        print("Conexiune securizata")
    else:
        print("Conexiune nesecurizata")

    # EX 17
    time.sleep(1)
    redirected = requests.get(
        "http://cybercor.org",
        timeout=TIMEOUT
    )

    for item in redirected.history:
        print(item.status_code, item.url)

    print(redirected.url)

    # EX 18
    time.sleep(1)
    head_response = requests.head(BASE_URL, timeout=TIMEOUT)

    time.sleep(1)
    get_response = requests.get(BASE_URL, timeout=TIMEOUT)

    print(len(head_response.content))
    print(len(get_response.content))

    # EX 19
    if response.cookies:
        for cookie in response.cookies:
            print(cookie.name, cookie.secure)
    else:
        print("Niciun cookie setat")

except requests.RequestException as e:
    print(e)

# EX 20
time.sleep(1)

try:
    with requests.Session() as session:
        session.headers.update({
            "User-Agent": "WebLab-Student"
        })

        result = session.get(
            ECHO_URL + "/headers",
            timeout=TIMEOUT
        )

        result.raise_for_status()
        headers = result.json().get("headers", {})
        print(headers)

except (requests.RequestException, ValueError) as e:
    print(e)


import time
import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# EX 21
def fetch(url: str, timeout: int = 10):
    """Returneaza raspunsul HTTP."""
    time.sleep(1)
    return requests.get(url, timeout=timeout)

# EX 22
def get_status(url: str) -> int:
    """Returneaza codul HTTP."""
    return fetch(url).status_code

# EX 23
def fetch_timeout(url: str, timeout: int = 10):
    """Foloseste un timeout implicit sau explicit."""
    return fetch(url, timeout=timeout)

# EX 24
def get_title(html: str) -> str:
    """Extrage titlul paginii HTML."""
    lower = html.lower()
    start = lower.find("<title>")

    if start == -1:
        return "Titlu negasit"

    start += len("<title>")
    end = lower.find("</title>", start)

    if end == -1:
        return "Titlu negasit"

    return html[start:end].strip()

# EX 25
def show_docstring():
    """Afiseaza documentatia functiei get_title."""
    help(get_title)

# EX 26
def check_type_hints():
    """Verifica comportamentul adnotarilor de tip."""
    try:
        return get_status(123)
    except (requests.RequestException, TypeError, ValueError):
        return None

# EX 27
def page_exists(url: str) -> bool:
    """Verifica existenta paginii."""
    try:
        response = fetch(url)
        return response.ok
    except requests.RequestException:
        return False

# EX 28
def check_paths(base: str, paths: list) -> dict:
    """Returneaza codurile HTTP pentru cai."""
    results = {}

    for path in paths:
        try:
            results[path] = get_status(base.rstrip("/") + path)
        except requests.RequestException:
            results[path] = None

    return results

# EX 29
def get_header(url: str, name: str, default="lipseste"):
    """Returneaza un antet HTTP."""
    response = fetch(url)
    return response.headers.get(name, default)

# EX 30
def security_headers(url: str) -> dict:
    """Verifica antetele de securitate."""
    names = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    response = fetch(url)
    results = {}

    for name in names:
        results[name] = name in response.headers

    return results

# EX 31
def score_headers(results: dict) -> str:
    """Returneaza scorul antetelor."""
    return f"{sum(results.values())}/{len(results)}"

# EX 32
def fetch_robots(base: str):
    """Descarca robots.txt."""
    try:
        response = fetch(base.rstrip("/") + "/robots.txt")
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None


def disallowed_paths(robots_text) -> list:
    """Extrage valorile Disallow."""
    if robots_text is None:
        return []

    paths = []

    for line in robots_text.splitlines():
        line = line.split("#", 1)[0].strip()

        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()

            if path:
                paths.append(path)

    return paths

# EX 33
def response_times(*urls: str) -> dict:
    """Returneaza timpul fiecarei cereri."""
    results = {}

    for url in urls:
        try:
            response = fetch(url)
            results[url] = response.elapsed.total_seconds()
        except requests.RequestException:
            results[url] = None

    return results

# EX 34
def log(message: str, **details):
    """Afiseaza mesajul si detaliile."""
    result = message

    for key, value in details.items():
        result += f" | {key}={value}"

    print(result)


def safe_call(function, *args, **kwargs):
    """Trateaza erorile cererilor."""
    try:
        return function(*args, **kwargs)
    except (requests.RequestException, TypeError, ValueError) as e:
        print(e)
        return None


if __name__ == "__main__":

    # EX 21
    response = safe_call(fetch, BASE_URL)

    if response is not None:
        print(response.status_code)

    # EX 22
    for path in ["/", "/robots.txt", "/sitemap.xml"]:
        print(path, safe_call(get_status, BASE_URL + path))

    # EX 23
    response1 = safe_call(fetch_timeout, BASE_URL)
    response2 = safe_call(fetch_timeout, BASE_URL, timeout=3)

    if response1 is not None:
        print(response1.status_code)

    if response2 is not None:
        print(response2.status_code)

    # EX 24
    if response is not None:
        print(get_title(response.text))

    # EX 25
    show_docstring()

    # EX 26
    print(check_type_hints())

    # EX 27
    print(page_exists(
        "https://this-domain-does-not-exist.invalid"
    ))

    # EX 28
    print(check_paths(
        BASE_URL,
        ["/", "/robots.txt", "/sitemap.xml"]
    ))

    # EX 29
    print(safe_call(get_header, BASE_URL, name="Server"))

    # EX 30
    headers = safe_call(security_headers, BASE_URL)
    print(headers)

    # EX 31
    if headers is not None:
        print(score_headers(headers))

    # EX 32
    robots = fetch_robots(BASE_URL)
    print(disallowed_paths(robots))
    print(disallowed_paths(None))

    # EX 33
    print(response_times(
        BASE_URL,
        BASE_URL + "/robots.txt"
    ))

    # EX 34
    log("verificat", url=BASE_URL, status=200)


import hashlib
import json
import re
import socket
import ssl
import time

from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# EX 35
def parse_address(url: str) -> dict:
    """Descompune URL-ul."""
    parsed = urlparse(url)

    return {
        "scheme": parsed.scheme,
        "netloc": parsed.netloc,
        "path": parsed.path,
        "query": parsed.query,
        "fragment": parsed.fragment
    }

# EX 36
def absolute_links(base: str, links: list) -> list:
    """Transforma linkurile in URL-uri complete."""
    return [
        urljoin(base.rstrip("/") + "/", link)
        for link in links
    ]

# EX 37
def extract_links(html: str) -> list:
    """Extrage linkurile fara duplicate."""
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))

# EX 38
def split_links(links: list, domain: str) -> tuple:
    """Separa linkurile interne si externe."""
    base = domain if "://" in domain else "https://" + domain
    host = urlparse(base).hostname

    internal = []
    external = []

    for link in links:
        full_url = urljoin(base.rstrip("/") + "/", link)
        parsed = urlparse(full_url)

        if parsed.scheme not in ("http", "https"):
            continue

        if not parsed.hostname:
            continue

        if parsed.hostname.lower() == host.lower():
            internal.append(full_url)
        else:
            external.append(full_url)

    return internal, external

# EX 39
class ImageFinder(HTMLParser):
    """Gaseste imaginile HTML."""

    def __init__(self):
        """Initializeaza parserul."""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Prelucreaza tagurile HTML."""
        if tag.lower() == "img":
            src = dict(attrs).get("src")

            if src is not None:
                self.images.append(src)

# EX 40
def page_fingerprint(url: str) -> str:
    """Calculeaza hashul SHA256."""
    time.sleep(1)
    response = requests.get(url, timeout=TIMEOUT)

    return hashlib.sha256(
        response.content
    ).hexdigest()

# EX 41
def save_headers(response) -> dict:
    """Salveaza si citeste antetele JSON."""
    with open("headers.json", "w", encoding="utf-8") as f:
        json.dump(
            dict(response.headers),
            f,
            indent=2
        )

    with open("headers.json", "r", encoding="utf-8") as f:
        return json.load(f)

# EX 42
def resolve(hostname: str) -> str:
    """Obtine adresa IP."""
    return socket.gethostbyname(hostname)

# EX 43
def cert_days_left(hostname: str) -> int:
    """Calculeaza zilele ramase ale certificatului."""
    context = ssl.create_default_context()

    with socket.create_connection(
        (hostname, 443),
        timeout=TIMEOUT
    ) as sock:

        with context.wrap_socket(
            sock,
            server_hostname=hostname
        ) as secure_sock:

            expires = secure_sock.getpeercert()["notAfter"]

    timestamp = ssl.cert_time_to_seconds(expires)
    now = datetime.now(timezone.utc).timestamp()

    return int((timestamp - now) // 86400)


if __name__ == "__main__":

    # EX 35
    print(parse_address(
        "https://cybercor.org/path?x=1#top"
    ))

    # EX 36
    print(absolute_links(
        BASE_URL,
        ["/about", "contact.html", "../index.html"]
    ))

    # EX 39
    test_html = """
    <html><body>
        <img src="/logo.png" alt="Logo">
        <IMG SRC="poza.jpg">
        <img alt="imagine fara src">
        <img src="https://cdn.example.com/banner.webp" />
        <a href="/despre">Nu este imagine</a>
    </body></html>
    """

    finder = ImageFinder()
    finder.feed(test_html)

    assert finder.images == [
        "/logo.png",
        "poza.jpg",
        "https://cdn.example.com/banner.webp"
    ]

    # EX 37
    time.sleep(1)

    try:
        response = requests.get(
            BASE_URL,
            timeout=TIMEOUT
        )

        response.raise_for_status()
        html = response.text

        links = extract_links(html)
        print(links)

        # EX 38
        internal, external = split_links(
            links,
            BASE_URL
        )

        print(len(internal), len(external))

        # EX 39
        finder = ImageFinder()
        finder.feed(html)

        print(finder.images)
        print(html.lower().count("<img"))

        # EX 41
        headers = save_headers(response)
        print(headers.get("Content-Type", "lipseste"))

    except requests.RequestException as e:
        print(e)

    # EX 40
    try:
        hash1 = page_fingerprint(BASE_URL)
        hash2 = page_fingerprint(BASE_URL)

        print(hash1)
        print(hash2)
        print(hash1 == hash2)

    except requests.RequestException as e:
        print(e)

    # EX 42
    try:
        print(resolve("cybercor.org"))
    except OSError as e:
        print(e)

    # EX 43
    try:
        print(cert_days_left("cybercor.org"))
    except (OSError, ssl.SSLError, KeyError, ValueError) as e:
        print(e)

import csv
import json
import re
import socket
import ssl
import time

from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10
DIRECTORY = Path(__file__).resolve().parent

# EX 47
DEFAULT_HEADERS = {
    "User-Agent": "WebLab-Student"
}

# EX 44
def fetch(url: str, timeout: int = TIMEOUT):
    """Descarca o pagina web."""
    time.sleep(1)
    return requests.get(
        url,
        timeout=timeout,
        headers=DEFAULT_HEADERS
    )


def get_status(url: str) -> int:
    """Returneaza codul HTTP."""
    return fetch(url).status_code


def get_title(html: str) -> str:
    """Extrage titlul HTML."""
    lower = html.lower()
    start = lower.find("<title>")

    if start == -1:
        return "Titlu negasit"

    start += len("<title>")
    end = lower.find("</title>", start)

    if end == -1:
        return "Titlu negasit"

    return html[start:end].strip()


def security_headers(url: str, response=None) -> dict:
    """Verifica antetele de securitate."""
    if response is None:
        response = fetch(url)

    names = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy"
    ]

    return {
        name: name in response.headers
        for name in names
    }


def score_headers(results: dict) -> str:
    """Calculeaza scorul antetelor."""
    return f"{sum(results.values())}/{len(results)}"


def check_paths(base: str, paths: list) -> dict:
    """Verifica mai multe cai HTTP."""
    results = {}

    for path in paths:
        url = urljoin(
            base.rstrip("/") + "/",
            path.lstrip("/")
        )

        try:
            results[path] = get_status(url)
        except requests.RequestException:
            results[path] = None

    return results


def fetch_robots(base: str):
    """Citeste robots.txt."""
    try:
        response = fetch(
            base.rstrip("/") + "/robots.txt"
        )

        response.raise_for_status()
        return response.text

    except requests.RequestException:
        return None


def disallowed_paths(robots_text) -> list:
    """Extrage valorile Disallow."""
    if robots_text is None:
        return []

    paths = []

    for line in robots_text.splitlines():
        line = line.split("#", 1)[0].strip()

        if line.lower().startswith("disallow:"):
            path = line.split(":", 1)[1].strip()

            if path:
                paths.append(path)

    return paths


def extract_links(html: str) -> list:
    """Extrage linkurile HTML."""
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))


def split_links(links: list, domain: str) -> tuple:
    """Separa linkurile interne si externe."""
    base = domain if "://" in domain else "https://" + domain
    host = urlparse(base).hostname

    internal = []
    external = []

    for link in links:
        full_url = urljoin(
            base.rstrip("/") + "/",
            link
        )

        parsed = urlparse(full_url)

        if parsed.scheme not in ("http", "https"):
            continue

        if not parsed.hostname:
            continue

        if parsed.hostname.lower() == host.lower():
            internal.append(full_url)
        else:
            external.append(full_url)

    return internal, external


def resolve(hostname: str) -> str:
    """Returneaza adresa IP."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Calculeaza zilele ramase ale certificatului."""
    context = ssl.create_default_context()

    with socket.create_connection(
        (hostname, 443),
        timeout=TIMEOUT
    ) as sock:

        with context.wrap_socket(
            sock,
            server_hostname=hostname
        ) as secure_sock:

            expires = secure_sock.getpeercert()["notAfter"]

    timestamp = ssl.cert_time_to_seconds(expires)
    now = datetime.now(timezone.utc).timestamp()

    return int((timestamp - now) // 86400)


def redirect_chain(hostname: str) -> list:
    """Obtine lantul de redirectionari."""
    response = fetch("http://" + hostname)

    chain = []

    for item in response.history:
        chain.append({
            "status": item.status_code,
            "url": item.url
        })

    chain.append({
        "status": response.status_code,
        "url": response.url
    })

    return chain


# EX 49
def save_csv(results: dict):
    """Salveaza codurile HTTP in report.csv."""
    path = DIRECTORY / "report.csv"

    with open(
        path,
        "w",
        encoding="utf-8",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "path",
            "status",
            "checked_at"
        ])

        for relative_path, status in results.items():
            writer.writerow([
                relative_path,
                status,
                datetime.now().isoformat()
            ])

    return path


# EX 50
def site_report(url: str) -> dict:
    """Construieste raportul final al site-ului."""
    parsed = urlparse(url)

    if (
        parsed.scheme not in ("http", "https")
        or parsed.hostname != "cybercor.org"
        or parsed.path not in ("", "/")
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("URL nepermis")

    response = fetch(url)
    response.raise_for_status()

    title = get_title(response.text)
    host = urlparse(response.url).hostname

    try:
        ip = resolve(host)
    except OSError:
        ip = None

    try:
        redirects = redirect_chain(parsed.hostname)
    except requests.RequestException:
        redirects = []

    headers = security_headers(
        url,
        response=response
    )

    score = score_headers(headers)

    try:
        days = cert_days_left(host)
    except (OSError, ssl.SSLError, KeyError, ValueError):
        days = None

    links = extract_links(response.text)

    internal, external = split_links(
        links,
        response.url
    )

    robots = fetch_robots(BASE_URL)
    forbidden = disallowed_paths(robots)

    report = {
        "url": url,
        "status": response.status_code,
        "final_url": response.url,
        "title": title,
        "ip": ip,
        "redirects": redirects,
        "security_headers": headers,
        "security_score": score,
        "certificate_days": days,
        "internal_links": len(internal),
        "external_links": len(external),
        "disallowed_paths": forbidden
    }

    with open(
        DIRECTORY / "report.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(response.status_code)
    print(response.url)
    print(title)
    print(ip)
    print(redirects)
    print(score)
    print(days)
    print(len(internal), len(external))
    print(forbidden)

    return report


# EX 46
if __name__ == "__main__":
    try:
        print(get_status(BASE_URL))
    except requests.RequestException as e:
        print(e)