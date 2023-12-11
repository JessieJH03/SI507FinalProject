## Tree Structure for Restaurant and Review Data
1. **Root Node:** The root of the tree represents the entire dataset of restaurants. 
2. **Level 1 Nodes** – Location: Each node at this level represents a specific location (city/state). This helps in filtering restaurants by geographical preferences.
  - Child Nodes: Cuisine categories within that location.
3. **Level 2 Nodes** – Cuisine: Under each location node, create nodes for each type of cuisine (e.g., Mexican, Italian). This allows for filtering by food preferences.
  - Child Nodes: Price range categories for the specified cuisine and location. 
5.	**Level 3 Nodes** – Price Range: For each cuisine node, create child nodes for different price ranges (e.g., $, $$, $$$). This categorizes restaurants by affordability.
  - Child Nodes: Individual restaurants matching the location, cuisine, and price range criteria. 
6.	**Level 4 Nodes** – Restaurant Details: These nodes contain detailed information about each restaurant. 

# Example Tree Structure
![image](https://github.com/JessieJH03/SI507FinalProject/assets/124538427/f5525199-9c51-4605-b024-12d09ade3470)
