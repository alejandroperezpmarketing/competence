
import prog_2023 as prog


dataset = prog.Vector()

print(type(dataset))

print(dataset)

# Setter
dataset.epsg = 4326

# Getter
print(dataset.epsg)

print(dataset)


dataset.read_csv('Numero', 'geo_point_2d', 'geo_point_2d', separator=';')








