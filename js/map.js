// ============ KARTE ============

let map = null;
let markersLayer = null;
let userMarker = null;

/**
 * Initialisiert die Leaflet-Karte
 */
function initMap(userLat, userLon) {
    if (typeof L === 'undefined') {
        console.error('Leaflet nicht geladen');
        return;
    }
    
    map = L.map('map').setView([userLat, userLon], 6);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);
    
    markersLayer = L.layerGroup().addTo(map);
    
    // User-Marker erstellen
    userMarker = L.marker([userLat, userLon], {
        icon: L.divIcon({
            className: 'custom-marker',
            html: '<div style="background: #7FB069; width: 20px; height: 20px; border-radius: 50%; border: 3px solid white; box-shadow: 0 0 10px rgba(127,176,105,0.8);"></div>',
            iconSize: [20, 20]
        })
    }).addTo(map).bindPopup('📍 Dein Standort');
}

/**
 * Aktualisiert die Kartenansicht auf eine neue Position
 */
function updateMapView(lat, lon, zoom = 8) {
    if (!map) return;
    
    map.setView([lat, lon], zoom);
    if (userMarker) {
        userMarker.setLatLng([lat, lon]);
    }
}

/**
 * Fügt einen Event-Marker zur Karte hinzu
 */
function addEventMarker(lat, lon, title, date) {
    if (!markersLayer) return;
    
    const marker = L.marker([lat, lon]).bindPopup(`<b>${title}</b><br>${date}`);
    markersLayer.addLayer(marker);
}

/**
 * Entfernt alle Event-Marker von der Karte
 */
function clearMarkers() {
    if (markersLayer) {
        markersLayer.clearLayers();
    }
}
