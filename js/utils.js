// ============ HILFSFUNKTIONEN ============

/**
 * Berechnet die Entfernung zwischen zwei GPS-Punkten in km
 */
function calculateDistance(lat1, lon1, lat2, lon2) {
    if (!lat1 || !lat2) return null;
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    return Math.round(R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)));
}

/**
 * Parst ein deutsches Datum (z.B. "12.05.2026")
 */
function parseDate(dateStr) {
    if (!dateStr) return null;
    const match = dateStr.match(/(\d{1,2})\.(\d{1,2})\.(\d{4})?/);
    if (match) {
        const day = parseInt(match[1]);
        const month = parseInt(match[2]) - 1;
        const year = parseInt(match[3]) || new Date().getFullYear();
        return new Date(year, month, day);
    }
    return null;
}

/**
 * Zeigt eine Status-Nachricht an
 */
function showStatus(msg) {
    const statusElement = document.getElementById('status-msg');
    if (statusElement) {
        statusElement.textContent = msg;
    }
}

/**
 * Erstellt einen Google Kalender Link
 */
function createGoogleCalendarLink(event) {
    const title = encodeURIComponent(event.title);
    const location = encodeURIComponent(event.location || event.city);
    const details = encodeURIComponent(event.desc || '');
    
    let startDate = '';
    if (event.date) {
        const dateMatch = event.date.match(/(\d{1,2})\.(\d{1,2})\.(\d{4})?/);
        if (dateMatch) {
            const day = dateMatch[1].padStart(2, '0');
            const month = dateMatch[2].padStart(2, '0');
            const year = dateMatch[3] || new Date().getFullYear();
            startDate = `${year}${month}${day}`;
        }
    }
    
    if (!startDate) return '#';
    return `https://calendar.google.com/calendar/render?action=TEMPLATE&text=${title}&dates=${startDate}/${startDate}&details=${details}&location=${location}`;
}

/**
 * Erstellt einen Booking.com Link
 */
function createBookingLink(event) {
    const city = encodeURIComponent(event.city || 'Berlin');
    
    let checkIn = '';
    if (event.date) {
        const dateMatch = event.date.match(/(\d{1,2})\.(\d{1,2})\.(\d{4})?/);
        if (dateMatch) {
            const day = dateMatch[1].padStart(2, '0');
            const month = dateMatch[2].padStart(2, '0');
            const year = dateMatch[3] || new Date().getFullYear();
            checkIn = `${year}-${month}-${day}`;
        }
    }
    
    if (!checkIn) {
        return `https://www.booking.com/searchresults.de.html?ss=${city}`;
    }
    
    const date = new Date(event.date.match(/(\d{1,2})\.(\d{1,2})\.(\d{4})?/));
    const checkout = new Date(date);
    checkout.setDate(checkout.getDate() + 1);
    const checkOut = checkout.toISOString().split('T')[0];
    
    return `https://www.booking.com/searchresults.de.html?ss=${city}&checkin=${checkIn}&checkout=${checkOut}`;
}
