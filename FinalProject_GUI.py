import tkinter as tk
from tkinter import ttk
from FinalProjectJSON import save_to_json_file
from FinalProject import populate_tree_yelp_data, find_restaurant_by_category, find_restaurant_by_category_and_price, get_tripAdvisor_reviews, get_price_ranges_for_category

def find_restaurants():
    location = location_entry.get()
    category = category_entry.get()
    price_range = price_range_combobox.get() if price_range_combobox.get() != '' else None
    root = populate_tree_yelp_data(location)
    save_to_json_file(root, f'restaurants_{location}.json')
    json_file_path = f'restaurants_{location}.json'

    valid_price_ranges = get_price_ranges_for_category(root, category)

    if price_range and price_range not in valid_price_ranges:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "Selected price range is not valid for the chosen category.")
        return

    if price_range:
        # If a price range is specified, find restaurants within that price range
        restaurants_info = find_restaurant_by_category_and_price(json_file_path, category, price_range, location)
    else:
        # If no price range is specified, find restaurants without considering the price range
        restaurants_info = find_restaurant_by_category(json_file_path, category, location)
    # Clear existing results
    result_text.delete('1.0', tk.END)

    if restaurants_info:
        for r in restaurants_info:
                formatted_info = "\n".join([f"{key}: {value}" for key, value in r.items()])
                result_text.insert(tk.END, formatted_info + "\n\n")
    else:
        result_text.insert(tk.END, "No restaurants found for the specified criteria.")


def show_reviews():
    restaurant_name = review_entry.get()
    location = location_entry.get()
    reviews = get_tripAdvisor_reviews(restaurant_name, location)[1]
    # Clear existing reviews
    review_text.delete('1.0', tk.END)
    # Display reviews
    if reviews:
        for i, review in enumerate(reviews, start=1):
            formatted_review = f"Review {i}:\n{review}\n\n----------\n\n"
            review_text.insert(tk.END, formatted_review)
    else:
        review_text.insert(tk.END, "No reviews available for this restaurant.")

# Create the main window
window = tk.Tk()
window.title("Restaurant Finder")

# Create widgets
location_label = tk.Label(window, text="Location:")
location_entry = tk.Entry(window)

category_label = tk.Label(window, text="Cuisine Category:")
category_entry = tk.Entry(window)

price_range_var = tk.StringVar()
price_range_label = tk.Label(window, text="Price Range:")
price_range_combobox = ttk.Combobox(window, textvariable=price_range_var, values=["$", "$$", "$$$", "$$$$"])

find_button = tk.Button(window, text="Find Restaurants", command=find_restaurants)

scrollbar = tk.Scrollbar(window)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(window, height=10, width=75)

review_label = tk.Label(window, text="Restaurant for Reviews:")
review_entry = tk.Entry(window)

review_button = tk.Button(window, text="Show Reviews", command=show_reviews)

review_text = tk.Text(window, height=10, width=75)

# Layout widgets
location_label.pack()
location_entry.pack()

category_label.pack()
category_entry.pack()

price_range_label.pack()
price_range_combobox.pack()

find_button.pack()

result_text.pack()

scrollbar.config(command=result_text.yview)

review_label.pack()
review_entry.pack()

review_button.pack()

review_text.pack()

# Run the application
window.mainloop()
