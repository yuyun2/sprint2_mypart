import json
from faker import Faker
from collections import OrderedDict
import numpy as np
import requests 

fake     = Faker() 

def good_json():
        return json.dumps(OrderedDict([  
            ('name', fake.last_name()),
            ('prop', OrderedDict(
                        [('age', np.random.randint(1,101)),
                         ('zip', fake.postalcode()),
                         ('DMID', np.random.randint(100000, 1000000))]))]))

def missing_one_index():
    json = good_json()
    index = np.random.randint(0,len(json))
    badjson = json[:index] + json[index + 1:]
    return badjson

def missing_value():
    prob = float(np.random.uniform(0.0,1.0))
    blob = json.loads(good_json())
    if prob > 0.5:
        json['name'] == None
    
    else:
        json['prop']['age'] == None
    return json.dumps(blob)

def delete_keys_from_dict(dict_del, lst_keys):
    for k in lst_keys:
        try:
            del dict_del[k]
        except KeyError:
            pass
    for v in dict_del.values():
        if isinstance(v, dict):
            delete_keys_from_dict(v, lst_keys)

    return dict_del 

def missing_keys():
    prob = np.random.uniform(0.0,1.0)
    blob = json.loads(good_json())
    if prob > 0.5:
        return json.dumps(delete_keys_from_dict(blob, ['name']))
    else:
        return json.dumps(delete_keys_from_dict(blob, ['age']))



def wrong_punctuation():
    badjson = good_json().replace(":", ',', np.random.randint(1,5))
    return badjson 

def which_json():
    good_prob = np.random.uniform(0.0,1.0)
    bad_prob = 1-good_prob
    
    if good_prob > 0.5:
        return good_json()
    elif 1.0 <= bad_prob <= 2.0:
        return missing_one_index()
    elif 2.0 <= bad_prob <= 3.0:
        return missing_value()
    elif 3.0 <= bad_prob <= 4.0:
        return missing_keys()
    elif 4.0 <= bad_prob <= 5.0:
        return wrong_punctuation()


json_blob = which_json()


#url = 'http://127.0.0.1:8080/'
url = 'http://ec2-35-166-134-236.us-west-2.compute.amazonaws.com:8080/'

headers = {'Content-Type': 'application/json'}
data = json_blob
params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1} 

requests.post(url, params=params, data=json_blob, headers=headers)


