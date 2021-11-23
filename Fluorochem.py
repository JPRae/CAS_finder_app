import requests
import json
import pandas as pd
from Website import Website as Web
from Product import Product
import streamlit as st


class Fluorochem(Web):

    def build_search_query(self, search_term: str)-> str: #builds payload for request
        data = {"lstSearchType":"C","txtSearchText":search_term,"showPrices":False,"showStructures":False,"groupFilters":[]}
        return json.dumps(data)

    def query_api(self, json_data: str) -> str: # makes request, returns a list of prodCodes
        url = "http://www.fluorochem.co.uk/Products/Search"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
                "Accept": "text/html, */*; q=0.01",
                "Accept-Language": "en-GB,en;q=0.5",
                "Content-Type": "application/json",
                "X-Requested-With": "XMLHttpRequest",
                "Cache-Control": "max-age=0"}    
        response = requests.post(url, headers = headers, data=json_data)
        #print(response) #useful for confirming the response
        catalogue_results = pd.read_html(response.text, converters={"Cat Num":str})
        catalogue_results_df = catalogue_results[0]
        prodCode_list = [item for item in catalogue_results_df["Cat Num"]]
        st.write(str(len(prodCode_list)) + " catalogue items found.")
        return prodCode_list

    def build_pricing_query(self, prodCode_list: str) -> str: #builds payload for request
        json_product_request_data_list = [json.dumps({"prodCode":prodCode_list[item]}) for item in range(len(prodCode_list))]
        return json_product_request_data_list

    def product_details_request(self, json_product_request_data_list: str) -> str: #makes product detail request, returns a list of responses
        product_request_header = {"accept": "text/html, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json",
        "x-requested-with": "XMLHttpRequest"}
        product_url = "http://www.fluorochem.co.uk/Products/Product-Detail"
        response = requests.post(product_url, headers = product_request_header, data=json_product_request_data_list[0])
        response_list = [requests.post(product_url, headers = product_request_header, data=json_product_request_data_list[item]) for item in range(len(json_product_request_data_list))]
        return response_list

    def output(self, response_list: str, CatCode_list) -> str: #parses the responses
        for item in range(len(response_list)):
            product_details_table = pd.read_html(response_list[item].text, attrs = {'id': 'tbdDetails'})
            product_details_df = product_details_table[0]
            name = product_details_df[0][0]
            pricing_table = pd.read_html(response_list[item].text, attrs = {'id': 'tblPricing'})
            pricing_table_df = pricing_table[0]
            catalogue_number = "Catalogue number = " + (CatCode_list[item])
            for i in range(len(pricing_table_df)):
                pack_size = pricing_table_df["Size"][i]
                price = pricing_table_df["Price"][i]
                availability = str(pricing_table_df["Stock"][i]) + " in stock,"
                p = Product(name=name, catalogue_number=catalogue_number, pack_size=pack_size, price=price, availability=availability)
                self.results.append(p)

    def search(self, search_term: str) -> str: # executes all methods
        st.write(f"""## Fluorochem\nSearching for {search_term}...\n""")
        search_query = self.build_search_query(search_term)
        try: CatCode_list = self.query_api(search_query)
        except:
            st.markdown("0 Results. CAS not found. \n")
        else:
            product_query_list = self.build_pricing_query(CatCode_list)
            prod_details_list = self.product_details_request(product_query_list)
            price_details = self.output(prod_details_list, CatCode_list)

    # def search(self, search_term: str) -> str: # executes all methods
    #     print(f"\n\n______________________________\n\nFluorochem\nSearching for {search_term}...")
    #     search_query = self.build_search_query(search_term)
    #     try: CatCode_list = self.query_api(search_query)
    #     except:
    #         print("0 Results. CAS not found. \n")
    #     else:
    #         product_query_list = self.build_pricing_query(CatCode_list)
    #         prod_details_list = self.product_details_request(product_query_list)
    #         price_details = self.output(prod_details_list, CatCode_list)