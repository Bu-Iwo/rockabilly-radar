// ============ HAUPT-APPLICATION ============

let allEvents = [];
let userLat = 50.7189;  // Default: Zwickau
let userLon = 12.4961;
let maxRadius = 2500;
let favorites = JSON.parse(localStorage.getItem('rockabilly-favorites') || '[]');

/**
 * Wechselt zwischen den Tabs
 */
function switchTab(tabName) {
    // Alle Tabs ausblenden
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Alle Nav-Buttons deaktivieren
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Aktiven Tab anzeigen
    document.getElementById(`tab-${tabName}`).classList.add('active');
    document.getElementById(`nav-${tabName}`).classList.add('active');
    
    // Wenn Favoriten-Tab, aktualisiere die Liste
    if (tabName === 'favorites') {
        loadFavorites();
    }
}

/**
 * Holt den GPS-Standort
 */
function getGPSLocation() {
    if (!navigator.geolocation) {
        showStatus('❌ GPS nicht unterstützt');
        return;
    }
    
    showStatus('📡 Suche GPS-Standort...');
    
    navigator.geolocation.getCurrentPosition(
        (position) => {
            userLat = position.coords.latitude;
            userLon = position.coords.longitude;
            
            updateMapView(userLat, userLon, 8);
            
            // Reverse Geocoding für Stadtnamen
            fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${userLat}&lon=${userLon}`)
                .then(res => res.json())
                .then(data => {
                    const city = data.address.city || data.address.town || data.address.village || 'Unbekannt';
                    document.getElementById('city-input').value = city;
                    showStatus(`✅ Standort: ${city}`);
                    updateDisplay();
                })
                .catch(() => {
                    showStatus('✅ GPS gefunden (Stadt unbekannt)');
                    updateDisplay();
                });
        },
        (error) => {
            showStatus('❌ GPS nicht verfügbar');
        }
    );
}

/**
 * Aktualisiert den Standort basierend auf der Eingabe
 */
async function updateLocation() {
    const city = document.getElementById('city-input').value.trim();
    if (!city) return;
    
    showStatus('🔍 Suche Koordinaten...');
    
    try {
        const res = await fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(city)}&limit=1`);
        const data = await res.json();
        
        if (data && data.length > 0) {
            userLat = parseFloat(data[0].lat);
            userLon = parseFloat(data[0].lon);
            
            updateMapView(userLat, userLon, 8);
            showStatus(`✅ Standort: ${city}`);
            updateDisplay();
        } else {
            showStatus('❌ Stadt nicht gefunden');
        }
    } catch (e) {
        showStatus('❌ Fehler bei der Suche');
    }
}

/**
 * Aktualisiert den Suchradius
 */
function updateRadius() {
    maxRadius = document.getElementById('radius-slider').value;
    document.getElementById('radius-display').textContent = maxRadius + ' km';
    updateDisplay();
}

/**
 * Toggle Favorit
 */
function toggleFavorite(eventTitle) {
    if (favorites.includes(eventTitle)) {
        favorites = favorites.filter(f => f !== eventTitle);
    } else {
        favorites.push(eventTitle);
    }
    localStorage.setItem('rockabilly-favorites', JSON.stringify(favorites));
    updateDisplay();
    loadFavorites();
}

/**
 * Lädt die Favoriten-Anzeige
 */
function loadFavorites() {
    const container = document.getElementById('favorites-container');
    if (!container) return;
    
    if (favorites.length === 0) {
        container.innerHTML = `
            <div class="favorites-empty">
                <div class="favorites-empty-icon">⭐</div>
                <p>Noch keine Favoriten gespeichert</p>
                <p style="font-size: 0.9rem; margin-top: 10px;">Tippe auf das Stern-Symbol bei einem Event</p>
            </div>
        `;
        return;
    }
    
    const favoriteEvents = allEvents.filter(ev => favorites.includes(ev.title));
    
    if (favoriteEvents.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #999;">Keine Favoriten mehr verfügbar</p>';
        return;
    }
    
    container.innerHTML = favoriteEvents.map((ev, index) => createEventCard(ev, index)).join('');
}

/**
 * Suchfunktion
 */
