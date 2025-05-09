import requests

API_url = "https://www.themealdb.com/api/json/v1/1"

def find_meal_by_ingredient(ingredients):
    ingredient_list = [i.strip() for i in ingredients.split(",")]
    all_meal_sets = []
    first_meal_map = {}

    for ing in ingredient_list:
        url = f"{API_url}/filter.php"
        query = {"i": ing}
        response = requests.get(url, params=query)
        data = response.json()
        meals = data.get("meals", [])

        if not meals:
            return []  # No meals found for this ingredient, abort

        meal_ids = set()
        for meal in meals:
            meal_ids.add(meal["idMeal"])
            first_meal_map[meal["idMeal"]] = meal  # store meal for later use

        all_meal_sets.append(meal_ids)

    # Intersect the meal IDs to find meals that contain ALL ingredients
    common_ids = set.intersection(*all_meal_sets)

    if not common_ids:
        return []

    # Return the meals that match the common IDs
    return [first_meal_map[mid] for mid in common_ids]

def get_meal(meal_id):
    url = f"{API_url}/lookup.php"
    query = {"i": meal_id}
    response = requests.get(url, params=query)
    data = response.json()
    return data["meals"][0] if data["meals"] else None

def display_meal(meal):
    print(f"\n{meal['strMeal']}")
    print(f"Category: {meal['strCategory']}")
    print(f"Area: {meal['strArea']}")
    print(f"Instructions:\n{meal['strInstructions'][:500]}...")
    print(f"Image: {meal['strMealThumb']}")
    print(f"Video Tutorial: {meal['strYoutube']}\n")

def main():
    print("Recipe Finder based on Ingredients!")
    ingredients = input("Enter ingredients (comma-separated): ").strip()
    meals = find_meal_by_ingredient(ingredients)

    if not meals:
        print("No meals found that use all the ingredients you provided.")
        return

    print(f"\nFound {len(meals)} meal(s) using: {ingredients}\n")
    for idx, meal in enumerate(meals[:5], 1):
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

if __name__ == "__main__":
    main()
