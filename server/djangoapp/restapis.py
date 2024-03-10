import requests
import json
# import related models here
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    
    
    try:
        # Call get method of requests library with URL and parameters
        if "api_key" in kwargs:
            api_key = kwargs["api_key"]
            params = kwargs["params"]
            response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                        auth=HTTPBasicAuth('apikey', api_key))
        else:
            # no authentication GET
            response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    # json_data = json.dumps(json_payload, indent=4). << delete
    print(f"{json_payload}")
    try:
        # Call get method of requests library with URL and parameters
        response = requests.post(url, params=kwargs, json=json_payload)
    except Exception as e:
        # If any error occurs
        print("Network exception occurred")
        print(f"Exception: {e}")
    print(f"With status {response.status_code}")
    print(f"Response: {response.text}")

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer

            print("DEaler",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter

    json_result = get_request(url+str(dealerId))
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result
        
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review
            review_doc['sentiment'] = analyze_review_sentiments(review_doc["review"])
            print("Review",review_doc)
            # Create a DealerReview object with values in `doc` object
            review_obj = DealerReview(dealership=review_doc["dealership"], name=review_doc["name"], purchase=review_doc["purchase"],
                                   id=review_doc["id"], purchase_date=review_doc["purchase_date"], car_make=review_doc["car_make"],
                                   car_model=review_doc["car_model"],
                                   car_year=review_doc["car_year"],
                                   review=review_doc["review"],
                                   sentiment=review_doc["sentiment"])
            
            results.append(review_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(text):
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/ddbfc1e3-4a2b-4785-8d3b-390a0bb99294"  # Replace with the actual Watson NLU URL
    api_key = "In5SjFCwmg_ZMOcMobdUkx2J0r6m2rFkMga40unL2jjf"  # Replace with your actual API key
    version = "2019-07-12"  # Replace with the actual version
    features = "sentiment"
    return_analyzed_text = True

    params = {
        "text": text,
        "version": version,
        "features": features,
        "return_analyzed_text": return_analyzed_text
    }

    response = get_request(url, api_key=api_key, params=params)
    sentiment = response.get("sentiment", {}).get("document", {}).get("label", "Unknown")
    return sentiment

