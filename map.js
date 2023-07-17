const initCoords = [44, -89];

var map = loadMap("humanitarian");
var coordless = loadMarkers();

coordless.forEach((org) => console.log(`No coords for ${org.NAME}`));
console.log(`There are ${coordless.length} organizations without coords`);

testData.features.forEach((feature) => {
    addGeo(feature, getStyle(feature))
})

// initialize map with tile layer
// http://leaflet-extras.github.io/leaflet-providers/preview/
function loadMap(mapType) {
    tilesURL = null
    switch (mapType) {
        case 'humanitarian':
            tilesURL = 'https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png';
            break;
        case 'standard':
            tilesURL = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
        default:
            break;
    }

    let newMap = new L.map("map", {
        center: initCoords,
        zoom: 8
    });
    if (tilesURL != null)
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
        fillColor: getColor2(feature.properties.DATA),
        weight: 2,
        opacity: 1,
        color: 'white',
        dashArray: '3',
        fillOpacity: 0.7
    };
}

function getColor(d) {
    return d > 95 ? '#800026' :
        d > 90 ? '#BD0026' :
        d > 75 ? '#E31A1C' :
        d > 60 ? '#FC4E2A' :
        d > 45 ? '#FD8D3C' :
        d > 30 ? '#FEB24C' :
        d > 15 ? '#FED976' :
        '#FFEDA0';
}

function getColor2(d) {
    return d > 10000 ? '#800026' :
        d > 9000 ? '#BD0026' :
        d > 7500 ? '#E31A1C' :
        d > 6000 ? '#FC4E2A' :
        d > 4500 ? '#FD8D3C' :
        d > 3000 ? '#FEB24C' :
        d > 1500 ? '#FED976' :
        '#FFEDA0';
}