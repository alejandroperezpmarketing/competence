from datetime import datetime
import json
import selenium
from bs4 import BeautifulSoup
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class Competence():
    

    #constructor
    def __init__(self, search_engine_type = 'Google', browser_type = 'Chrome'):
        
        
        #Search attributes *******
        if browser_type.upper() not in ['CHROME', 'OPERA','FIREFOX','EDGE']:
            self._browser_type = None
        else:
            self._browser_type = browser_type

        if search_engine_type.upper() not in ['GOOGLE', 'YAHOO','YANDEX','BING']:
            self._search_engine_type = None
        else:
            self.search_engine_type = search_engine_type


        self._search_date = None
        self._search_engine_type = search_engine_type
        self._browser_type = browser_type

        
        
        #Start link
        #This is the link use by the system to make the research on the web - provied by the user
        self._start_link = None
        #datetime.today().strftime('%Y-%m-%d')
        self._search_time = None
        #datetime.now().strftime('%H-%m-%s')
        self._seach_id = None
        self._header_id = None
        self._extract_id = None

        #Numbers ******
        #This varible save the number of reults of geomarketing companies found asociated with a search keyword
        self._results_number = None

        #Title and subtitles *****
        #This variable save the dictionary if H1 titles and the result ID from each seach result  - SERP 
        self._header_results = {}
        
        #This varible save a dictionary and SERP ID of the keywords used on the SERP headers 
        self._header_keywords = None

        #This variable save a dictionary with the header link
        self._header_links = []


        

        #SERP Resume ******
        #This varible save a resume from the entire SERP extract dataset
        self._extract = None
        #This variable save a keyword list of earch SERP extract
        self._extract_keywords = None

        ###Links ******
        #This variable save a dictionary with the links and teh Result ID of each SERP
        self._links = {
            'link':None,
            'attributes':[]
            }

        


    def __repr__(self):

        report = {

            'Search Engine Type':self._search_engine_type,
            'Browser':self._browser_type,
            'Search date': self._search_date,
            'Search time': self._search_time,
            'Search link': self._start_link,
            'ChromeDrive': self._ChromeDrive

            }

        report = json.dumps(report, indent=4)

        return report



    #Properties ******

    #Set the start link to make the search on the browser

    def _set_link(self, code):
        self._start_link = code

    def _get_link(self):
        return self._start_link

    start_link = property(fget=_get_link, fset=_set_link)

    #Set the ChromeDrive for a selenium engine


    def _set_ChromeDrive(self, code):
        self._ChromeDrive = code
    def _get_ChromeDrive(self):
        return self._ChromeDrive

    ChromeDrive = property(fset=_set_ChromeDrive, fget=_get_ChromeDrive)
            


    #System methodes ********

    
    def _open_google_results(self,_start_link):
        #print(type(self._start_link))
        #print(self._ChromeDrive)
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        global driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(self._start_link)
        driver.find_element(By.ID,"L2AGLb").click()

        return driver
    
    def _extract_headers(self):
        disc_e = {}
        empresas = []
        directories = []
        headers = []
        header_links = []
        abstracts = []
        

        id = 1
        
        #Titilo de la  empresa
        for count, element in enumerate(driver.find_elements(By.XPATH,'//*[@class="dURPMd"]/div')):
            if driver.find_elements(By.XPATH, './/div[@class="GTRloc"]/span')[count].text == '':
                continue
            else:
                empresa = driver.find_elements(By.XPATH, './/div[@class="GTRloc"]/span')[count].text
                empresas.append(empresa)

        #link inferior
       
            if driver.find_elements(By.XPATH, './/div[@class="GTRloc"]/div/cite')[count].text == '':
                continue
            else:

                directory = driver.find_elements(By.XPATH, './/div[@class="GTRloc"]/div/cite')[count].text
                directories.append(directory)

        #Headers

            if driver.find_elements(By.XPATH, './/div[@class="yuRUbf"]/div/span/a/h3')[count].text == '':
                continue
            else:

                header = driver.find_elements(By.XPATH, './/div[@class="yuRUbf"]/div/span/a/h3')[count].text
                headers.append(header)

        #Link header
                
            if driver.find_elements(By.XPATH, './/div[@class="yuRUbf"]/div/span/a')[count].get_attribute('href') == '':
                continue
            else:
                header_link = driver.find_elements(By.XPATH, './/div[@class="yuRUbf"]/div/span/a')[count].get_attribute('href')
                header_links.append(header_link)

        

            disc_e[id] = {'Nombre de la empresa:':empresa,
                             'Directorio':directory,
                             'Titulios en la busqueda':header,
                             'Link':header_link
                             }

            id = id + 1
        

        #print(empresas, directories, headers,header_links)  
        #print(empresas, directories)
        # NOTA/ class='qGXjvb' bloque general del patrocinios
        # Nota class= 'MjjYud' claque individual de cada sin patrocinio
                                        
        print(json.dumps(disc_e, indent=4))
        with open("report.json", "w") as json_file:
            json_file.write(json.dumps(disc_e, indent=4))
            print('Saved succesfully')

    def _extract_SERP(self):
        self._open_google_results(self._start_link)
        self._extract_headers()
     

    #User methodes **********

    def extract_SERP(self):
        self._extract_SERP()
        
    


    

    

    
        

    
    

    


    

            
            


       
