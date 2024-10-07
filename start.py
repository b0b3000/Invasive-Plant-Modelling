from ecosystem import Ecosystem
from plant import Plant
import presets

native_species_params = presets.plant_1_params
native_species_layout = presets.layout_2
invasive_species_params = presets.plant_2_params
invasive_species_layout = presets.layout_1

timesteps = 40
size = 50

# Create plant instances
plants = []

for location in native_species_layout:
    plants.append(Plant(location, native_species_params))

for location in invasive_species_layout:
    plants.append(Plant(location, invasive_species_params))

flora_types = [native_species_params["type"], invasive_species_params["type"]]

params = {"plants": plants, "competition_constant": 0.1, "flora_types":flora_types}
# Example output to show its properties
desert = Ecosystem(size, params)

desert.animate(timesteps)