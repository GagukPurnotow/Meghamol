from web3 import Web3
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC    
import requests, json, time, secrets

web3 = Web3()

# Log to a text file
def log(txt):
    with open('datamegaethwallet.txt', "a") as f:
        f.write(txt + '\n')    
        
def get_token(url, delay_seconds=7):
    try:
        # Initialize the driver in headless mode
        driver = Driver(uc=True, headless=True)  # Set headless=True
        
        # Open URL with reconnect time
        driver.uc_open_with_reconnect(url, reconnect_time=delay_seconds)
        
        # Wait for specified delay
        time.sleep(delay_seconds)
        
        # Wait for the FAUCET element to be clickable and click it
        faucet_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'FAUCET')]"))
        )
        faucet_button.click()  # Click on the FAUCET button to trigger the CAPTCHA popup
        
        # Wait for specified delay
        time.sleep(delay_seconds)
        
        # Wait for element to be present and get its value
        token_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "cf-turnstile-response"))
        )
        
        # Get the token value from the element
        token = token_element.get_attribute("value")
        
        # Check if the token is invalid and recursively call get_token if necessary
        if not token or token == "None":
            print(f'Fail! Trying to get token again...')
            return get_token(url, delay_seconds)  # Return the result of the recursive call
        else:
            print(f'\r\r\033[0m>>\033[1;32m Captcha token get successful \033[0m')
            return token
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None  # Return None in case of an error
    finally:
        try:
            driver.quit()
        except:
            pass

def req_faucet(token, addr, proxy=None):
    try:
        url = f"https://carrot.megaeth.com/claim"
        headers = {
            "content-type": "application/json",
            "origin": "https://testnet.megaeth.com",
            "referer": "https://testnet.megaeth.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }
        
        # Prepare the proxy settings if provided
        proxies = {
            "http": proxy,
            "https": proxy
        } if proxy else None

        # Data for the API request
        data = {
            "addr": addr,
            "token": token
        }

        # Send POST request with the optional proxy
        response = requests.post(url, headers=headers, json=data, proxies=proxies)

        # Return the JSON response
        return response.json()
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

proxy = input('input http rotate proxy [ http://user:pass@ip:port : ')
delays = int(input('input delay get token [min 7 second] : '))
while True:
    try:
        sender = web3.eth.account.from_key(secrets.token_hex(32))
        print(f'Processing get turnstile token...')
        gettoken = get_token("https://testnet.megaeth.com/", delays)
        print(f'token : {gettoken}')
        reqfaucet = req_faucet(gettoken, sender.address, proxy)
        txhash = reqfaucet["txhash"]
        if not txhash or txhash == "None" or txhash == None or txhash == "":
            print(f'get faucet failed for address {sender.address}')
            print(f'{reqfaucet}')
        else:
            print(f'get faucet success for address {sender.address}')
            print(f'txhash : {txhash}')
            log(f'{sender.address}|{web3.to_hex(sender.key)}')
    except Exception as e:
        print(str(e))