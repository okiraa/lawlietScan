#!/usr/bin/python3

import socket
import collections
from subprocess import check_output
from rich.console import Console
from bs4 import BeautifulSoup
from threading import Thread
from rich.table import Table
from requests import get
from time import sleep
from rich import print
from os import system
from sys import argv

defaultports = [21, 22, 23, 25, 53, 67, 68, 69, 80, 110, 123, 143, 177, 389, 443, 445, 587, 993, 995, 3306, 3690]
defaultheaders = {'User-Agent': 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
collections.Callable = collections.abc.Callable

banner = lambda color : f"""[{color}]

█   █   █▀█ █ █ █▀▀
█   █▄▄ █▄█ ▀▄▀ ██▄

    █ █ ▄▀█ █▀▀ █▄▀ █ █▄ █ █▀▀
    █▀█ █▀█ █▄▄ █ █ █ █ ▀█ █▄█

i want a way out of loneliness :(

  -= created by: kira † '-'
        """

class Scan:
    def __init__(self, url, wordlist):
        self.url = url.replace("https://", "") if "https://" in url else url.replace("http://", "")
        self.url2 = url
        self.ip = socket.gethostbyname(self.url)
        self.openPorts = []
        self.wordlist = wordlist
        Thread(target=self.portscanner).start()
        self.domain = socket.getfqdn(self.url)
        try:
            self.server = f"[red]{get(self.url2).headers['server']}"
        except KeyError:
            self.server = ""

    def portscanner(self, ports=defaultports):
        for port in ports:
            sock = socket.socket()
            sock.settimeout(0.3)
            try:
                sock.connect((self.url, port))
                self.openPorts.append(port)
            except Exception as e:
                continue

    def directoryScanner(self):
        with open(self.wordlist, "r") as file:
            words = [word.replace("\n", "") for word in file.readlines()]
        directory = "[yellow][+] Wordlist → " + f"[green]({self.wordlist})...\n"
        print(directory)
        self.generatelog("[+] DIRETORIOS/ARQUIVOS ENCONTRADOS ↓")
        for word in words:
            newUrl = f"{self.url2}/{word}"
            cod = get(newUrl, defaultheaders)
            if cod.status_code == 200:
                self.generatelog(newUrl)
                print(f"[green] → {newUrl} ← [200]")
            elif cod.status_code == 404:
                print(f"[red] → {newUrl} ← [404]")
            else:
                self.generatelog(newUrl)
                print(f"[yellow] → {newUrl} ← [{cod.status_code}]")
        print()

    def getinfobyip(self):
        sleep(0.5)
        result = get(f"https://ipinfo.io/{self.ip}/json").json()
        bn = "[!] INFORMAÇÕES SOBRE O IP ↓"
        print(f"[yellow]{bn}")
        del result["ip"]
        del result["readme"]
        with open(self.filename, "a") as file:
            file.write(bn+"\n")
            for k, v in result.items():
                bn2 = f" → {k.upper()}: {v}"
                file.write(bn2+"\n")
                print(f"[magenta]{bn2}")

    def getBanner(self):
        print("[yellow][!] Banner Grabbing...")
        if 21 in self.openPorts:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.ip, 21))
            banner = sock.recv(1024).decode()
            if banner:
                print("\n[green][+] [Port 21] ↓↓\n" + f"[blue]{banner}")
        if 22 in self.openPorts:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.ip, 22))
            banner2 = sock.recv(1024).decode()
            if banner2:
                print("[green][+] [Port 22] ↓↓\n" + f"[blue]{banner2}")
        else:
            print("[red][-] Error in Banner Grabbing.\n")

    def getrobots(self):
        sleep(1)
        robots = get(f"{self.url2}/robots.txt", headers=defaultheaders)
        if robots.status_code == 200 and "User-agent" in robots.text:
            bn = "[!] robots.txt Encontrado ↓"
            table = Table()
            table.add_column("robots.txt", style="magenta")
            table.add_row(robots.text, style="cyan")
            console = Console()
            print(f"[yellow]{bn}")
            console.print(table)
            self.generatelog(f"{bn}\n{45*'-'}\n{robots.text}{45*'-'}")

    def service(self):
        print("[yellow][!] Escaneando Portas Padrões ↓\n")
        sleep(1.5)
        if self.openPorts:
            table = Table()
            table.add_column("PORTA", style="magenta")
            table.add_column("SERVIÇO", style="cyan")
            self.generatelog("[+] Portas Abertas: ")
            for port in self.openPorts:
                service = socket.getservbyport(port)
                self.generatelog(f"PORT: {port} → SERVICE: {service}")
                table.add_row(str(port), service)
            else:
                console = Console()
                console.print(table)
        print()

    def savesite(self):
        self.filename = f"sites/saved/{self.url.split('.')[1]}.html"
        save = "[yellow][!] Salvando Html em → " + f"[green]({self.filename})..."
        print(save)
        sleep(1.5)
        content = get(self.url2).text
        with open(self.filename, "w") as file:
            file.write(content)

    def generatelog(self, *data):
        self.filename = f"sites/{self.url.split('.')[1]}.txt"
        with open(self.filename, "a") as file:
            for e in data:
                file.write(str(e)+"\n")

    # Desenvolvendo e Testando...
    def entrypoints(self):
        print("[yellow][!] Entry Points.\n")
        with open(self.filename, "r") as file:
            content = file.read()
        soup = BeautifulSoup(content, "html.parser")
        links = soup.find_all("script", {"src":True})
        for source in links:
            print(f"[cyan] → {source['src']}")
        print()

    def run(self):
        system("clear")
        print(banner("blue"))
        url, ip = f"[+] URL → {self.url}", f"[+] IP → {self.ip}"
        self.generatelog(url, ip)
        sleep(1)
        print(f"[green]{url} ({self.server})\n[cyan]{ip}")
        self.getinfobyip()
        self.getrobots()
        self.service()
        self.getBanner()
        self.savesite()
        self.entrypoints()
        try:
            self.directoryScanner()
        except KeyboardInterrupt:
            print("\n[red][-] Interrompido Pelo Usuario!")

#implementar.
class Proxy:
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)

    def runProxy(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(10)

if len(argv) != 3:
    print(banner("green"))
    print("[yellow][!] Use: python3 lawliet.py [url] [wordlist.txt]\n  → Use -w No Final Para Usar a Wordlist Padrão.")
    print("[yellow][!] If You Want to Run a Proxy Server:\n  → python3 lawliet.py [host] [port]")
    exit()
elif argv[2] in ("-w", "-W", "--w", "--W"):
    scan = Scan(argv[1], "wordlists/wordlist.txt")
    scan.run()
else:
    if isinstance(int(argv[2]), int):
        print("ainda não foi implementada.")
        exit()
    scan = Scan(argv[1], argv[2])
    scan.run()