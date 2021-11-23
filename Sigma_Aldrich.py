from Website import Website as Web
from Product import Product
from MLStripper import strip_tags
import requests
import json
from datetime import datetime
import streamlit as st

class Sigma_Aldrich(Web):

    def build_search_query(self, search_term: str) -> str:
            """ Builds the query to search for. Params: the search key - eg. "497-23-4"
            Returns a json string of the query"""
            data = {"operationName":"ProductSearch","variables":{"searchTerm":search_term,"page":1,"group":"substance","selectedFacets":[],"sort":"relevance","type":"PRODUCT"},"query":"query ProductSearch($searchTerm: String, $page: Int!, $sort: Sort, $group: ProductSearchGroup, $selectedFacets: [FacetInput!], $type: ProductSearchType, $catalogType: CatalogType, $orgId: String, $region: String, $facetSet: [String]) {  getProductSearchResults(input: {searchTerm: $searchTerm, pagination: {page: $page}, sort: $sort, group: $group, facets: $selectedFacets, type: $type, catalogType: $catalogType, orgId: $orgId, region: $region, facetSet: $facetSet}) {    ...ProductSearchFields    __typename  }}fragment ProductSearchFields on ProductSearchResults {  metadata {    itemCount    setsCount    page    perPage    numPages    redirect    __typename  }  items {    ... on Substance {      ...SubstanceFields      __typename    }    ... on Product {      ...SubstanceProductFields      __typename    }    __typename  }  facets {    key    numToDisplay    isHidden    isCollapsed    multiSelect    prefix    options {      value      count      __typename    }    __typename  }  didYouMeanTerms {    term    count    __typename  }  __typename}fragment SubstanceFields on Substance {  _id  id  name  synonyms  empiricalFormula  linearFormula  molecularWeight  aliases {    key    label    value    __typename  }  images {    sequence    altText    smallUrl    mediumUrl    largeUrl    __typename  }  casNumber  products {    ...SubstanceProductFields    __typename  }  match_fields  __typename}fragment SubstanceProductFields on Product {  name  productNumber  productKey  cardCategory  cardAttribute {    citationCount    application    __typename  }  attributes {    key    label    values    __typename  }  speciesReactivity  brand {    key    erpKey    name    color    __typename  }  images {    altText    smallUrl    mediumUrl    largeUrl    __typename  }  description  sdsLanguages  sdsPnoKey  similarity  paMessage  features  catalogId  materialIds  __typename}"}
            return json.dumps(data)

