import requests
from bs4 import BeautifulSoup as soup
from Website import Website as Web
from Product import Product
import streamlit as st

class Enamine(Web):
    def build_search_query(self, search_term: str)-> str: #builds payload for request
        data = f"t%3Aformdata=5ZRS8eZATmCPt23H9cEHnWMai4Y%3D%3AH4sIAAAAAAAAAJWQv0oDQRDGJ4FYJIWgCEIQUmi7aUyjjUkhFkHE08Zu%2F4yXk73ddXdi7hpb38InEGv7FHa%2Bgw9ga2XhrVfJQdByvvmY3%2FfN0wd0FgPYSZB7OTsQ1iv0jGstSm8t1TMEDyPrU8YdlzNkxB0G8uWISetRZ4IJHpCNRSVySccZarWbIM3d3uWy9771%2BtWG1hR60hryVp%2FyHAk2pjf8jg81N%2BkwIZ%2BZ9LBwBOsVe1KeV%2BzJD%2FtP4cb%2FDXfmrcQQkrnIsxAya5bPav%2F68%2FGtDVC4RR%2B2fzMVp%2BpIVCDcwj0AQTdqtWulP9o7TUe9pdJhLHC0soC0ubMGDQV2kimFppn%2F6mGwWfRf1hqPjvhWfGy3Jl5UxG%2FlYaXI9QEAAA%3D%3D&allByRootBorder=on&dataSearch={search_term}&searchType=bb"
        return data

    def query_api(self, data: str) -> str: # makes request, returns a list of prodCodes
        url = "https://www.enaminestore.com/search.border.searchiddata;jsessionid=652AEB7F18E0BB79B4507D84D61C74D8"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-GB,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1"}    
        response = requests.post(url, headers = headers, data=data)
        #print(response)
        #print(response.text)  
        return response

    def find_catalogue_number(self, response: str) -> str: #soup finds catalogue number
        enamine_soup = soup(response.text, 'html.parser')
        catalogue_number = enamine_soup.find("span",{"class" : "catdata1 cdatamarker js-catalog-item-code"}).text
        return catalogue_number

    def pricing_query(self, catalogue_number: str) -> str: #builds payload for request and returns the response
        catalogue_url = f"https://www.enaminestore.com/productapi:price/{catalogue_number}"
        catalogue_response = requests.get(catalogue_url, data = catalogue_number) # seems to work without headers = headers
        pricing_details = catalogue_response.json()
        return pricing_details

    def output(self, pricing_details: str, response: str) -> str: #outputs catalogue details and prices:
        enamine_soup = soup(response.text, 'html.parser')
        result_numbers = enamine_soup.find("p", {"class" : "clearfix"})
        product_name = enamine_soup.findAll("span",{"class" : "catdata1"})
        name = product_name[2].text
        availability = enamine_soup.find("td", {"data-grid-property" : "stockinfo"}).text
        catalogue_number = "Catalogue number = " + pricing_details["catalogId"]
        samples = pricing_details["samples"]
        st.markdown("Availability:\n" + availability + "\n")
        for i in samples:
            pack_size = str(i["amount"]/1000)+"g"
            price = "$" + str(i["price"])
            p = Product(name=name, catalogue_number=catalogue_number, pack_size=pack_size, price=price, availability="")
            self.results.append(p)

    def search(self, search_term: str) -> str: # executes all methods      
        st.markdown(f"""## Enamine\nSearching for {search_term}...\n""")
        data = self.build_search_query(search_term)
        response = self.query_api(data)
        try: catalogue_number = self.find_catalogue_number(response)
        except:
            st.markdown("0 Results. CAS not found. \n")
        else:
            pricing_details = self.pricing_query(catalogue_number)
            price_details = self.output(pricing_details, response)
        

