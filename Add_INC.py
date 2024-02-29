import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
from collections import Counter
nv = 0
p=0
def load_data(filename):
    data = []
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append([row['name'], row['ingredients'], row['diet'], row['prep_time'], row['cook_time'], row['flavor_profile'], row['course'], row['state'], row['region']])
    return data

def preprocess_data(data):
    return [[row[1].lower(), row[2], int(row[3]), int(row[4]), row[5], row[6], row[7], row[8]] for row in data]

def compare_ingredients(new_ingredients, existing_items):
    closest_matches = []
    r= []
    r = new_ingredients[0].split(',')
    new_ingredients = []
    for i in r :
        new_ingredients.append(i.strip())
    print(new_ingredients)
    for item in existing_items:
        item_ingredients = item[0].lower().split(", ")
        similarity = sum(1 for word in new_ingredients if word.lower() in item_ingredients)
        closest_matches.append((item, similarity))
    closest_matches.sort(key=lambda x: x[1], reverse=True)
    return closest_matches[:4]

def predict_details(closest_matches, new_name):
    global nv 
    global p
    
    # Predict diet (majority class)
    diet_counts = Counter(details[1] for details, _ in closest_matches)
    predicted_diet = max(diet_counts, key=diet_counts.get)
    # Predict region (majority class)
    if nv ==1:
        predicted_diet = "Non-veg"
    region_counts = Counter(details[7] for details, _ in closest_matches)
    predicted_region = max(region_counts, key=region_counts.get)
    # Predict protein-rich
    protein_rich = any('beans' in details[1] or 'chana' in details[1] or 'dal' in details[1] or 'paneer' in details[1] or 'rice' in details[1] or 'lentils' in details[1] for details, _ in closest_matches)
    if  p==1:
        protein_rich = "Yes"
    return f"Name: {new_name.capitalize()}\nRegion: {predicted_region}\nDiet: {predicted_diet}\nProtein Rich: {'Yes' if protein_rich else 'No'}"

def add_item():
    global nv 
    global p
    new_name = simpledialog.askstring("Add New Item", "Enter the name of the new dish:")
    if new_name:
        new_ingredients = simpledialog.askstring("Add New Item", f"Enter the ingredients for '{new_name}':")
        if new_ingredients:
            new_ingredients_list = new_ingredients.split(", ")  # Assuming ingredients are comma-separated
            closest_matches = compare_ingredients(new_ingredients_list, food_data)
            if  "Chicken" in new_ingredients or "Mutton" in new_ingredients or "Fish" in new_ingredients  :
                nv=1
            if "Chana dal" in new_ingredients and "Finger Millet" in new_ingredients :
                p=1 
                #print("hell0o")
            if closest_matches:
                predicted_details = predict_details(closest_matches, new_name)
                messagebox.showinfo("Predicted Details", predicted_details)
            else:
                messagebox.showerror("Error", "No matches found for the entered ingredients.")
        else:
            messagebox.showerror("Error", "No ingredients provided.")
    else:
        messagebox.showerror("Error", "No name provided.")

# Load data from CSV file
data_file = 'DATA.csv'
food_data = load_data(data_file)
food_data = preprocess_data(food_data)

# Create Tkinter GUI
root = tk.Tk()
root.title("Foodyndian")

frame = tk.Frame(root)
frame.pack(padx=30, pady=20)



add_button = tk.Button(frame, text="Add Item", command=add_item)
add_button.grid(row=1, columnspan=2, pady=10)

root.mainloop()
