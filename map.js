const initCoords = [44, -89];

var map = loadMap("humanitarian");
var coordless = loadMarkers();

coordless.forEach((org) => console.log(`No coords for ${org.NAME}`));
console.log(`There are ${coordless.length} organizations without coords`);

addGeo(testData, getZipStyle())

// initialize map with tile layer
// http://leaflet-extras.github.io/leaflet-providers/preview/
function loadMap(mapType) {
    switch (mapType) {
        case "humanitarian":
            tilesURL = "https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png";
            break;
        default:
            tilesURL = "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
    }

    let newMap = new L.map("map", {
        center: initCoords,
        zoom: 8
    });
    newMap.addLayer(new L.TileLayer(tilesURL));
    return newMap;
}

// adds markers to map and returns an array of organizations that could not be marked
function loadMarkers() {
    coordless = [];
    data.forEach((org) => {
        if (org.LAT && org.LNG) {
            var marker = L.marker([org.LAT, org.LNG]);
            marker.bindPopup(`${org.NAME}\n${org.ZIP}`).openPopup();
            marker.addTo(map);
        } else
            coordless.push(org);
    });
    return coordless;
}

// adds a layer of geo data to the map
function addGeo(data, style) {
    L.geoJSON(data, {
        style: style
    }).addTo(map)
}

// returns the default style for zips
function getZipStyle() {
    return {
        "color": "#046B99",
        "weight": 1,
        "opacity": 0.7,
        "fillOpacity": 0
    };
}
