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

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s: %(levelname)s - %(message)s"
)


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
        filename = os.path.join(
            download_folder, f"{os.path.basename(url)}_{current_date}.pdf"
        )

        with open(filename, "wb") as file:
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
    return get_read_button().get_attribute("href")


def main():
    """Main function to download all magazines."""
    download_folder = "downloaded_magazines"
    os.makedirs(download_folder, exist_ok=True)
    prune_download_folder(download_folder)  # Clean the folder before starting downloads

    driver = setup_driver()

    base_url = "https://iceportal.de/zeitungskiosk/"
    magazine_names = [
        "brand_eins",
        "brigitte",
        "capital",
        "cicero",
        "couch",
        "die_welt",
        "e_commerce_magazin",
        "falstaff",
        "fas",
        "faz",
        "flow",
        "geliebte_katze",
        "geo",
        "handelsblatt",
        "mens_health_de",
        "monopol",
        "psychologie_heute",
        "schoener_wohnen",
        "stern",
        "sueddeutsche_zeitung",
        "tagesspiegel",
        "taz_die_tageszeitung",
        "financial_times",
        "sports_illustrated",
        "the_london_standard",
    ]

    for name in magazine_names:
        url = f"{base_url}{name}"
        download_magazine(driver, url)

    # TODO: doesn't work with sleep timer, which is needed in selenium to get the download button
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     executor.map(download_magazine, magazine_urls)
    driver.quit()


if __name__ == "__main__":
    main()
