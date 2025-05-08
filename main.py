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


def main():
    print("Recipe Finder based on Ingredient!:")
    ingredient= input("Enter an ingredient: ").strip()

    meals=find_meal_by_ingredient(ingredient)

    if not meals:
        print("No meals found with the ingredient you have inputed")
        return


    print(f"\n Found {len(meals)} meal(s) with '{ingredient}' :\n")
    for idx, meal in enumerate(meals, 1):
        print(f"{idx}. {meal['strMeal']} (ID: {meal['idMeal']})")  

    while True:
        choice = input("\nEnter the number of the meal you want details for: ").strip()
        
        if choice.isdigit() and 1 <= int(choice) <= len(meals[:5]):
            meal_id = meals[int(choice) - 1]["idMeal"]
            meal_details = get_meal(meal_id)
            if meal_details:
                display_meal(meal_details)
            break 
        else:
            print("⚠️ Invalid input. Please enter a number from the list.")

if __name__=="__main__":
    main()
