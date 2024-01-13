import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from dataclasses import dataclass

chromedriver_autoinstaller.install()

url = 'https://findoutnazare.pt/category/onde-dormir/'

browser = webdriver.Chrome()
source = browser.page_source

container_xpath = '//*[@id="finderListings"]/div[2]'
grid_items_css = '.col-md-12.grid-item .lf-item'
item_link_xpath = './a/@href'
info_address_xpath = "/div[@class='lf-item-info']/h4/text()"
info_contact_xpath = "/div[@class='lf-item-info']/ul/li/i/text()"

browser.get(url)
container = browser.find_element_by_xpath(container_xpath)
grid_items = container.find_elements(By.CSS_SELECTOR, grid_items_css)

item_link = grid_items.find_elements(By.XPATH, item_link_xpath)
# ^ take link for this listing

#@dataclass
#class Place:
#    link: str
#    address: str
#    contact: str
#
# places = []
#
#for item in grid_items:
#    places.append(
#        Place(link=item.find_element_by_xpath(item_link_xpath),
#              address=item.find_element_by_xpath(info_address_xpath),
#              contact=item.find_element_by_xpath(info_contact_xpath)
#            )
    
