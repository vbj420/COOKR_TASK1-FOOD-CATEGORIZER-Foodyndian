import tkinter as tk
from tkinter import messagebox
import csv
from difflib import get_close_matches

def load_data(filename):
    data = {}
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data[row['name'].lower()] = {
                'ingredients': row['ingredients'],
                'diet': row['diet'],
                'prep_time': int(row['prep_time']),
                'cook_time': int(row['cook_time']),
                'flavor_profile': row['flavor_profile'],
                'course': row['course'],
                'state': row['state'],
                'region': row['region']
            }
    return data

def search_item():
    item_name = entry.get().strip().lower()
    if item_name in food_data:
        details = food_data[item_name]
        diet_details = "Veg" if details["diet"] == "vegetarian" else "Non-Veg"
        
        prep_cook_time = details["prep_time"] + details["cook_time"]
        if 20 <= prep_cook_time <= 40:
            course_details = "Fast Food"
        else:
            course_details = details["course"]

        region_details = "North Indian Dish" if details["region"] in ["North", "West", "East"] else "South Indian Dish"

        flavor_details = ""
        if details["flavor_profile"] == "-1":
            flavor_details += "Diabetic Friendly"
        if "flour" in details["ingredients"].lower() or "Maida" in details["ingredients"].lower() or "poha" in details["ingredients"].lower():
            flavor_details += ", Baked Item"
        
        protein_rich_ingredients = ["beans", "chana", "dal", "paneer", "rice", "lentils"]
        if course_details == "snack" :
            all_details = f"{entry.get().strip().capitalize()} - {region_details}, {diet_details}, {course_details}, {flavor_details}"
        else :
          if any(ingredient in details["ingredients"].lower() for ingredient in protein_rich_ingredients):
            if flavor_details:
                flavor_details += ", Protein Rich"
            else:
                flavor_details = "Protein Rich"
          all_details = f"{entry.get().strip().capitalize()} - {region_details}, {diet_details}, {course_details}, {flavor_details}"
        
        # Add state to details if length is 3 or 4
        if len(all_details.split(", ")) == 3 or len(all_details.split(", ")) == 4:
            all_details += f", {details['flavor_profile']}"
        
        all_details = all_details.replace(", ,", ",").strip(", ")
        messagebox.showinfo("Item Details", all_details)
    else:
        # Find closest matches if item not found
        closest_matches = get_close_matches(item_name, food_data.keys(), n=5)
        closest_matches_str = "\n".join(closest_matches)
        messagebox.showinfo("Refer Closest Matches", f"Item '{entry.get().strip().capitalize()}' not found. Closest matches:\n\n{closest_matches_str}")

# Load data from CSV file
data_file = 'DATA.csv'
food_data = load_data(data_file)

# Create Tkinter GUI
root = tk.Tk()
root.title("Foodyndian")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

label = tk.Label(frame, text="Enter item name:")
label.grid(row=0, column=0)

entry = tk.Entry(frame)
entry.grid(row=0, column=1)

surf_button = tk.Button(frame, text="Surf Item", command=search_item)
surf_button.grid(row=1, columnspan=2, pady=10)

root.mainloop()
