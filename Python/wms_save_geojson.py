import requests

# GeoServer WMS GetMap request parameters
wms_url = "http://지오서버주소/geoserver/ows?"
params = {
    "SERVICE": "WMS",
    "REQUEST": "GetMap",
    "VERSION": "1.1.0",
    "LAYERS": "workspace:3_TYPHN_20220530T1549_TYPHN_NO1DMG",
    "WIDTH": "800",
    "HEIGHT": "800",
    "CRS": "EPSG:4326",
    "BBOX": "-180,-90,180,90",
    "FORMAT": "geojson"
}


# Make a GET request to GeoServer WMS
response = requests.get(wms_url, params=params)
# Check if the request was successful
if response.status_code == 200:
    # Save the CSV data to a file
    with open("output.geojson", "wb") as f:
        f.write(response.content)
    print("geojson file downloaded successfully.")
else:
    print(f"Failed to download CSV file. Status code: {response.status_code}")
