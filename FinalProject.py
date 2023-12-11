import requests
import json

class TreeNode:
    def __init__(self, name):
        self.name = name
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def get_or_create_child(self, node_class, name):
        for child in self.children:
            if child.name == name:
                return child

        new_child = node_class(name)
        self.add_child(new_child)
        return new_child

    def serialize(self):
        return {
            "name": self.name,
            "children": [child.serialize() for child in self.children]
        }

class LocationNode(TreeNode):
    def __init__(self, name):
        super().__init__(name)
        self.cuisines = {}

    def add_cuisine(self, cuisine_name):
        if cuisine_name not in self.cuisines:
            new_cuisine_node = CuisineNode(cuisine_name)
            self.cuisines[cuisine_name] = new_cuisine_node
            self.add_child(new_cuisine_node)
        return self.cuisines

    def get_cusine(self, cuisine_name):
        return self.cuisines.get(cuisine_name, None)

    def serialize(self):
        data = super().serialize()
        data["cuisines"] = {k: v.serialize() for k, v in self.cuisines.items()}
        return data

class CuisineNode(TreeNode):
    def __init__(self, name):
        super().__init__(name)
        self.price_range = {}

    def add_price_range(self, price):
        if price not in self.price_range:
            new_price_node = PriceRangeNode(price)
            self.price_range[price] = new_price_node
            self.add_child(new_price_node)
        return self.price_range[price]

    def get_price_range(self, price):
        return self.price_range.get(price, None)

    def serialize(self):
        data = super().serialize()
        data["price_range"] = {k: v.serialize() for k, v in self.price_range.items()}
        return data

class PriceRangeNode(TreeNode):
    def __init__(self, name):
        super().__init__(name)
        self.restaurants = {}

    def add_restaurant(self, restaurant_name, details):
        if restaurant_name not in self.restaurants:
            self.restaurants[restaurant_name] = RestaurantNode(restaurant_name, details)
            self.add_child(self.restaurants[restaurant_name])

    def get_restaurant(self, restaurant_name):
        return self.restaurants.get(restaurant_name, None)

    def serialize(self):
        data = super().serialize()
        data["restaurants"] = {k: v.serialize() for k, v in self.restaurants.items()}
        return data

class RestaurantNode(TreeNode):
    def __init__(self, name, details):
        super().__init__(name)
        self.details = details

    def serialize(self):
        data = super().serialize()
        data["details"] = self.details
        return data

