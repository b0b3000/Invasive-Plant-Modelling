from ecosystem import Ecosystem
from plant import Plant


# Example parameters for the plant
plant_params = {
    "type": "Sunflower",
    "min_lifespan": 3,
    "max_lifespan": 6,
    "min_resilience": 0.5,
    "max_resilience": 1.0,
    "min_growth_rate": 0.1,
    "max_growth_rate": 0.3,
    "min_reproduction_rate": 0.05,
    "max_reproduction_rate": 0.2
}

# Random location on a 2D grid (example)
location = (4,4)

# Create a plant instance
new_plant = Plant(location, plant_params)

params = {"plants": [new_plant]}
# Example output to show its properties
desert = Ecosystem(50, params)

desert.animate(10)