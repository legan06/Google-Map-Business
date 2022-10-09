import csv
from email.contentmanager import raw_data_manager
from numpy import inf
from selenium.webdriver.common.keys import Keys

import time
from selenium import webdriver


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By

import chromedriver_autoinstaller


from geopy.geocoders import Nominatim

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import re
import json
from apify_client import ApifyClient

chromedriver_autoinstaller.install()
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("window-size=1280,800")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.headless = True
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument('--disable-dev-shm-usage')

chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#prefs = {"profile.managed_default_content_settings.images": 2}
#capa = DesiredCapabilities.CHROME
#chrome_options.add_experimental_option("prefs", prefs)
#chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
chrome_options.add_argument('log-level=3')
#chrome_options.add_argument('-lang=en_US')
chrome_options.add_argument("--lang=en-GB")
driver=webdriver.Chrome(chrome_options=chrome_options)
                    
                    
                    
chrome_options2 = webdriver.ChromeOptions()
chrome_options2.add_argument('disable-infobars')
chrome_options2.headless = True
chrome_options2.add_argument('log-level=3')
chrome_options2.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options2.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options2.add_experimental_option('useAutomationExtension', False)
#chrome_options2.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})

prefs = {"profile.managed_default_content_settings.images": 2}
capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"
chrome_options2.add_experimental_option("prefs", prefs)

driver2=webdriver.Chrome(chrome_options=chrome_options2,desired_capabilities=capa)

# Initialize Nominatim API
geolocator = Nominatim(user_agent="geoapiExercises")
 
