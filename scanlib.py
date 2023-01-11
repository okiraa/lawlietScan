class Tools:
    def color(cor, text):
        colors = {
        "ciano": "\033[36m",
        "magenta": "\033[35m",
        "blue": "\033[1;34m",
        "red": "\033[31m",
        "green": "\033[1;32m",
        "yellow": "\033[1;33m",
        "fundo": "\033[0;0m"}
        return colors[cor]+f"{text}"+colors["fundo"]

    defaultports = [21, 22, 23, 25, 53, 67, 68, 69, 80, 110, 123, 143, 177, 389, 443, 445, 587, 993, 995, 3306, 3690]
    defaultheaders = {'User-Agent': 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}

