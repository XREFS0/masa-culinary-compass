"""
MASA 19_Food Recipe Finder App Using Tkinter in Python with Source Code
Developer: MASA
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO


def search_recipe():
    food_name = entry.get().strip()
    if not food_name:
        return

    url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={food_name}"
    response = requests.get(url)
    data = response.json()

    for widget in results_container.winfo_children():
        widget.destroy()

    global recipes
    recipes = data["meals"]

    if not recipes:
        tk.Label(results_container, text="No recipes found.", font=("Helvetica", 14)).pack(pady=10)
        return

    for index, meal in enumerate(recipes):
        card_frame = tk.Frame(results_container, bg="white", bd=2, relief=tk.RIDGE)
        card_frame.pack(pady=5, padx=5, fill=tk.X)

        try:
            img_data = requests.get(meal["strMealThumb"]).content
            img = Image.open(BytesIO(img_data)).resize((100, 80))
            photo = ImageTk.PhotoImage(img)
        except:
            photo = None

        img_label = tk.Label(card_frame, image=photo, bg="white")
        img_label.image = photo
        img_label.pack(side=tk.LEFT, padx=5, pady=5)

        info_frame = tk.Frame(card_frame, bg="white")
        info_frame.pack(side=tk.LEFT, padx=5)

        tk.Label(info_frame, text=meal["strMeal"], font=("Helvetica", 14, "bold"), bg="white").pack(
            anchor="w"
        )
        tk.Label(
            info_frame,
            text=f"{meal['strCategory']} | {meal['strArea']}",
            font=("Helvetica", 11),
            bg="white",
            fg="gray",
        ).pack(anchor="w")

        btn = tk.Button(
            info_frame,
            text="View Recipe",
            bg="#ff6f61",
            fg="white",
            relief=tk.FLAT,
            command=lambda m=meal: show_recipe_detail(m),
        )
        btn.pack(pady=5, anchor="w")


def show_recipe_detail(meal):
    for widget in detail_container.winfo_children():
        widget.destroy()

    try:
        img_data = requests.get(meal["strMealThumb"]).content
        img = Image.open(BytesIO(img_data)).resize((300, 200))
        photo = ImageTk.PhotoImage(img)
        img_label = tk.Label(detail_container, image=photo, bg="white")
        img_label.image = photo
        img_label.pack(pady=5)
    except:
        pass

    tk.Label(detail_container, text=meal["strMeal"], font=("Helvetica", 18, "bold"), bg="white").pack(pady=5)
    tk.Label(
        detail_container,
        text=f"{meal['strCategory']} | {meal['strArea']}",
        font=("Helvetica", 12),
        fg="gray",
        bg="white",
    ).pack()

    canvas = tk.Canvas(detail_container, bg="white", highlightthickness=0)
    scrollbar = ttk.Scrollbar(detail_container, orient="vertical", command=canvas.yview)
    scroll_frame = tk.Frame(canvas, bg="white")
    scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    tk.Label(scroll_frame, text="🧂 Ingredients:", font=("Helvetica", 14, "bold"), bg="white").pack(
        anchor="w", pady=(10, 0)
    )
    for i in range(1, 21):
        ing = meal[f"strIngredient{i}"]
        meas = meal[f"strMeasure{i}"]
        if ing and ing.strip():
            tk.Label(scroll_frame, text=f"- {ing} ({meas})", font=("Helvetica", 12), bg="white").pack(
                anchor="w"
            )

    tk.Label(scroll_frame, text="\n📖 Instructions:", font=("Helvetica", 14, "bold"), bg="white").pack(
        anchor="w", pady=(10, 0)
    )
    tk.Label(
        scroll_frame,
        text=meal["strInstructions"],
        font=("Helvetica", 12),
        wraplength=500,
        justify="left",
        bg="white",
    ).pack(anchor="w")

    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


root = tk.Tk()
root.title("MASA Culinary Compass")
root.geometry("900x600")
root.config(bg="#f5f5f5")

top_frame = tk.Frame(root, bg="#f5f5f5")
top_frame.pack(pady=10)

entry = tk.Entry(top_frame, font=("Helvetica", 14), width=30)
entry.pack(side=tk.LEFT, padx=5)

search_btn = tk.Button(
    top_frame, text="Search", bg="#ff6f61", fg="white", font=("Helvetica", 12, "bold"), command=search_recipe
)
search_btn.pack(side=tk.LEFT, padx=5)

main_frame = tk.Frame(root, bg="#f5f5f5")
main_frame.pack(fill=tk.BOTH, expand=True)

results_container = tk.Frame(main_frame, bg="#f5f5f5")
results_container.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

detail_container = tk.Frame(main_frame, bg="white", bd=2, relief=tk.RIDGE)
detail_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