EMAIL_REGEX=r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'''

with open("page_number.txt","r")as file:
    page_number=int(file.readlines()[0].replace("\n","").strip())
    
with open("queries.csv","r")as file:
    all_lines=file.readlines()
    
print(all_lines)
all_lines=[x for x in all_lines if "DONE" not in x]



def done_region(query,page_number):
    with open("queries.csv","r") as file:
        llines=file.readlines()
        print(llines)
        print(query)
        for i in range(0,len(llines)):
            if query in llines[i]:
                llines[i]=f"{llines[i]},DONE with {page_number} pages"
            llines[i]=llines[i].replace("\n","")
                
    with open("queries.csv","w") as file:   
        for i in llines:
            file.write(i+"\n")
            


def findmail(website,information_list,driver2):
    
    print("\nParsing\n")
    
    url=website.replace("http://","").replace("https://","").replace("www.","").split(".")[0]    
    print(url)

    divide_title=information_list[0].lower().split(" ")

    if website[-1]=="/":
        website=website[:-1]
        
    driver2.get(website)
    time.sleep(6)
    contact_urls=[]
    contact_urls.append(website)
    try:
        contact_urls.append(driver2.find_element_by_xpath('//a[contains(@href,"contact")]').get_attribute("href"))
    except:
        pass
    try:
        contact_urls.append(driver2.find_element_by_xpath('//a[contains(@href,"about")]').get_attribute("href"))
    except:
        pass
    em_list=''
    
    list_of_emails=[]
    for contact in contact_urls:
        if "http" not in contact:
            try:
                contact=driver2.current_url.split("/")[0]+"//"+url.split("/")[2]+contact
            except:
                continue
        print(contact)
        driver2.get(contact)
        time.sleep(5)

        page_source=driver2.page_source
        
        
        for re_match in re.finditer(EMAIL_REGEX,page_source):
            list_of_emails.append(re_match.group())
            

        for g,email in enumerate(list_of_emails):
            if em_list=='':
                em_list=email
            else: 
                em_list=f"{em_list} | {email}"

                
        information_list[4]=em_list
        for g,email in enumerate(list_of_emails):
            if ".png" in email:
                continue
            
            for i in divide_title:
                if (len(i)>3) and (i in email) and((len(email)<70))and "www." not in i:
                    information_list[3]=email
                    break
                    

            if "co.uk" in email:
                information_list[3]=email

            if "@gmail.com" in email:
                information_list[3]=email
                
            if "info@" in email:
                information_list[3]=email
                
            if "contact@" in email:
                information_list[3]=email


            if "@hotmail.com" in email:
                information_list[3]=email
                

            if "@icloud.com" in email:
                information_list[3]=email
            
            if "me.uk" in email:
                information_list[3]=email

            if "business" in email:
                information_list[3]=email


            if (email=='') and (url in email):
                information_list[3]=email
            if information_list[3]!='':
                break
                

    return information_list

     
def start(queries,page_number,driver,driver2):
    with open("output_File.csv","a+", encoding="utf8", newline='') as file:
        wr=csv.writer(file)
        wr.writerow(("Business Name","Address", "Postal Code","Email","Other Emails","Search Term Used","Website"))
        
    driver.maximize_window()
    driver.get("https://www.google.com/maps/")
    time.sleep(5)
    try:
        driver.find_element_by_xpath('//button[@aria-label="Accept all"]').click()
        time.sleep(5)
    except:
        pass
    restart_count=0

    for query in queries:
        #Close and open browser to clear ram
        #"""""
        restart_count+=4
        if restart_count==2:
            restart_count=0
            driver.close()
            time.sleep(1)
            driver2.close()
            driver=webdriver.Chrome(chrome_options=chrome_options)
            driver.get("https://www.google.com/maps/")
            driver2=webdriver.Chrome(chrome_options=chrome_options2,desired_capabilities=capa)
        #"""""
        #Cleared ram
            
        #print(query)
        query=query.replace("\n","")
        driver.get("https://www.google.com/maps/search/"+query)
        time.sleep(5)
        
        for i in range(1,page_number+1):
            
            print(f"'{query}'- Page {i}")
            if i!=1:
                try:
                    next_button=WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH,'//button[@jslog="12696;track:click"]'))).click()
                    time.sleep(3)
                except:
                    pass
            for a in range(0,20):
                try:
                    elements=WebDriverWait(driver, 7).until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="bfdHYd Ppzolf OFBs3e"]')))
                    driver.execute_script("arguments[0].scrollIntoView(true);",elements[a])
                
                    time.sleep(0.5)
                except:
                    pass
                
            for d in range(0,20):
                information_list=[]
                for b in range(1,8):
                    information_list.append("")
            

                #print(i)
                try:
                    elements=driver.find_elements_by_xpath('//a[@class="hfpxzc"]')
                    elements[d].click()
                    time.sleep(4)
                except:
                    break
                #Add business name
                try:
                    business_name=WebDriverWait(driver, 7).until(EC.presence_of_element_located((By.XPATH,'//h1[@class="DUwDvf fontHeadlineLarge"]'))).text
                    information_list[0]=business_name
                except:
                    pass
                
                #Add business address
                try:    
                    store_address=driver.find_elements_by_xpath("//div[contains(text(),'United Kingdom')]")[0].text
                    information_list[1]=store_address
                    information_list[2]=store_address.replace(", United Kingdom","").split(" ")[-2]+" "+store_address.replace(", United Kingdom","").split(" ")[-1]

                except:
                    pass
                
                #Add email
                website=''
                try:    
                    website= driver.find_elements_by_xpath('//a[@data-tooltip="Open website"]')[0].get_attribute("href")
                    
                except:
                    pass
                if website!='':
                    information_list=findmail(website,information_list,driver2)
                    information_list[6]=website

                    
                information_list[5]=query
                print(information_list)
                
                with open("output_File.csv","a+", encoding="utf8", newline='') as file:
                    wr=csv.writer(file)

                    wr.writerow((information_list[0],information_list[1],information_list[2],information_list[3],information_list[4],information_list[5],information_list[6]))


        done_region(query,page_number)
        
      
    print("END OF THE SCRIPT")  
start(all_lines,page_number,driver,driver2)
