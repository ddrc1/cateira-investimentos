from bs4 import BeautifulSoup

list_codes = set()

with open("./html_files/fundos_imobiliarios.html", "r", encoding="utf-8") as file:
    content = file.read()

    html = BeautifulSoup(content, 'html.parser')
    links = html.select('.tickerBox__title')
    for link in links:
        code = link.text
        list_codes.add((code, "Real Estate Investment Trust (REIT)"))