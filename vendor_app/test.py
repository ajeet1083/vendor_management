import requests
import json


URL = ""

def get_data(id=None):
    data = {
        'name' : 'vendor1'
        'contact_details' : 'vendor1'
        'address' : 'vendor1'
        'vendor_code' : 'vendor1'
        'on_time_delivery_rate' : 'vendor1'
        'quality_rating_avg' : 'vendor1'
        'average_response_time' : ''
        'fulfillment_rate' : '4'
    }
    if id is not None:
        data = {'id' : id}
        json_data = json.dumps(data)
    req = requests.post(url= URL, data = json_data)
    data = req.json()
    print(data)
    
    
get_data(1)