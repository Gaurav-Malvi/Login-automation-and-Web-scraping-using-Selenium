# Python script to automate the process of login and scraping the Order Histroy data on Amazon



# Import necessary libraries
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from dotenv import dotenv_values



# Load environment variables from info.env (Privacy for Login Credentials)
env_variables = dotenv_values("path/to/your/info.env")

# Retrieve email and password from loaded environment variables
EMAIL = env_variables.get('AMAZON_EMAIL')
PASSWORD = env_variables.get('AMAZON_PASSWORD')

LOGIN_URL = "https://www.amazon.in/ap/signin?openid.pape.max_auth_age=900&openid.return_to=https%3A%2F%2Fwww.amazon.in%2Fgp%2Fyourstore%2Fhome%3Fpath%3D%252Fgp%252Fyourstore%252Fhome%26signIn%3D1%26useRedirectOnSuccess%3D1%26action%3Dsign-out%26ref_%3Dnav_AccountFlyout_signout&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0"

# Initialize the Chrome WebDriver
ser = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=ser)


driver.get(LOGIN_URL)


# find the email field and fill the information
email_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "ap_email"))
)

email_field.send_keys(EMAIL)
continue_button = driver.find_element(By.ID, "continue")
continue_button.click()


# In Case if email or phone number is incorrect
try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "a-list-item"))
    )
    print("Incorrect email or phone number")
    driver.quit()
except TimeoutException:
    pass



# find the password_field and fill the information
password_field = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "ap_password"))
)

password_field.send_keys(PASSWORD)
sign_in_submit = driver.find_element(By.ID, "signInSubmit")
sign_in_submit.click()


# In Case if password is incorrect
try:
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "a-list-item"))
    )
    print("Incorrect password")
    driver.quit()
except TimeoutException:
    pass




# direct to Order History Page
order_history = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "nav-orders"))
)
order_history.click()



# List to Store Scraped Data
orders_data = []



# Select the orders (type list)
orders = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".a-box-group.a-spacing-base.order"))
    )



# Iterate each order and scrape the relevant information
for order in orders:
    order_date = order.find_element(By.CSS_SELECTOR, ".a-color-secondary.value").text
    print(order_date)

    order_number = order.find_element(By.CSS_SELECTOR, ".a-row.a-size-mini.yohtmlc-order-id .a-color-secondary.value bdi").text
    print(order_number)

    delivery_date = order.find_element(By.CSS_SELECTOR, "div[style='margin-right:230px; padding-right:20px'] .a-size-medium.a-color-base.a-text-bold").text
    print("Delivery Date:", delivery_date)

    product_name = order.find_element(By.CSS_SELECTOR, ".a-fixed-left-grid .a-row a.a-link-normal").text
    print("Product Name:", product_name)
 
    price = order.find_element(By.CSS_SELECTOR, ".a-color-secondary.value span").text.strip()
    print("Price:", price)

    # Add data to orders_data
    orders_data.append({
        'Order ID': order_number,
        'Product Name': product_name,
        'Order Date': order_date,
        'Delivery Date': delivery_date,
        'Price': price
    })



# Convert the list of dictionaries to a pandas DataFrame 
df = pd.DataFrame(orders_data)

# Save the DataFrame to a CSV file
df.to_csv('amazon_order_history.csv', index=False, encoding='utf-8')


time.sleep(10)

# Close the browser
driver.quit()

print("Data has been successfully scraped and saved to amazon_order_history.csv")
