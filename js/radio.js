// ============ RADIO PLAYER ============

let audioElement = null;

/**
 * Initialisiert den Radio-Player
 */
function initRadio() {
    audioElement = document.getElementById('audio-stream');
    if (!audioElement) {
        console.warn('Audio Element nicht gefunden');
        return;
    }
    
    // Event Listener für Status-Updates
    audioElement.addEventListener('playing', () => {
        updateRadioStatus('🎵 Läuft...', '⏸');
    });
    
    audioElement.addEventListener('pause', () => {
        updateRadioStatus('Pausiert', '▶');
    });
    
    audioElement.addEventListener('error', () => {
        updateRadioStatus('❌ Fehler beim Laden', '▶');
    });
}

/**
 * Spielt Radio ab oder pausiert es
 */
function toggleRadio() {
    if (!audioElement) {
        initRadio();
    }
    
    if (audioElement.paused) {
        audioElement.play().catch(err => {
            console.error('Radio konnte nicht gestartet werden:', err);
            updateRadioStatus('❌ Nicht verfügbar', '▶');
        });
    } else {
        audioElement.pause();
    }
}

/**
 * Aktualisiert die Radio-Anzeige
 */
function updateRadioStatus(statusText, buttonText) {
    const statusElement = document.getElementById('radio-status');
    const buttonElement = document.getElementById('play-btn');
    
    if (statusElement) statusElement.textContent = statusText;
    if (buttonElement) buttonElement.innerHTML = buttonText;
}
