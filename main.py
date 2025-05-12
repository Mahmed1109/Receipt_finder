import requests
from collections import defaultdict

API_url = "https://www.themealdb.com/api/json/v1/1"

def find_meal_by_ingredient(ingredients):
    ingredient_list = [i.strip().lower() for i in ingredients.split(",")]
    all_meal_sets = []
    first_meal_map = {}
    match_count = defaultdict(int)

    for ing in ingredient_list:
        url = f"{API_url}/filter.php"
        query = {"i": ing}
        try:
            response = requests.get(url, params=query)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            print(f"⚠️ Error fetching meals for ingredient: {ing}")
            continue

        meals = data.get("meals", [])
        if not meals:
            continue

        meal_ids = set()
        for meal in meals:
            meal_id = meal["idMeal"]
            meal_ids.add(meal_id)
            first_meal_map[meal_id] = meal
            match_count[meal_id] += 1

        all_meal_sets.append(meal_ids)

    if not all_meal_sets:
        return []

    common_ids = set.intersection(*all_meal_sets) if len(all_meal_sets) == len(ingredient_list) else set()

    if common_ids:
        return [first_meal_map[mid] for mid in common_ids]

    # No full match: suggest meals with highest match count
    print("\n⚠️ No meals found that use ALL the ingredients.")
    print("🔎 Suggesting meals that match SOME of them...\n")
    sorted_suggestions = sorted(match_count.items(), key=lambda x: -x[1])
    top_matches = sorted_suggestions[:5]

    suggestions = [first_meal_map[meal_id] for meal_id, _ in top_matches]
    return suggestions

def get_meal(meal_id):
    url = f"{API_url}/lookup.php"
    query = {"i": meal_id}
    try:
        response = requests.get(url, params=query)
        response.raise_for_status()
        data = response.json()
        return data["meals"][0] if data["meals"] else None
    except requests.RequestException:
        print("⚠️ Failed to retrieve meal details.")
        return None

def display_meal(meal):
    print(f"\n🍽️ {meal['strMeal']}")
    print(f"Category: {meal['strCategory']}")
    print(f"Area: {meal['strArea']}")
    print(f"Instructions:\n{meal['strInstructions'][:500]}...")
    print(f"Image: {meal['strMealThumb']}")
    print(f"Video Tutorial: {meal['strYoutube']}\n")

def main():
    print("🥘 Recipe Finder based on Ingredients!")
    ingredients = input("Enter ingredients (comma-separated): ").strip()
    meals = find_meal_by_ingredient(ingredients)

    if not meals:
        print("❌ No meals found with the ingredients you provided.")
        return

    print(f"\n✅ Found {len(meals)} meal(s) using: {ingredients}\n")
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
