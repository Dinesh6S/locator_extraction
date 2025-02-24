import time

import openpyxl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
workbook = openpyxl.Workbook()
workbook.remove(workbook["Sheet"])


# Start the browser
driver = webdriver.Chrome()
driver.get("bootswatch.com/default")  # Replace with your target URL





enter_email = driver.find_element(By.ID, f"login-user-id")
enter_email.send_keys('qaadmin@wizfreight.com')
enter_pass = driver.find_element(By.ID, f"login-password")
enter_pass.send_keys('qa_test@2025')
driver.find_element(By.ID, f"login-button-submit").click()

time.sleep(8)

driver.find_element(By.XPATH, f"//div[@href='/bookings/add']").click()
time.sleep(3)



def get_locators(master_element):
    elements = driver.find_elements(By.XPATH, f"//{master_element}")
    print(f'{len(elements)} Elements Found In The Page For The Given Element: {master_element} ')
    locator_count = 0
    finial_locators = []
    if (master_element == 'input'):

        elements_with_placeholder = driver.find_elements(By.XPATH, f"//div[contains(@class,'-placeholder')]")

        for j, element_with_placeholder in enumerate(elements_with_placeholder):
            locators = []
            locators_with_index = {}
            if(element_with_placeholder.is_displayed()):
                locators.append(f'By.XPATH: //div[text()=\'{element_with_placeholder.text}\']//following-sibling::div//input')
                locator_count = locator_count + 1
                locators_with_index[j] = locators
                finial_locators.append(locators_with_index)

    locator_count = 0
    for i, element in enumerate(elements):
        locators_with_index = {}
        locators = []
        try:
            element = driver.find_elements(By.XPATH, f"//{master_element}")[i]

            if(element.is_displayed()):
                tag = element.tag_name
                element_id = element.get_attribute("id")
                if element_id:
                    locators.append(f'By.ID: "{element_id}"')
                    locator_count = locator_count+1
                element_placeholder = element.get_attribute("placeholder")
                if element_placeholder:
                    locators.append(f'By.XPATH: "//{tag}[@placeholder=\'{element_placeholder}\']"')
                    locator_count = locator_count + 1
                element_class = element.get_attribute("class")
                if element_class:
                    locators.append(f'By.CLASS_NAME: "{element_class}"')
                    locator_count = locator_count + 1
                element_name = element.get_attribute("name")
                if element_name:
                    locators.append(f'By.NAME: "{element_name}"')
                    locator_count = locator_count + 1
                element_text = element.text
                if element_text:
                    element_text.split('\n')
                    locators.append(f'By.XPATH: "//{tag}[text()=\'{element_text}\']"')
                    locator_count = locator_count + 1

                locators_with_index[i] = locators
                finial_locators.append(locators_with_index)
            else:
                locators_with_index[i] = ['Element Not Displayed']
                finial_locators.append(locators_with_index)


        except StaleElementReferenceException:
            print(f"Element at index {i} became stale.")
    print(f'{locator_count} Locators Found In The Page For The Given Element: {master_element} ')
    add_locators_to_sheet(master_element, finial_locators)
    return finial_locators


def add_locators_to_sheet(element_name, element_list):
    sheet = workbook.create_sheet(title=f"{element_name} Element")
    headers = ["Element", "Locator", "Element Index", "Locator Type"]
    sheet.append(headers)
    element_index = 2
    for loc_index, loc_value in enumerate(element_list):
        for key, values in loc_value.items():
            for locator in values:
                if(locator == 'Element Not Displayed'):
                    locator_type = '-'
                else:
                    locator_type = locator.split(':')[0].split('.')[1]
                sheet[f"A{element_index}"] = element_name
                sheet[f"B{element_index}"] = locator
                sheet[f"C{element_index}"] = key+1
                sheet[f"D{element_index}"] = locator_type
                element_index = element_index+1
                # print(locator)


element = 'button'
get_locators(element)

element = 'input'
get_locators(element)
#
# element = 'a'
# get_locators(element)
#
# element = 'p'
# get_locators(element)


workbook.save("locators.xlsx")
driver.quit()