def get_restaurants_yelp(location):
    """
    Retrieves a list of restaurants from the Yelp API based on the specified location.

    Parameters:
        location (str): The location for which to find restaurants, e.g., a city name.

    Returns:
        dict: A JSON response containing restaurant data if the API call is successful.
        None is returned in case of a failed API call, with an error message printed to the console.
    """
    url = f"https://api.yelp.com/v3/businesses/search?location={location}"

    headers = {
        "accept": "application/json",
        "Authorization": "Bearer McWQwVTrS6ExSN69_OMmBcI-of7By4qW_rqe7nhJl7sLfCRZZYvnmoAP7tdLqG_x7JaA5TMMIfL1pImfCeXvi8Fd5sUSDq1KBWEOmp3oe2cvMc-h39JyBV8fZL1bZXYx"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data: {response.status_code}, {response.text}")
        return None

def locationSearch_tripAdvisor(searchQuery, location):
    url = f"https://api.content.tripadvisor.com/api/v1/location/search?key=8C3457B6333544CB9D708385EF296FA6&searchQuery={searchQuery}&address={location}&language=en"

    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            first_item = data['data'][0]
            location_id = first_item.get('location_id', None)
            return location_id
    else:
        print(f"Failed to fetch data: {response.status_code}, {response.text}")
        return None

def locationReview_tripAdvisor(locationID):
    url = f"https://api.content.tripadvisor.com/api/v1/location/{locationID}/reviews?key=8C3457B6333544CB9D708385EF296FA6&language=en"

    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'data' in data and len(data['data']) > 0:
            reviews = data.get('data', [])
            review_texts = [review.get('text', 'No review text found') for review in reviews]
            return review_texts
    else:
        print(f"Failed to fetch data: {response.status_code}, {response.text}")
        return None

def locationDetail_tripAdvisor(locationID):
    url = f"https://api.content.tripadvisor.com/api/v1/location/{locationID}/details?key=8C3457B6333544CB9D708385EF296FA6&language=en&currency=USD"

    headers = {
        "accept": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'ranking_data' in data and len(data['ranking_data']) > 0:
            ranking_string = data.get('ranking_data', []).get('ranking_string', None)
            return ranking_string

def get_tripAdvisor_reviews(restaurant, location):
    location_id = locationSearch_tripAdvisor(restaurant, location)
    if location_id:
        ranking_string = locationDetail_tripAdvisor(location_id)
        reviews = locationReview_tripAdvisor(location_id)
        return [ranking_string, reviews]
    else:
        return [None, None]

def populate_tree_yelp_data(location):
    yelp_data = get_restaurants_yelp(location)

    if not yelp_data or 'businesses' not in yelp_data:
        print("Invalid or empty Yelp data.")
        return None

    root = LocationNode(location)

    for business in yelp_data.get('businesses', []):
        location = business['location']['city']
        price_range = business.get('price', 'Unknown')
        cuisines = [category['title'] for category in business['categories']]

        location_node = root.get_or_create_child(LocationNode, location)

        for cuisine in cuisines:
            location_node.add_cuisine(cuisine)

            cuisine_node = location_node.get_cusine(cuisine)

            cuisine_node.add_price_range(price_range)

            price_node = cuisine_node.get_price_range(price_range)

            restaurant_details = {
                'name': business['name'],
                'rating': business.get('rating'),
                'address': ", ".join(business['location']['display_address']),
                'phone': business.get('display_phone'),
                'url': business['url']
            }

            price_node.add_restaurant(business['name'], restaurant_details)
            restaurant_node = price_node.get_restaurant(business['name'])
            restaurant_node.details = restaurant_details

    return root

def save_to_json_file(root_node, file_name):
    with open(file_name, 'w') as file:
        json.dump(root_node.serialize(), file, indent=4)

def find_restaurant_by_category(json_file, category, location, max_results=5):
    with open(json_file, 'r') as file:
        data = json.load(file)

    def search_category(node, category):
        if node['name'] == category:
            return node
        for child in node.get('children', []):
            result = search_category(child, category)
            if result is not None:
                return result
        return None

    category_node = search_category(data, category)

    restaurants_list = []

    if category_node:
        price_range_nodes = category_node.get('children', [])
        if not price_range_nodes:
            print(f"No restaurants found under the category '{category}'.")
            return []

        count = 0

        for price_range_node in price_range_nodes:
            for r in price_range_node.get('children', []):
                details = r.get('details', {})
                restaurant_info = {
                    'Restaurant Name': details.get('name'),
                    'Price Range': price_range_node.get('name'),
                    'Ranking': get_tripAdvisor_reviews(details.get('name'), location)[0],
                    'Address': details.get('address'),
                    'Phone': details.get('phone'),
                    'Rating': details.get('rating'),
                    'Website': details.get('url')
                }
                restaurants_list.append(restaurant_info)
                count += 1
                if count >= max_results:
                    return restaurants_list

    else:
        print(f"Category '{category}' not found.")
        return []

    return restaurants_list

def get_price_ranges_for_category(root, category):
    price_ranges = set()

    for location_node in root.children:
        for cuisine_node in location_node.children:
            if cuisine_node.name.lower() == category.lower():
                for price_node in cuisine_node.children:
                    price_ranges.add(price_node.name)

    return list(price_ranges)

def find_restaurant_by_category_and_price(root, category, price_range, location):
    restaurants_list = []

    for location_node in root.children:
        if location_node.name.lower() == location.lower():
            for cuisine_node in location_node.children:
                if cuisine_node.name.lower() == category.lower():
                    for price_range_node in cuisine_node.children:
                        if price_range is None or price_range_node.name == price_range:
                            for restaurant_node in price_range_node.children:
                                restaurant_details = restaurant_node.details
                                restaurants_list.append(restaurant_details)

    return restaurants_list

def main():
    print("Unsure about where to eat? Let this program help you choose the perfect restaurant!")

    while True:
        location = input("Next, please enter your location to help me find restaurants near you (e.g., 'San Francisco', 'New York'): ").strip()
        root = populate_tree_yelp_data(location)

        if root and root.children:
            save_to_json_file(root, f'restaurants_{location}.json')
            break
        else:
            print("Invalid location. Please try again.")

    while True:
        category = input("Do you have a cuisine category in mind? If so, please enter the cuisine category you're interested in: ").strip()

        specify_price = input("Would you like to specify a price range? (yes/no): ").strip().lower()
        price_range = None
        if specify_price == 'yes':
            price_ranges = get_price_ranges_for_category(root, category)
            if price_ranges:
                print(f"Available price ranges for {category}: {price_ranges}")
                price_range = input("Please enter your preferred price range: ").strip()
            else:
                print(f"No specific price ranges found for {category}. Showing all restaurants.")

        restaurants_info = find_restaurant_by_category_and_price(root, category, price_range, location)

        if restaurants_info:
            for r in restaurants_info:
                print()
                formatted_info = "\n".join([f"{key}: {value}" for key, value in r.items()])
                print(formatted_info)
                print()
            break
        else:
            print("No restaurants found for the specified criteria. Please try again.")

    while True:
        find_reviews = input("If you are interested in any of these restaurants, please enter the name for reviews, or type 'exit' to skip: ").strip()

        if find_reviews.lower() == "exit":
            break

        reviews = get_tripAdvisor_reviews(find_reviews, location)[1]
        print(" ")
        if reviews:
            for i, review in enumerate(reviews, start=1):
                print(f"Review {i}:\n{review}\n")
                print("----------\n")
        else:
            print("No reviews available for this restaurant.")

if __name__ == '__main__':
    main()