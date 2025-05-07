import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# config telegram
TOKEN = '7847062572:AAGBzajQT5z9Si7HfnkUGW5tdXVzwZSQ8JE'
CHAT_ID = '249699122'

def enviar_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Mensaje enviado a Telegram")
    else:
        print("Error al enviar el mensaje a Telegram")

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ejecutar backend
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--log-level=3")
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_contenido(driver):
    driver.get("https://www.ticketmaster.es/event/40759?subchannel_id=12071&brand=es_bluelane")
    print("Iniciando botito...")

    try:
        enviar_telegram("funciona test")
        # cargar boton de ticketmaster
        btn_buscar = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Buscar entradas']"))
        )

        # clicar encima del javascript
        driver.execute_script("arguments[0].click();", btn_buscar)
        print("Click valido en 'Buscar entradas'")

        time.sleep(2)

        fan_items = driver.find_elements(By.XPATH, "//span[contains(text(), 'Entradas de fan a fan')]")
        print(f"Hay {len(fan_items)} entradas 'Fan a Fan'")

        if len(fan_items) > 0:
            message = f"¡Entradas 'Fan a Fan' encontradas para Billie Eilish! 🎟️"
            enviar_telegram(message)

    except TimeoutException:
        print("No se ha encontrado el boton 'Buscar entradas'")
    except Exception as e:
        print("SE: ", e)

if __name__ == "__main__":
    driver = get_driver()
    get_contenido(driver)
    driver.quit()