#     def build_substance_query(self, product_id: str, catalog_type: str) -> str:
#         """Builds a query for the substance API. Params: the product id eg. "25hfuranone8407497234", and cataloge type eg. "sial"
#         Returns a json string of the query"""
#         data = {"operationName":"ProductSearch","variables":{"searchTerm":search_term,"page":1,"group":"substance","selectedFacets":[],"sort":"relevance","type":"PRODUCT", "catalogType":"buildingblocks"},"query":"query ProductSearch($searchTerm: String, $page: Int!, $sort: Sort, $group: ProductSearchGroup, $selectedFacets: [FacetInput!], $type: ProductSearchType, $catalogType: CatalogType, $orgId: String, $region: String, $facetSet: [String]) { getProductSearchResults(input: {searchTerm: $searchTerm, pagination: {page: $page}, sort: $sort, group: $group, facets: $selectedFacets, type: $type, catalogType: $catalogType, orgId: $orgId, region: $region, facetSet: $facetSet}) { ...ProductSearchFields __typename }}fragment ProductSearchFields on ProductSearchResults { metadata { itemCount setsCount page perPage numPages redirect __typename } items { ... on Substance { ...SubstanceFields __typename } ... on Product { ...SubstanceProductFields __typename } __typename } facets { key numToDisplay isHidden isCollapsed multiSelect prefix options { value count __typename } __typename } didYouMeanTerms { term count __typename } __typename}fragment SubstanceFields on Substance { _id id name synonyms empiricalFormula linearFormula molecularWeight aliases { key label value __typename } images { sequence altText smallUrl mediumUrl largeUrl __typename } casNumber products { ...SubstanceProductFields __typename } match_fields __typename}fragment SubstanceProductFields on Product { name productNumber productKey cardCategory cardAttribute { citationCount application __typename } attributes { key label values __typename } speciesReactivity brand { key erpKey name color __typename } images { altText smallUrl mediumUrl largeUrl __typename } description sdsLanguages sdsPnoKey similarity paMessage features catalogId materialIds __typename}"}
#         return json.dumps(data)

    def build_pricing_query(self, product_number: str, material_ids: list, brand: str, catalog_type: str) -> str:
            """Builds a query for the pricing API.Params product number, list of material ids, and catalog type
            Returns a json string of the query"""
            data = {"operationName":"PricingAndAvailability","variables":{"displaySDS":False,"productNumber":product_number,"materialIds":material_ids,"brand":brand,"quantity":1,"catalogType":catalog_type,"orgId":"null","checkForPb":True},"query":"query PricingAndAvailability($productNumber: String!, $brand: String, $quantity: Int!, $catalogType: CatalogType, $checkForPb: Boolean, $orgId: String, $materialIds: [String!], $displaySDS: Boolean = false) {  getPricingForProduct(input: {productNumber: $productNumber, brand: $brand, quantity: $quantity, catalogType: $catalogType, checkForPb: $checkForPb, orgId: $orgId, materialIds: $materialIds}) {  ...ProductPricingDetail    __typename  }}fragment ProductPricingDetail on ProductPricing {  productNumber  country  materialPricing {   ...ValidMaterialPricingDetail    __typename  }  discontinuedPricingInfo {    ...DiscontinuedMaterialPricingDetail    __typename  }  dchainMessage  __typename}fragment ValidMaterialPricingDetail on ValidMaterialPricing {  brand  type  currency  listPriceCurrency  listPrice  shipsToday  freeFreight  sdsLanguages  catalogType  materialDescription  materialNumber  netPrice  packageSize  price  product  quantity  isPBAvailable  vendorSKU  availabilities {    ...Availabilities    __typename  }  additionalInfo {    ...AdditionalInfo    __typename  }  promotionalMessage {    ...PromotionalMessage    __typename  }  ... @include(if: $displaySDS) {    sdsLanguages    __typename  }  __typename}fragment Availabilities on MaterialAvailability {  date  key  plantLoc  quantity  displayFromLink  displayInquireLink  contactInfo {    contactPhone    contactEmail    __typename  }  availabilityOverwriteMessage {    messageKey    messageValue    messageVariable1    messageVariable2    messageVariable3    __typename  }  supplementaryMessage {    messageKey    messageValue    messageVariable1    messageVariable2    messageVariable3    __typename  }  __typename}fragment AdditionalInfo on CartAdditionalInfo {  carrierRestriction  unNumber  tariff  casNumber  jfcCode  pdcCode  __typename}fragment PromotionalMessage on PromotionalMessage {  messageKey  messageValue  messageVariable1  messageVariable2  messageVariable3  __typename}fragment DiscontinuedMaterialPricingDetail on DiscontinuedMaterialPricing {  errorMsg  paramList  hideReplacementProductLink  displaySimilarProductLabel  hideTechnicalServiceLink  replacementProducts {    ...ReplacementProductDetail    __typename  }  alternateMaterials {    ...AlternateMaterialDetail    __typename  }  __typename}fragment ReplacementProductDetail on Product {  productNumber  name  description  sdsLanguages  images {    mediumUrl    altText    __typename  }  brand {    key    erpKey    name    logo {      smallUrl      altText      __typename    }    __typename  }  __typename}fragment AlternateMaterialDetail on Material {  number  __typename}"}
            return json.dumps(data)

    def start_session(self, ) -> requests.session:
            """Wrapper for requests session"""
            url = "https://www.sigmaaldrich.com"
            headers = {
                    "User-Agent":
                    "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36",
                    "accept": "*/*",
                    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                    "content-type": "application/json",
                    "sec-ch-ua":
                    "\"Google Chrome\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"",
                    "sec-ch-ua-mobile": "?1",
                    "sec-ch-ua-platform": "\"Android\"",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "x-gql-access-token": "006470b1-02a3-11ec-819a-f11160011a2a", # see note -> maybe randomly generate the access token
                    "x-gql-country": "FR",
                    "x-gql-language": "en",
                    "x-gql-operation-name": "SubstanceDetails", # see note
            }
            """" Note - headers sets the operationName and access-token
            but they don't seem to be used or respected by the API (but are required). 
            One to watch if it stops working - just set them based on the below / data query """

            s = requests.session()
            s.headers.update(headers)
            r = s.get(url) # Fetches initial cookies
            return s

    def post_api(self, s: requests.session, data: str) -> json:
            api_url = "https://www.sigmaaldrich.com/api"
            p = s.post(api_url, data=data)
            return p.json()

    def query_api(self, search_term: str):
            """Wrapper querys Sigma API for data. Parameters: The data query json string - contains the query type"""
            s = self.start_session()

            # This is the place to start - returns the a list of products that match your query ("items")
            # Each product has a product Id, eg. "25hfuranone8407497234" - and catalogue Id e.g "sial"
            # These can be used in the substance API if needed
            # Each product then has a list of "materialIds", productKey, brand 
            # These can then used in the pricing API 
            search_query = self.build_search_query(search_term)
            products = self.post_api(s, search_query)
            return products
            #print(products)

    def output(self, products):
            s = self.start_session()
            # Parsing the dict to pass to other API requests
            items = products["data"]["getProductSearchResults"]["items"]
            if items ==[]:
                st.markdown("CAS not found")
            st.markdown(f"{len(items)} catalogue items found.")
            for i in items:
                    product_id = i["id"]
                    name = strip_tags(i["name"])
                    sub_products = i["products"]
                    for k in sub_products:
                            brand = k["brand"]["key"]
                            catalog_id = k["catalogId"]
                            product_number = k["productNumber"]
                            description = str(strip_tags(k["description"])) + ", "
                            catalogue_numbers = k["materialIds"]

                            pricing_query = self.build_pricing_query(product_number, catalogue_numbers, brand, catalog_id)
                            pricing = self.post_api(s, pricing_query)
                            try:
                                prices = pricing["data"]["getPricingForProduct"]["materialPricing"]
                            except: 
                                st.markdown("No pricing data available")                            
                            else: 
                                for i in prices:
                                    catalogue_number = "Catalogue number = " + str(i["materialNumber"])
                                    price = "€" + str(i["price"])
                                    availabilities = i["availabilities"] 
                                    pack_size = i["packageSize"]
                                    
                                    for i in availabilities:
                                        date = int(i["date"])/1000
                                        unix_date = datetime.utcfromtimestamp(date).strftime('%d-%m-%y')
                                        key = i["key"].replace("_", " ").lower()
                                        shipping_date = str(key) + ": " + str(unix_date)
                                        if shipping_date == "only few left in stock: 01-01-70":
                                            pass
                                        else:
                                            availability = shipping_date
                                    p = Product(name=name, description = description, catalogue_number=catalogue_number, pack_size=pack_size, price=price, availability=availability)
                                    self.results.append(p)


    def search(self, search_term):
        st.write(f"""## Sigma Aldrich \nSearching for {search_term}...\n""")
        product_list = self.query_api(search_term)
        self.output(product_list)
                
# search_term = "497-23-4"
# # #search_term = "74-88-4"
# # # search_term = "22122-36-7" 
# # # search_term = "51673-83-7" # Building block explorer
# # # search_term = "45-125-15478" #Not valid CAS
# # #search_term = "110-86-1" # pyridine

# def CAS_Searcher(search_term):
#     sigma_aldrich = Sigma_Aldrich()
#     sigma_aldrich.search(search_term)
#     n = sigma_aldrich.get_results()
#     for i in n:
#         print(i)
        
# CAS_Searcher(search_term)


