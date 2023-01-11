#!/usr/bin/python3

import socket
import collections
from sys import argv
from os import system
from time import sleep
from rich.console import Console
from rich.table import Table
from scanlib import Tools
from threading import Thread
from requests import get
from bs4 import BeautifulSoup

collections.Callable = collections.abc.Callable
banner = lambda color : cor(color, """

█   █   █▀█ █ █ █▀▀
█   █▄▄ █▄█ ▀▄▀ ██▄

    █ █ ▄▀█ █▀▀ █▄▀ █ █▄ █ █▀▀
    █▀█ █▀█ █▄▄ █ █ █ █ ▀█ █▄█

i want a way out of loneliness :(

  -= created by: kira † '-'
        """)

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
            self.server = cor("red", get(self.url2).headers["server"])
        except KeyError:
            self.server = ""

    def portscanner(self, ports=Tools.defaultports):
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
        directory = cor("yellow", "[+] Procurando Diretorios com → ")+cor("green", f"[{self.wordlist}]...")
        print(directory)
        self.generatelog("[+] DIRETORIOS/ARQUIVOS ENCONTRADOS ↓")
        for word in words:
            newUrl = f"{self.url2}/{word}"
            cod = get(newUrl, headers=Tools.defaultheaders)
            if cod.status_code == 200:
                self.generatelog(newUrl)
                print(cor("green", f" → {newUrl} ← [200]"))
            elif cod.status_code == 404:
                print(cor("red", f" → {newUrl} ← [404]"))
            else:
                self.generatelog(newUrl)
                print(cor("yellow", f" → {newUrl} ← [{cod.status_code}]"))

    def getinfobyip(self):
        sleep(0.5)
        result = get(f"https://ipinfo.io/{self.ip}/json").json()
        bn = "[!] INFORMAÇÕES SOBRE O IP ↓"
        print(cor("yellow", bn))
        del result["ip"]
        del result["readme"]
        with open(self.filename, "a") as file:
            file.write(bn+"\n")
            for k, v in result.items():
                bn2 = f" → {k.upper()}: {v}"
                file.write(bn2+"\n")
                print(cor("magenta", bn2))

    def getrobots(self):
        sleep(1)
        robots = get(f"{self.url2}/robots.txt", headers=Tools.defaultheaders)
        if robots.status_code == 200 and "User-agent" in robots.text:
            bn = "[!] robots.txt Encontrado ↓"
            table = Table()
            table.add_column("robots.txt", style="magenta")
            table.add_row(robots.text, style="cyan")
            console = Console()
            print(cor("yellow", bn))
            console.print(table)
            self.generatelog(f"{bn}\n{45*'-'}\n{robots.text}{45*'-'}")

    def service(self):
        print(cor("yellow", "[!] Escaneando Portas Padrões ↓"))
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

    def savesite(self):
        self.filename = f"sites/saved/{self.url.split('.')[1]}.html"
        save = cor("yellow", f"[!] Salvando Html em → ")+cor("green", f"[{self.filename}]...")
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
        print(cor("yellow", "[!] Entry Points."))
        with open(self.filename, "r") as file:
            content = file.read()
        soup = BeautifulSoup(content, "html.parser")
        links = soup.find_all("script", {"src":True})
        for source in links:
            print(cor("ciano", f" → {source['src']}"))

    def run(self):
        system("clear")
        print(banner("blue"))
        url, ip = f"[+] URL → {self.url}", f"[+] IP → {self.ip}"
        self.generatelog(url, ip)
        sleep(1)
        print(f"{cor('green', url)} ({self.server})\n{cor('ciano', ip)}")
        self.getinfobyip()
        self.getrobots()
        self.service()
        self.savesite()
        self.entrypoints()
        try:
            self.directoryScanner()
        except KeyboardInterrupt:
            print(cor("red", "\n[-] Interrompido Pelo Usuario!"))

cor = Tools.color
if len(argv) != 3:
    print(banner("green"))
    print(cor("red", "[!] Use: python3 lawliet.py [url] [wordlist.txt]\n[!] Use -w No Final Para Usar a Wordlist Padrão."))
    exit()
elif argv[2] in ("-w", "-W", "--w", "--W"):
    scan = Scan(argv[1], "wordlists/wordlist.txt")
    scan.run()
else:
    scan = Scan(argv[1], argv[2])
    scan.run()
