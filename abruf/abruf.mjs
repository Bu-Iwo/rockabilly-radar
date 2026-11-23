// ROCKABILLY RADAR - Abrufer
// Liest die Seiten aus quellen.json (hoeflich: robots.txt beachten, 1 Sekunde Pause),
// speichert den Text jeder Seite und eine Uebersicht (_index.json) sowie neue Links (_kandidaten.json).
// Es wird nichts angemeldet, nichts umgangen. Gesperrte Seiten werden nur gemeldet.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import crypto from 'node:crypto';

const UA = 'RockabillyRadarAbruf/1.0 (+https://github.com/Bu-Iwo/rockabilly-radar)';
const OUT = process.argv[2] || 'out';
const PAUSE_MS = 1000;
const PREV = process.env.PREV || '';
const REPO = process.env.REPO || '.';
const quellen = JSON.parse(fs.readFileSync(process.env.QUELLEN || new URL('./quellen.json', import.meta.url), 'utf8'));

// ---- Automatische Liste: Veranstalter-Links aus events*.js und Band-Seiten aus kuenstler.js ----
const kalenderRegex = /(swingcalendar|we-love-country|boogietanzen|rock-and-roll-termine|brokensilence|jukeboxstompers)/i;
const nichtLesen = /(facebook|instagram|fb\.me|youtube|twitter|x\.com|tiktok|google\.|wa\.me|whatsapp)/i;
function kurz(u) { const x = new URL(u); return (x.hostname.replace(/^www\./, '') + x.pathname).replace(/[^a-z0-9]+/gi, '-').replace(/-+$/, '').slice(0, 50) + '-' + crypto.createHash('md5').update(u).digest('hex').slice(0, 6); }
function ladeJs(datei) {
  const f = path.join(REPO, datei);
  if (!fs.existsSync(f)) return null;
  const ctx = { window: {} }; ctx.self = ctx.window;
  try { vm.runInNewContext(fs.readFileSync(f, 'utf8'), ctx, { timeout: 5000 }); } catch { return null; }
  return ctx.window;
}
function autoSeiten() {
  const urls = new Map(); // url -> typ
  const heute = new Date().toISOString().slice(0, 10);
  const jahr = new Date(Date.now() + 366 * 864e5).toISOString().slice(0, 10);
  const nimm = (u, typ) => {
    if (!u || typeof u !== 'string' || !/^https?:\/\//i.test(u)) return;
    if (nichtLesen.test(u) || kalenderRegex.test(u)) return;
    u = u.split('#')[0];
    if (!urls.has(u)) urls.set(u, typ);
  };
  const ev = ladeJs('events.js');
  for (const e of (ev && ev.RR_EVENTS) || []) if (e.end >= heute && e.start <= jahr) { nimm(e.info, 'veranstalter'); nimm(e.tickets, 'tickets'); }
  for (const f of ['events-country-1.js', 'events-country-2.js', 'events-country-3.js']) {
    const w = ladeJs(f);
    for (const r of (w && w.RR_MORE) || []) if (r[1] >= heute && r[0] <= jahr) { nimm(r[8], 'veranstalter'); nimm(r[9], 'tickets'); }
  }
  const k = ladeJs('kuenstler.js');
  for (const b of (k && k.RR_KUENSTLER && k.RR_KUENSTLER.eintraege) || []) {
    if (b.lesbar === 'nur-facebook') continue;
    nimm(b.terminseite, 'band'); nimm(b.homepage, 'band');
  }
  const blockiert = new Set((process.env.NICHT_LESEN || 'the-firebirds.de,c-a-t-enterprises.de,boozebombs.de,reach-country.de').split(','));
  return [...urls].filter(([u]) => !blockiert.has(hostOf(u))).map(([url, typ]) => ({ id: typ[0] + '-' + kurz(url), url, typ, js: false, auto: true }));
}
let alle = quellen.seiten.map(s => ({ ...s, typ: s.typ || 'kalender' }));
if (!process.env.KEINE_AUTO) {
  const bekanntUrl = new Set(alle.map(s => s.url));
  for (const a of autoSeiten()) if (!bekanntUrl.has(a.url)) alle.push(a);
}
{ const gesehen = new Set(); for (const a of alle) { let i = a.id, n = 2; while (gesehen.has(i)) i = a.id + '-' + (n++); a.id = i; gesehen.add(i); } }
if (process.env.NUR_LISTE) { for (const a of alle) console.log(a.typ, a.url); console.log('GESAMT', alle.length); process.exit(0); }

fs.mkdirSync(OUT, { recursive: true });

const sleep = ms => new Promise(r => setTimeout(r, ms));
function hostOf(u) { try { return new URL(u).hostname.replace(/^www\./, ''); } catch { return ''; } }
const bekannt = new Set();
const ignoriert = /(facebook|instagram|twitter|x\.com|youtube|google|apple|tiktok|whatsapp|linkedin|paypal|wikipedia|spotify|fb\.me|goo\.gl|bit\.ly|openstreetmap|maps)/i;

const robotsCache = new Map();
function musterZuRegex(m) {
  const ende = m.endsWith('$');
  const kern = (ende ? m.slice(0, -1) : m).replace(/[.+?^${}()|[\]\\]/g, '\\$&').replace(/\*/g, '.*');
  return new RegExp('^' + kern + (ende ? '$' : ''));
}
async function robotsErlaubt(url) {
  const u = new URL(url);
  if (!robotsCache.has(u.origin)) {
    const regeln = []; // { erlaubt, laenge, re }
    try {
      const r = await fetch(u.origin + '/robots.txt', { headers: { 'User-Agent': UA }, signal: AbortSignal.timeout(15000) });
      if (r.ok && /text|plain/i.test(r.headers.get('content-type') || 'text/plain')) {
        let gilt = false, letzteWarAgent = false;
        for (const zeile of (await r.text()).split(/\r?\n/)) {
          const z = zeile.split('#')[0].trim();
          const m = z.match(/^([A-Za-z-]+)\s*:\s*(.*)$/);
          if (!m) continue;
          const k = m[1].toLowerCase(), v = m[2].trim();
          if (k === 'user-agent') {
            const trifft = (v === '*' || /rockabillyradar/i.test(v));
            gilt = letzteWarAgent ? (gilt || trifft) : trifft;
            letzteWarAgent = true;
          } else {
            letzteWarAgent = false;
            if (gilt && (k === 'disallow' || k === 'allow') && v) regeln.push({ erlaubt: k === 'allow', laenge: v.length, re: musterZuRegex(v) });
          }
        }
      }
    } catch { /* robots.txt nicht lesbar: dann gilt nichts als gesperrt */ }
    robotsCache.set(u.origin, regeln);
  }
  const p = u.pathname + u.search;
  let best = null;
  for (const r of robotsCache.get(u.origin)) if (r.re.test(p) && (!best || r.laenge > best.laenge || (r.laenge === best.laenge && r.erlaubt))) best = r;
  return !best || best.erlaubt;
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

for (const s of alle) bekannt.add(hostOf(s.url));
const index = { gestartet: new Date().toISOString(), seiten: [] };
const kandidaten = new Map();
const vorher = {};
try { for (const x of JSON.parse(fs.readFileSync(path.join(PREV, '_index.json'), 'utf8')).seiten) vorher[x.id] = x; } catch { /* erster Lauf */ }
const MAX_ZEICHEN = 600000;

async function holen(s) {
  let letzterFehler = '';
  for (let versuch = 1; versuch <= 3; versuch++) {
    try {
      if (s.js) return await mitBrowser(s.url);
      const r = await fetch(s.url, { headers: { 'User-Agent': UA, 'Accept-Language': 'de,en;q=0.8' }, redirect: 'follow', signal: AbortSignal.timeout(45000) });
      if (r.status === 403 || r.status === 401 || r.status === 404 || r.status === 410) throw Object.assign(new Error('HTTP ' + r.status), { endgueltig: true });
      if (!r.ok) throw new Error('HTTP ' + r.status);
      const typ = r.headers.get('content-type') || '';
      if (!/text|html|xml|json/i.test(typ) && typ) throw Object.assign(new Error('kein Text: ' + typ), { endgueltig: true });
      return await r.text();
    } catch (e) {
      letzterFehler = String(e.message || e);
      if (e.endgueltig) break;
      await sleep(3000 * versuch);
    }
  }
  throw new Error(letzterFehler);
}

for (const s of alle) {
  const eintrag = { id: s.id, url: s.url, typ: s.typ, status: 'fehler', bytes: 0, fehler: '', ok_seit: '' };
  try {
    if (!(await robotsErlaubt(s.url))) { eintrag.status = 'robots'; eintrag.fehler = 'robots.txt verbietet das Lesen'; }
    else {
      const html = await holen(s);
      const { text, links } = htmlZuText(html, s.url);
      fs.writeFileSync(path.join(OUT, s.id + '.txt'), text.slice(0, MAX_ZEICHEN));
      eintrag.status = 'ok'; eintrag.bytes = Math.min(text.length, MAX_ZEICHEN); eintrag.ok_seit = index.gestartet.slice(0, 10);
      for (const l of links) {
        const h = hostOf(l);
        if (h && !bekannt.has(h) && !ignoriert.test(h)) {
          const k = kandidaten.get(h) || { domain: h, beispiel: l, gefunden_auf: s.id, anzahl: 0 };
          k.anzahl++; kandidaten.set(h, k);
        }
      }
    }
  } catch (e) { eintrag.fehler = String(e.message || e).slice(0, 200); }
  // Ausfall-Schutz: Beim Fehler den letzten guten Text behalten und als veraltet kennzeichnen.
  if (eintrag.status !== 'ok' && PREV) {
    const alt = path.join(PREV, s.id + '.txt');
    if (fs.existsSync(alt) && vorher[s.id] && vorher[s.id].ok_seit) {
      fs.copyFileSync(alt, path.join(OUT, s.id + '.txt'));
      eintrag.veraltet = true; eintrag.ok_seit = vorher[s.id].ok_seit; eintrag.bytes = vorher[s.id].bytes;
    }
  }
  index.seiten.push(eintrag);
  console.log(eintrag.status + (eintrag.veraltet ? '(veraltet)' : ''), s.id, eintrag.bytes, eintrag.fehler);
  await sleep(PAUSE_MS);
}
if (browser) await browser.close();
const z = (st) => index.seiten.filter(x => x.status === st).length;
index.zusammenfassung = { gesamt: index.seiten.length, ok: z('ok'), robots: z('robots'), fehler: z('fehler'), veraltet: index.seiten.filter(x => x.veraltet).length,
  hauptquellen_ok: index.seiten.filter(x => x.typ === 'kalender' && x.status === 'ok').length, hauptquellen_gesamt: index.seiten.filter(x => x.typ === 'kalender').length };
index.beendet = new Date().toISOString();
fs.writeFileSync(path.join(OUT, '_index.json'), JSON.stringify(index, null, 1));
fs.writeFileSync(path.join(OUT, '_kandidaten.json'), JSON.stringify([...kandidaten.values()].sort((a, b) => b.anzahl - a.anzahl).slice(0, 200), null, 1));
