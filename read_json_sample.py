import requests
import secrets as secrets
import json
import os
import re
import csv
from bs4 import BeautifulSoup
import plotly.graph_objects as go

api_key = secrets.API_KEY
base_url = "https://www.nps.gov"

def get_website_each_state():
    '''
    Collect the web url of all the states in USA

    Parameters
    ----------
        None

    Returns
    -------
        A dict which key is the name of state and the value is the list of web url of that state
    '''
    if os.path.exists("state_web.json"):
        with open("state_web.json", 'r') as f:
            state_web = json.load(f)
    else:
        state_web = {}
        web_list_each_state = BeautifulSoup(requests.get(base_url).text, 'html.parser').find(class_="dropdown-menu SearchBar-keywordSearch").find_all('a')

        for element in web_list_each_state:
            state_web[element.text.lower()] = base_url + element.get('href')


    if os.path.exists("state_web.json"):
        None
    else:
        with open("state_web.json", "w") as f:
            json.dump(state_web, f)

    return state_web


def each_park_url_in_one_state(state_web):
    '''
    Collect all the park url of one state

    Parameters
    ----------
        state_web: web url of the state(string)

    Returns
    -------
        A list of each park web url of one state
    '''
    site = BeautifulSoup(requests.get(state_web).text, 'html.parser').find('div',id="parkListResultsArea").find_all('h3')
    location = BeautifulSoup(requests.get(state_web).text, 'html.parser').find('div',id="parkListResultsArea").find_all('h4')
    location_list = []
    site_list = []
    park_web = []

    for element in location:
        location_list.append(element.text)
    for element in site:
        site_list.append(base_url + element.find('a').get('href') + "index.htm")

    park_web = site_list
    return park_web


def cache_park_url_of_each_state():
    '''
    Store all the park url of each state in a json file.

    Parameters
    ----------
        None

    Returns
    -------
        A dict whose key is the name of the state and the value is 
        all the park web url of that state
    '''
    if os.path.exists("park_web_state.json"):
        with open("park_web_state.json", 'r') as f:
            park_web_state = json.load(f)
    else:
        park_web_state = {}
        web_list_each_state = BeautifulSoup(requests.get(base_url).text, 'html.parser').find(class_="dropdown-menu SearchBar-keywordSearch").find_all('a')
        for element in web_list_each_state:
            state_web = get_website_each_state()[element.text.lower()]
            park_web_state[element.text.lower()] = each_park_url_in_one_state(state_web)

    if os.path.exists("park_web_state.json"):
        None
    else:
        with open("park_web_state.json", "w") as f:
            json.dump(park_web_state, f)
    return park_web_state


def park_data(park_web):
    '''
    collect data of one park

    Parameters
    ----------
        park_web: park wbe url(string)

    Returns
    -------
        A list contain all the data of that park
    '''
    params = {'api_key': secrets.API_KEY, 'parkCode': park_web.split('/')[3]}
    response = requests.get(f"https://developer.nps.gov/api/v1/parks", params).text
    data = json.loads(response)['data']
    return data


def cache_each_park_data():
    '''
    Store data of all the parks in USA in a json file
    Data include name, web url, description.etc

    Parameters
    ----------
        None

    Returns
    -------
        A dict whose key is the name of state and the value is a list.
        The list contain a dict whose value is the name of park and the
        value is all the data info of that park
    '''

    if os.path.exists("park_info.json"):
        with open("park_info.json", 'r') as f:
            park_info = json.load(f)
    else:
        park_info = {}
        name_list = list(cache_park_url_of_each_state().keys())# name of each state
        for x in name_list:
            park_url_list = cache_park_url_of_each_state()[x]
            park_data_dict = {}
            for y in park_url_list:
                a = park_data(y)
                if a == []:
                    None
                else:
                    park_name = a[0]['fullName']
                    park_data_dict[park_name] = a
            park_info[x] = park_data_dict

    if os.path.exists("park_info.json"):
        None
    else:
        with open("park_info.json", "w") as f:
            json.dump(park_info, f)
    return park_info


if __name__ == "__main__":
    '''
    Get all the data from the json file
    '''
    Data = cache_each_park_data()


    '''
    Get all the state name()
    '''
    State_name = list(Data.keys())
    print(State_name)
    print('\n')


    '''
    Get all the national park name in alabama
    '''
    Park_name = list(Data['alabama'].keys())# I use alabama as an example but you are free to change to another state
    print(Park_name)
    print('\n')


    '''
    Get all the data of one park
    '''
    Park_data = Data['alabama']['Birmingham Civil Rights National Monument'][0] #Birmingham Civil Rights National Monument is one of the national park in alabama,
    #you are free to change to another park
    print(Park_data)