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

def display_meal(meal):
    print(f"\n {meal['strMeal']}")
    print(f"Category: {meal['strCategory']}")
    print(f"Area: {meal['strArea']}")
    print(f"Instructions:\n{meal['strInstructions'][500]}...")
    print(f"Image: {meal['strMealThumb']}")
    print(f"Video Tutorial: {meal['strYoutube']}\n")
    
