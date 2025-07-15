import logging
import os
import time
from datetime import date

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(levelname)s - %(message)s')

def prune_download_folder(folder):
    """Remove all files in the specified folder."""
    for file in os.listdir(folder):
        os.remove(os.path.join(folder, file))

def setup_driver():
    """Set up WebDriver with opciones for headless browsing."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def download_magazine(driver, url):
    try:
        logging.info(f"Navigating to: {url}")
        driver.get(url)
        time.sleep(2)

        # # TODO: make it more reactive in order to be able to use ThreadPoolExecutor
        # WebDriverWait(driver, 6).until(
        #     EC.presence_of_element_located((By.CLASS_NAME, 'link-anchor')))
        
        download_url = extract_download_url()

        logging.info(f"Downloading PDF from: {download_url}")
        response = requests.get(download_url)
        response.raise_for_status()

        # Get the current date
        current_date = date.today().strftime("%Y-%m-%d")

        # Save the PDF file
        filename = os.path.join(download_folder, f"{os.path.basename(url)}_{current_date}.pdf")

        with open(filename, 'wb') as file:
            file.write(response.content)
        logging.info(f"[SUCCESS] Successfully downloaded: {filename}")
        return True


    except Exception as e:
        logging.error(f"Error occurred while downloading {url}: {str(e)}")
        return False


def get_read_button():
    button_texts = ["Jetzt lesen", "Read now"]

    for text in button_texts:
        try:
            return driver.find_element(By.LINK_TEXT, text)
        except:
            pass
    return None


def extract_download_url():
    return get_read_button().get_attribute('href')


def main():
    """Main function to download all magazines."""
    download_folder = "downloaded_magazines"
    os.makedirs(download_folder, exist_ok=True)
    prune_download_folder(download_folder)  # Clean the folder before starting downloads

    driver = setup_driver()

    magazine_urls = [  # Replace with actual URLs
        "https://iceportal.de/zeitungskiosk/brand_eins",
        "https://iceportal.de/zeitungskiosk/brigitte",
        "https://iceportal.de/zeitungskiosk/capital",
        "https://iceportal.de/zeitungskiosk/cicero",
        "https://iceportal.de/zeitungskiosk/couch",
        "https://iceportal.de/zeitungskiosk/die_welt",
        "https://iceportal.de/zeitungskiosk/e_commerce_magazin",
        "https://iceportal.de/zeitungskiosk/falstaff",
        "https://iceportal.de/zeitungskiosk/fas",
        "https://iceportal.de/zeitungskiosk/faz",
        "https://iceportal.de/zeitungskiosk/flow",
        "https://iceportal.de/zeitungskiosk/geliebte_katze",
        "https://iceportal.de/zeitungskiosk/geo",
        "https://iceportal.de/zeitungskiosk/handelsblatt",
        "https://iceportal.de/zeitungskiosk/mens_health_de",
        "https://iceportal.de/zeitungskiosk/monopol",
        "https://iceportal.de/zeitungskiosk/psychologie_heute",
        "https://iceportal.de/zeitungskiosk/schoener_wohnen",
        "https://iceportal.de/zeitungskiosk/stern",
        "https://iceportal.de/zeitungskiosk/sueddeutsche_zeitung",
        "https://iceportal.de/zeitungskiosk/tagesspiegel",
        "https://iceportal.de/zeitungskiosk/taz_die_tageszeitung",
        "https://iceportal.de/zeitungskiosk/financial_times",
        "https://iceportal.de/zeitungskiosk/sports_illustrated",
        "https://iceportal.de/zeitungskiosk/the_london_standard",
    ]


    # Download each magazine sequentially
    for url in magazine_urls:
        download_magazine(driver, url)

    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     executor.map(download_magazine, magazine_urls)
    # doesn't work with sleep timer, which is needed in selenium to get the download button
    driver.quit()


if __name__ == "__main__":
    main()
