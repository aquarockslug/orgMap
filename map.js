const initCoords = [44, -89];

var map = loadMap("humanitarian");
var coordless = loadMarkers();

coordless.forEach((org) => console.log(`No coords for ${org.NAME}`));
console.log(`There are ${coordless.length} organizations without coords`);


console.log(testData)
testData.features.forEach((feature) => {
  addGeo(feature, getStyle(feature))
})

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

function getStyle(feature) {
    return {
      fillColor: getColor(feature.properties.DATA),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function getColor(d) {
    return d > 1000 ? '#800026' :
        d > 500 ? '#BD0026' :
        d > 200 ? '#E31A1C' :
        d > 100 ? '#FC4E2A' :
        d > 50 ? '#FD8D3C' :
        d > 20 ? '#FEB24C' :
        d > 10 ? '#FED976' :
        '#FFEDA0';
}