function searchEvents() {
    const query = document.getElementById('search-input').value.toLowerCase().trim();
    const resultsContainer = document.getElementById('search-results');
    
    if (!query) {
        resultsContainer.innerHTML = '';
        return;
    }
    
    const results = allEvents.filter(ev => {
        const searchText = `${ev.title} ${ev.city} ${ev.location} ${ev.desc}`.toLowerCase();
        return searchText.includes(query);
    });
    
    if (results.length === 0) {
        resultsContainer.innerHTML = '<p style="text-align: center; color: #999;">Keine Ergebnisse gefunden</p>';
        return;
    }
    
    resultsContainer.innerHTML = results.map((ev, index) => createEventCard(ev, index)).join('');
}

/**
 * Erstellt eine Event-Karte (HTML)
 */
function createEventCard(ev, index) {
    const dist = calculateDistance(userLat, userLon, ev.lat, ev.lon);
    const distText = dist !== null ? `<span class="distance-badge">📍 ${dist} km</span>` : '';
    const calLink = createGoogleCalendarLink(ev);
    const bookingLink = createBookingLink(ev);
    const isFavorite = favorites.includes(ev.title);
    const favoriteIcon = isFavorite ? '⭐' : '☆';
    
    return `
    <div class="event-card">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div style="flex: 1;">
                <div class="event-title">${ev.title}</div>
                <div class="event-date">📅 ${ev.date || 'Termin unbekannt'}</div>
                <div class="event-loc">🏠 ${ev.location || ev.city}</div>
                ${distText}
            </div>
            <button onclick="toggleFavorite('${ev.title.replace(/'/g, "\\'")}')" 
                    style="background: none; border: none; font-size: 2rem; cursor: pointer; color: ${isFavorite ? 'var(--neon-orange)' : 'var(--chrome-silver)'};">
                ${favoriteIcon}
            </button>
        </div>
        
        <button class="btn-toggle" onclick="toggleDetails(${index})">
            ℹ️ Mehr Infos
        </button>
        
        <div class="event-details" id="details-${index}">
            <div class="event-desc">${ev.desc || 'Keine Beschreibung verfügbar.'}</div>
            
            <div class="action-buttons">
                ${ev.url ? `<a href="${ev.url}" target="_blank" class="btn-action">🔗 Webseite</a>` : ''}
                <a href="${calLink}" target="_blank" class="btn-action">📅 Kalender</a>
                <a href="${bookingLink}" target="_blank" class="btn-action">🏨 Hotel</a>
            </div>
        </div>
    </div>
    `;
}

/**
 * Toggle Details einer Event-Karte
 */
function toggleDetails(eventId) {
    const details = document.getElementById(`details-${eventId}`);
    if (details) {
        details.classList.toggle('active');
    }
}

/**
 * Lädt Events aus der JSON-Datei
 */
async function loadEvents() {
    try {
        const response = await fetch('events.json?v=' + new Date().getTime());
        const data = await response.json();
        allEvents = Array.isArray(data) ? data : [];
        showStatus(`✅ ${allEvents.length} Events geladen`);
        updateDisplay();
    } catch (e) {
        document.getElementById('events-container').innerHTML = "❌ Fehler beim Laden";
        showStatus('❌ Fehler');
    }
}

/**
 * Aktualisiert die Anzeige (Events + Karte)
 */
function updateDisplay() {
    const container = document.getElementById('events-container');
    clearMarkers();
    
    // Events verarbeiten
    let processed = allEvents.map(ev => {
        const dist = calculateDistance(userLat, userLon, ev.lat, ev.lon);
        const dateObj = parseDate(ev.date);
        return { ...ev, distance: dist, dateObj: dateObj };
    });

    // Nach Radius filtern
    let filtered = processed.filter(ev => {
        if (ev.distance === null) return true;
        return ev.distance <= maxRadius;
    });

    // Nach Datum sortieren
    filtered.sort((a, b) => {
        if (!a.dateObj && !b.dateObj) return 0;
        if (!a.dateObj) return 1;
        if (!b.dateObj) return -1;
        return a.dateObj - b.dateObj;
    });

    if (filtered.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: #999;">Keine Events gefunden</p>';
        return;
    }

    // Events anzeigen und Marker setzen
    container.innerHTML = filtered.map((ev, index) => {
        if (ev.lat && ev.lon) {
            addEventMarker(ev.lat, ev.lon, ev.title, ev.date);
        }
        return createEventCard(ev, index);
    }).join('');

    showStatus(`✅ ${filtered.length} Events im Radius`);
}

/**
 * Initialisiert die komplette App beim Laden
 */
function initApp() {
    initMap(userLat, userLon);
    initRadio();
    loadEvents();
}

// App starten wenn DOM geladen ist
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}
