from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

driver = webdriver.Chrome()

def scrape_site_pattern_1(url):
    driver.get(url)

    list_codes = []
    while True:
        current_url = driver.current_url
        table_element = driver.find_element(By.TAG_NAME, "table")
        for row in table_element.find_elements(By.TAG_NAME, "tr")[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            code = cells[1].text
            list_codes.append(code)

        try:
            next_button = driver.find_element(By.LINK_TEXT, "Próxima")
            driver.execute_script("arguments[0].click();", next_button)
            if current_url == driver.current_url:
                break
        except:
            break

    return list_codes

def scrape_site_pattern_2(url):
    driver.get(url)

    list_codes = []
    while True:
        current_url = driver.current_url
        grid_elements = driver.find_elements(By.CSS_SELECTOR, ".actions")
        for grid_element in grid_elements:
            href = grid_element.find_element(By.TAG_NAME, "a").get_attribute("href")
            code = href.split("/")[-2].upper()
            list_codes.append(code)

        try:
            next_button = driver.find_element(By.LINK_TEXT, "Próxima")
            driver.execute_script("arguments[0].click();", next_button)
            if current_url == driver.current_url:
                break
        except:
            break

    return list_codes

def scrape_site_pattern_3(url):
    driver.get(url)

    list_codes = []
    while True:
        current_url = driver.current_url
        table_element = driver.find_element(By.TAG_NAME, "table")
        for row in table_element.find_elements(By.TAG_NAME, "tr")[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            code = cells[1].find_element(By.CSS_SELECTOR, ".description").get_attribute("title")
            list_codes.append(code)

        try:
            next_button = driver.find_element(By.LINK_TEXT, "Próxima")
            driver.execute_script("arguments[0].click();", next_button)
            if current_url == driver.current_url:
                break
        except:
            break
    
    return list_codes

def scrape_site_pattern_4(url):
    driver.get(url)

    list_codes = set()
    sub_links = set()
    while True:
        try:
            current_url = driver.current_url
            table_element = driver.find_element(By.TAG_NAME, "table")
            for row in table_element.find_elements(By.TAG_NAME, "tr")[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                sub_link = cells[2].find_element(By.TAG_NAME, "a").get_attribute("href")
                sub_links.add(sub_link)
            
            if len(list(sub_links)) > 1000:
                break 

            next_button = driver.find_element(By.LINK_TEXT, "Próxima")
            driver.execute_script("arguments[0].click();", next_button)
            if current_url == driver.current_url:
                break

        except Exception as e:
            print(e)
            break
    
    for sub_link in sub_links:
        driver.get(sub_link)
        try:
            code = driver.find_elements(By.CSS_SELECTOR, ".name-company")[0].text
            list_codes.add(code)
        except Exception as e:
            print(e)
            continue

    return list_codes

list_codes = set()
list_codes.update([(asset, "Exchange-Traded Fund (ETF)") for asset in scrape_site_pattern_1("https://investidor10.com.br/etfs-global/")])
list_codes.update([(asset, "Exchange-Traded Fund (ETF)") for asset in scrape_site_pattern_1("https://investidor10.com.br/etfs/")])
list_codes.update([(asset, 'Real Estate Investment Trust (REIT)') for asset in scrape_site_pattern_2("https://investidor10.com.br/reits/")])
list_codes.update([(asset, 'Certificate of Deposit (CDs)') for asset in scrape_site_pattern_2("https://investidor10.com.br/bdrs/")])
list_codes.update([(asset, 'Stock') for asset in scrape_site_pattern_2("https://investidor10.com.br/acoes/")])
list_codes.update([(asset, 'Fixed Income Fund') for asset in scrape_site_pattern_3("https://investidor10.com.br/fundos/classes/fundo-de-renda-fixa/")])
list_codes.update([(asset, 'Equity Fund') for asset in scrape_site_pattern_3("https://investidor10.com.br/fundos/classes/fundo-de-acoes/")])
list_codes.update([(asset, 'Multimarket Fund') for asset in scrape_site_pattern_3("https://investidor10.com.br/fundos/classes/fundo-multimercado/")])
list_codes.update([(asset, 'Currency Fund') for asset in scrape_site_pattern_3("https://investidor10.com.br/fundos/classes/fundo-cambial/")])
list_codes.update([(asset, 'Fixed Income Fund') for asset in scrape_site_pattern_3("https://investidor10.com.br/fundos/classes/renda-fixa/")])
list_codes.update([(asset, 'Multimarket Fund') for asset in scrape_site_pattern_3("https://investidor10.com.br/fundos/classes/multimercado/")])
list_codes.update([(asset, 'Equity Fund') for asset in scrape_site_pattern_3("https://investidor10.com.br/fundos/classes/acoes/")])
list_codes.update([(asset, 'Cryptocurrency') for asset in scrape_site_pattern_4("https://investidor10.com.br/criptomoedas/")])

driver.close()