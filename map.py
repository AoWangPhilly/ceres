import folium
import shapefile
import pandas as pd

m = folium.Map(location=[-28.2744, 135.7751], zoom_start = 4.5) # Creates the map focusing on Australia

# Reads in the shapefile of the Austrailian wildfires from https://firms.modaps.eosdis.nasa.gov/active_fire/#firms-shapefile
shape = shapefile.Reader("/Users/aowang/Downloads/MODIS_C6_Australia_NewZealand_24h/MODIS_C6_Australia_NewZealand_24h.shp")

@lru_cache()
def create_dataframe(data_set):
    """Creates a pandas dataframe from the shapefile, retrieving only the coordinates and intensity.
    """
    column_names = ["Coordinates", "Intensity"]
    coord, inten = [],[]
    df = pd.DataFrame(columns = column_names)
    for i in range(len(data_set.shapeRecords())):
        inten.append(data_set.shapeRecords()[i].__geo_interface__["properties"]["BRIGHT_T31"])
        coord.append(data_set.shapeRecords()[i].__geo_interface__["geometry"]["coordinates"])
    df["Coordinates"] = coord
    df["Intensity"] = inten
    return df

        
if __name__ == "__main__":
    print("Folium version:", folium.__version__) # 0.10.1

    wild_fire_df = create_dataframe(shape)
    for coord, inten in zip(wild_fire_df.Coordinates, wild_fire_df.Intensity):
        folium.Circle(
          location=[coord[1], coord[0]],
          radius=inten,
          color='crimson',
          fill=True,
          fill_color='crimson'
       ).add_to(m)
 
    m.save("australia_map.html")
    print("Done!")
    
    