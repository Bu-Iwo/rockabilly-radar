let allEvents = [];
let userLat = 50.7189;
let userLon = 12.4961;
let maxRadius = 2500;
let activeGenre = 'all';

// Genre Filter Initialisierung
document.addEventListener('DOMContentLoaded', () => {
    const pills = document.querySelectorAll('.pill');
    pills.forEach(pill => {
        pill.addEventListener('click', (e) => {
            pills.forEach(p => p.classList.remove('active'));
            e.target.classList.add('active');
            activeGenre = e.target.dataset.genre;
            updateDisplay();
        });
    });
});

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(`tab-${tabName}`).classList.add('active');
    document.getElementById(`nav-${tabName}`).classList.add('active');
}

function getGPSLocation() {
    if (!navigator.geolocation) {
        showStatus('❌ GPS nicht unterstützt');
        return;
    }
    showStatus('📡 Suche GPS-Standort...');
    navigator.geolocation.getCurrentPosition(
        pos => {
            userLat = pos.coords.latitude;
            userLon = pos.coords.longitude;
            updateMapView(userLat, userLon, 8);
            fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${userLat}&lon=${userLon}`)
                .then(r => r.json())
                .then(d => {
                    const city = d.address.city || d.address.town || 'Unbekannt';
                    document.getElementById('city-input').value = city;
                    showStatus(`✅ Standort: ${city}`);
                    updateDisplay();
                })
                .catch(() => {
                    showStatus('✅ GPS gefunden');
                    updateDisplay();
                });
        },
        () => showStatus('❌ GPS nicht verfügbar')
    );
}

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

function updateRadius() {
    maxRadius = document.getElementById('radius-slider').value;
    document.getElementById('radius-display').textContent = maxRadius + ' km';
    updateDisplay();
}

function searchEvents() {
    const q = document.getElementById('search-input').value.toLowerCase().trim();
    const r = document.getElementById('search-results');
    if (!q) {
        r.innerHTML = '';
        return;
    }
    const results = allEvents.filter(ev =>
        `${ev.title} ${ev.city} ${ev.location} ${ev.desc}`.toLowerCase().includes(q)
    );
    r.innerHTML = results.length
        ? results.map((ev, i) => createEventCard(ev, i)).join('')
        : '<p style="text-align:center;color:#999">Keine Ergebnisse</p>';
}

function createEventCard(ev, index) {
    const dist = calculateDistance(userLat, userLon, ev.lat, ev.lon);
    const distText = dist !== null ? `<span class="distance-badge">📍 ${dist} km</span>` : '';
    const genreTags = (ev.genres || []).map(g =>
        `<span style="font-size:0.7rem;background:#eee;padding:2px 6px;border-radius:4px;margin-right:4px">${g}</span>`
    ).join('');

    return `<div class="event-card">
        <div style="flex:1">
            <div class="event-title">${ev.title}</div>
            <div style="margin-bottom:5px">${genreTags}</div>
            <div class="event-date">📅 ${ev.date || 'Termin unbekannt'}</div>
            <div class="event-loc">🏠 ${ev.location || ev.city}</div>
            ${distText}
        </div>
        <button class="btn-toggle" onclick="toggleDetails(${index})">ℹ️ Mehr Infos</button>
        <div class="event-details" id="details-${index}">
            <div class="event-desc">${ev.desc || 'Keine Beschreibung.'}</div>
            <div class="action-buttons">
                ${ev.url ? `<a href="${ev.url}" target="_blank" class="btn-action">🔗 Webseite</a>` : ''}
                <a href="${createGoogleCalendarLink(ev)}" target="_blank" class="btn-action">📅 Kalender</a>
                <a href="${createBookingLink(ev)}" target="_blank" class="btn-action">🏨 Hotel</a>
            </div>
        </div>
    </div>`;
}

function toggleDetails(id) {
    document.getElementById(`details-${id}`)?.classList.toggle('active');
}

async function loadEvents() {
    try {
        const res = await fetch('events.json?v=' + new Date().getTime());
        if (!res.ok) throw new Error('HTTP ' + res.status);
        allEvents = await res.json();
        if (!Array.isArray(allEvents)) allEvents = [];
        showStatus(`✅ ${allEvents.length} Events geladen`);
        updateDisplay();
    } catch (e) {
        console.error('Fehler beim Laden:', e);
        // Fallback: Hardcoded Events verwenden
        allEvents = [
            {
                title: "Summer Jamboree 2026",
                date: "01.08. - 09.08.2026",
                location: "Senigallia, Italien",
                city: "Senigallia",
                lat: 43.7147,
                lon: 13.2183,
                desc: "Europas größtes Rockabilly-Festival.",
                url: "https://www.summerjamboree.com",
                genres: ["Rockabilly", "Rock'n'Roll"]
            },
            {
                title: "Firebirds Festival 2026",
                date: "03.07. - 05.07.2026",
                location: "Grimma, Deutschland",
                city: "Grimma",
                lat: 51.2294,
                lon: 12.7561,
                desc: "Rock'n'Roll im Kloster.",
                url: "https://www.firebirds-festival.de",
                genres: ["Rock'n'Roll"]
            }
        ];
        showStatus(`⚠️ Fallback: ${allEvents.length} Events (keine Internet-Verbindung)`);
        updateDisplay();
    }
}

function updateDisplay() {
    const container = document.getElementById('events-container');
    clearMarkers();

    let processed = allEvents.map(ev => ({
        ...ev,
        distance: calculateDistance(userLat, userLon, ev.lat, ev.lon),
        dateObj: parseDate(ev.date)
    }));

    let filtered = processed.filter(ev => {
        const inRadius = ev.distance === null || ev.distance <= maxRadius;
        const matchesGenre = activeGenre === 'all' || (ev.genres && ev.genres.includes(activeGenre));
        return inRadius && matchesGenre;
    });

    filtered.sort((a, b) => {
        if (!a.dateObj && !b.dateObj) return 0;
        if (!a.dateObj) return 1;
        if (!b.dateObj) return -1;
        return a.dateObj - b.dateObj;
    });

    if (filtered.length === 0) {
        container.innerHTML = '<p style="text-align:center;color:#999">Keine Events gefunden</p>';
        return;
    }

    container.innerHTML = filtered.map((ev, i) => {
        if (ev.lat && ev.lon) addEventMarker(ev.lat, ev.lon, ev.title, ev.date);
        return createEventCard(ev, i);
    }).join('');
    showStatus(`✅ ${filtered.length} Events im Radius`);
}

function initApp() {
    initMap(userLat, userLon);
    initRadio();
    loadEvents();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    initApp();
}
