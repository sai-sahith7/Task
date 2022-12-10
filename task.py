from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import pandas as pd

driver = webdriver.Edge()
website = "https://propertysearch.altusgroup.com/Property/Search/All/All/For-Sale-and-To-Let/All/All/All/All/recently-added-first/All"
driver.get(website)
wait = WebDriverWait(driver, 5)
wait.until(ec.presence_of_element_located(
    (By.XPATH, '//button[@class="load-more-button d-inline-block title3"]')))
property_links = list()
result = {'Property Address': list(), 'Property Area': list(), 'Property Type': list(), 'Property Link': list(), 'Image Links': list(
), 'Property Description': list(), 'Key Features': list(), 'Agent Names': list(), 'Agent Mails': list(), 'Agent Contacts': list(), 'Property File Link': list()}
while True:
    try:
        driver.find_element(
            By.XPATH, '//button[@class="load-more-button d-inline-block title3"]').click()  # constantly click on load more button until it disappears
    except:
        # used child::button to get the button
        if len(driver.find_elements(By.XPATH, '//div[@id="property-pagination-wrapper"]//child::button')) == 2:
            continue
        else:
            for i in driver.find_elements(
                    By.XPATH, '//div[@class="d-inline-flex property-card-wrapper"]//a'):
                property_links.append(i.get_attribute('href'))
            for j in property_links:
                driver.get(j)
                result['Property Link'].append(j)
                wait.until(ec.presence_of_element_located((
                    By.XPATH, '//h2[@class="property-address title1 d-block"]//parent::div[@class="d-inline-block property-details"]')))  # used parent::div to get the address
                result['Property Address'].append(driver.find_element(
                    By.XPATH, '//h2[@class="property-address title1 d-block"]').text)
                image_elements = driver.find_elements(
                    By.XPATH, '//div[@class="d-inline-block property-images"]//img')
                images = set()
                for image in image_elements:
                    images.add(image.get_attribute('src'))
                result['Image Links'].append(';'.join(list(images)))
                result['Property Area'].append(driver.find_element(
                    By.XPATH, '//p[@class="d-block property-size-item title3"]').text)
                result['Property Type'].append(driver.find_element(
                    By.XPATH, '//h1[@class="property-type title3 d-block"]').text)
                result['Property Description'].append(driver.find_element(
                    By.XPATH, '//br//parent::p[@id="about-property-section"]').text.split("\n")[0])  # used parent::p to get the description (not actually necessary)
                key_feature_elements = driver.find_elements(
                    By.XPATH, '//p[@class="d-block key-feature-item title5"]')
                features = list()
                for feature in key_feature_elements:
                    features.append(feature.text)
                result['Key Features'].append(';'.join(features))
                agent_name_elements = driver.find_elements(
                    By.XPATH, '//p[@class="contact-name title5 d-block"]')
                agent_names = list()
                for agent_name in agent_name_elements:
                    agent_names.append(agent_name.text)
                result['Agent Names'].append(';'.join(agent_names))
                agent_mail_elements = driver.find_elements(
                    By.XPATH, '//a[@class="agent-contact d-block w-100 title5"]//preceding-sibling::a')  # used preceding-sibling::a to get the mail
                agent_mails = list()
                for agent_mail in agent_mail_elements:
                    agent_mails.append(agent_mail.get_attribute('href'))
                result['Agent Mails'].append(';'.join(agent_mails))
                agent_phone_elements = driver.find_elements(
                    By.XPATH, '//a[@class="agent-contact d-block w-100 title5"]//following-sibling::a')  # used following-sibling::a to get the phone
                agent_phones = list()
                for agent_phone in agent_phone_elements:
                    agent_phones.append(agent_phone.get_attribute('href'))
                result['Agent Contacts'].append(';'.join(agent_phones))
                result['Property File Link'].append(driver.find_element(
                    By.XPATH, '//a[contains(text(),"View current brochure")]').get_attribute('href'))  # used contains() function to get the link
            print("done")
            print(result)
            break

df = pd.DataFrame(result)
df.to_csv('Output.csv')
