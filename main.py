import requests

API_url="https://www.themealdb.com/api/json/v1/1"

def find_meal_by_ingredient(ingredient):
    url=f"{API_url}/filter.php"
    query={"i": ingredient}
    response= requests.get(url, params=query)
    data= response.json()
    return data.get("meals",[])
