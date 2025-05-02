import requests

API_url="https://www.themealdb.com/api/json/v1/1"

def find_meal_by_ingredient(ingredient):
    url=f"{API_url}/filter.php"
    query={"i": ingredient}
    response= requests.get(url, params=query)
    data= response.json()
    return data.get("meals",[])

def get_meal(meal_id):
    url=f"{API_url}/lookup.php"
    query={"i": meal_id}
    response=requests.get(url,params=query)
    data=response.json()
    return data["meals"][0] if data["meals"] else None
