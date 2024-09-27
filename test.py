from ecosystem import Ecosystem
from plant import Plant


# Example parameters for the plant
plant_1_params = {
    "type": "Sunflower",
    "min_lifespan": 3,
    "max_lifespan": 6,
    "min_resilience": 0.5,
    "max_resilience": 1.0,
    "min_growth_rate": 0.1,
    "max_growth_rate": 0.3,
    "min_reproduction_rate": 0.05,
    "max_reproduction_rate": 0.4
}

plant_2_params = {
    "type": "tree",
    "min_lifespan": 3,
    "max_lifespan": 6,
    "min_resilience": 0.5,
    "max_resilience": 1.0,
    "min_growth_rate": 0.1,
    "max_growth_rate": 0.3,
    "min_reproduction_rate": 0.5,
    "max_reproduction_rate": 0.9
}

# Random location on a 2D grid (example)
location = (4,4)

# Create plant instances
plants = []
plants.append(Plant((4,4), plant_1_params))
plants.append(Plant((10,10), plant_2_params))

flora_types = [plant.type for plant in plants]

params = {"plants": plants, "competition_constant": 0.1, "flora_types":flora_types}
# Example output to show its properties
desert = Ecosystem(50, params)

desert.animate(10)