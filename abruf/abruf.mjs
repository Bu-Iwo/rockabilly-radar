// ROCKABILLY RADAR - Abrufer
// Liest die Seiten aus quellen.json (hoeflich: robots.txt beachten, 1 Sekunde Pause),
// speichert den Text jeder Seite und eine Uebersicht (_index.json) sowie neue Links (_kandidaten.json).
// Es wird nichts angemeldet, nichts umgangen. Gesperrte Seiten werden nur gemeldet.
import fs from 'node:fs';
import path from 'node:path';

const UA = 'RockabillyRadarAbruf/1.0 (+https://github.com/Bu-Iwo/rockabilly-radar)';
const OUT = process.argv[2] || 'out';
const PAUSE_MS = 1000;
const quellen = JSON.parse(fs.readFileSync(process.env.QUELLEN || new URL('./quellen.json', import.meta.url), 'utf8'));
fs.mkdirSync(OUT, { recursive: true });

const sleep = ms => new Promise(r => setTimeout(r, ms));
const hostOf = u => { try { return new URL(u).hostname.replace(/^www\./, ''); } catch { return ''; } };
const bekannt = new Set(quellen.seiten.map(s => hostOf(s.url)));
const ignoriert = /(facebook|instagram|twitter|x\.com|youtube|google|apple|tiktok|whatsapp|linkedin|paypal|wikipedia|spotify|fb\.me|goo\.gl|bit\.ly|openstreetmap|maps)/i;

const robotsCache = new Map();
async function robotsErlaubt(url) {
  const u = new URL(url);
  if (!robotsCache.has(u.origin)) {
    let regeln = [];
    try {
      const r = await fetch(u.origin + '/robots.txt', { headers: { 'User-Agent': UA }, signal: AbortSignal.timeout(15000) });
      if (r.ok) {
        let gilt = false;
        for (const zeile of (await r.text()).split(/\r?\n/)) {
          const z = zeile.split('#')[0].trim();
          const m = z.match(/^([A-Za-z-]+)\s*:\s*(.*)$/);
          if (!m) continue;
          const k = m[1].toLowerCase(), v = m[2].trim();
          if (k === 'user-agent') gilt = (v === '*' || /rockabillyradar/i.test(v));
          else if (gilt && k === 'disallow' && v) regeln.push(v);
        }
      }
    } catch { /* robots.txt nicht lesbar: dann gilt nichts als gesperrt */ }
    robotsCache.set(u.origin, regeln);
  }
  const p = u.pathname + u.search;
  return !robotsCache.get(u.origin).some(r => r === '/' || p.startsWith(r.split('*')[0].replace(/\$$/, '')));
}

function htmlZuText(html, basis) {
  const links = [];
  let t = html.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>|<!--[\s\S]*?-->/gi, ' ');
  t = t.replace(/<a\s[^>]*href=["']([^"'#][^"']*)["'][^>]*>([\s\S]*?)<\/a>/gi, (_, h, inner) => {
    let abs = ''; try { abs = new URL(h, basis).href; } catch {}
    if (abs.startsWith('http')) links.push(abs);
    return ' ' + inner + (abs ? ' [' + abs + '] ' : ' ');
  });
  t = t.replace(/<(br|\/p|\/div|\/li|\/tr|\/h\d|\/td)[^>]*>/gi, '\n').replace(/<[^>]+>/g, ' ');
  t = t.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#0?39;/g, "'")
       .replace(/&auml;/g, 'ä').replace(/&ouml;/g, 'ö').replace(/&uuml;/g, 'ü').replace(/&Auml;/g, 'Ä').replace(/&Ouml;/g, 'Ö').replace(/&Uuml;/g, 'Ü').replace(/&szlig;/g, 'ß');
  t = t.replace(/[ \t\r]+/g, ' ').replace(/\n\s*\n+/g, '\n').trim();
  return { text: t, links };
}

let browser = null;
async function mitBrowser(url) {
  if (!browser) {
    const { chromium } = await import('playwright');
    browser = await chromium.launch();
  }
  const page = await browser.newPage({ userAgent: UA });
  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
    return await page.content();
  } finally { await page.close(); }
}

const index = { gestartet: new Date().toISOString(), seiten: [] };
const kandidaten = new Map();

for (const s of quellen.seiten) {
  const eintrag = { id: s.id, url: s.url, status: 'fehler', bytes: 0, fehler: '' };
  try {
    if (!(await robotsErlaubt(s.url))) { eintrag.status = 'robots'; eintrag.fehler = 'robots.txt verbietet das Lesen'; }
    else {
      let html;
      if (s.js) html = await mitBrowser(s.url);
      else {
        const r = await fetch(s.url, { headers: { 'User-Agent': UA, 'Accept-Language': 'de,en;q=0.8' }, redirect: 'follow', signal: AbortSignal.timeout(45000) });
        if (!r.ok) throw new Error('HTTP ' + r.status);
        html = await r.text();
      }
      const { text, links } = htmlZuText(html, s.url);
      fs.writeFileSync(path.join(OUT, s.id + '.txt'), text);
      eintrag.status = 'ok'; eintrag.bytes = text.length;
      for (const l of links) {
        const h = hostOf(l);
        if (h && !bekannt.has(h) && !ignoriert.test(h)) {
          const k = kandidaten.get(h) || { domain: h, beispiel: l, gefunden_auf: s.id, anzahl: 0 };
          k.anzahl++; kandidaten.set(h, k);
        }
      }
    }
  } catch (e) { eintrag.fehler = String(e.message || e).slice(0, 200); }
  index.seiten.push(eintrag);
  console.log(eintrag.status, s.id, eintrag.bytes, eintrag.fehler);
  await sleep(PAUSE_MS);
}
if (browser) await browser.close();
index.beendet = new Date().toISOString();
index.zusammenfassung = { gesamt: index.seiten.length, ok: index.seiten.filter(x => x.status === 'ok').length };
fs.writeFileSync(path.join(OUT, '_index.json'), JSON.stringify(index, null, 1));
fs.writeFileSync(path.join(OUT, '_kandidaten.json'), JSON.stringify([...kandidaten.values()].sort((a, b) => b.anzahl - a.anzahl).slice(0, 200), null, 1));
