from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys,os,time
# ==========================
# CONFIG
# ==========================
#IMAGE_URL = "https://cdn.shopify.com/s/files/1/0424/4606/1723/files/Syrian-Hamster_grande.jpg"
WAIT_TIME = 15  # seconds

# ==========================
# HANDLE COMMAND-LINE ARGUMENTS
# ==========================
if len(sys.argv) >= 2:
    IMAGE_URL = sys.argv[1]
else:
    IMAGE_URL = input("Enter image URL: ").strip()

if not IMAGE_URL:
    print("Usage: python3 program.py <image_url>")
    sys.exit(1)

# Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
ublock=os.path.abspath("ublock")
chrome_options.add_argument(f"--load-extention={ublock}")
chrome_options.add_argument("--lang=en-US")
# ==========================
# SETUP DRIVER
# ==========================
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, WAIT_TIME)

# ==========================
# HELPER FUNCTION
# ==========================
def search_image_tineye(url):
    driver.get("https://tineye.com/")
    input_box = driver.find_element(By.NAME, "url")
    input_box.clear()
    input_box.send_keys(url)
    input_box.send_keys(Keys.RETURN)  # submit
    print("Tineye search done.")

def search_image_yandex(url):
    driver.get("https://yandex.com/images")
    img_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Image search']")))
    img_btn.click()
    input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Enter image URL']")))
    input_box.clear()
    input_box.send_keys(url)
    input_box.send_keys(Keys.RETURN)
    print("Yandex search done.")

def search_image_bing(url):
    driver.get("https://www.bing.com/visualsearch")
    paste_btn = wait.until(EC.element_to_be_clickable((By.ID, "vsk_pastepn")))
    paste_btn.click()
    input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='url'], input[placeholder*='URL']")))
    input_box.clear()
    input_box.send_keys(url)
    input_box.send_keys(Keys.RETURN)
    print("Bing search done.")

def search_image_saucenao(url):
    driver.get("https://saucenao.com")
    input_box = driver.find_element(By.NAME, "url")
    input_box.clear()
    input_box.send_keys(url)
    search_btn = wait.until(EC.element_to_be_clickable((By.ID, "searchButton")))
    search_btn.click()
    print("SauceNAO search done.")

def search_image_google_lens(url):
    driver.get("https://images.google.com")
    time.sleep(2)
    driver.execute_script('''
    // Try to find the Google Lens button using stable attributes
    let lensBtn = document.querySelector('div[jsname="R5mgy"][role="button"]');
    
    // If found, click it
    if (lensBtn) {
        lensBtn.click();
    }
    ''')
    time.sleep(1)

    driver.execute_script(f'''
        let inputBox = document.querySelector('input.cB9M7[jsname="W7hAGe"]');
        if (inputBox) {{
            inputBox.value = "{url}";
            inputBox.dispatchEvent(new Event("input", {{ bubbles: true }}));
            inputBox.dispatchEvent(new Event("change", {{ bubbles: true }}));
            let searchBtn = document.querySelector('div.Qwbd3[jsname="ZtOxCb"]');
            if (searchBtn) {{
                searchBtn.click();
            }}
        }}
    ''')
    
    print("Google Lens search done.")

# ==========================
# RUN ALL SEARCHES
# ==========================
search_image_tineye(IMAGE_URL)
input("Press Enter to continue")
search_image_bing(IMAGE_URL)
input("Press Enter to continue")
search_image_saucenao(IMAGE_URL)
input("Press Enter to continue")
try:
    search_image_google_lens(IMAGE_URL)
except Exception:
    pass
input("Press Enter to continue")
search_image_yandex(IMAGE_URL)
input("Press Enter to continue")
print("All searches completed.")
