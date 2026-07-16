import json, html

videos = json.load(open('videos.json'))

def fmt_views(n):
    if not n: return ''
    if n >= 1_000_000: return f'{n/1_000_000:.1f}M'.replace('.0M','M')
    if n >= 1_000: return f'{n/1000:.0f}K'
    return str(n)

def fmt_date(d):
    if not d or len(d) != 8: return ''
    months = ['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    return f'{months[int(d[4:6])]} {int(d[6:8])}, {d[:4]}'

def fmt_dur(s):
    if not s: return ''
    s = int(s); m = s // 60; sec = s % 60
    return f'{m}:{sec:02d}'

# category -> accent color (validated, works light+dark)
CATS = {
    'Politics & Society':   '#4f7cff',
    'Media & Culture':      '#e0699f',
    'Science & Education':  '#2bb673',
    'Economics & Money':    '#f2a541',
    'Personal Reflection':  '#9b6dde',
    'History & Geopolitics':'#d9644a',
    'Philosophy & Meaning': '#00a5b5',
    'Health Care':          '#5fb0e8',
    'Mortality & Grief':    '#8892b0',
    'Mental Health':        '#3ec6c6',
    'Global Health & TB':   '#c0553b',
}

total_views = sum(v['view_count'] or 0 for v in videos)
years = sorted({v['year'] for v in videos if v['year']})
from collections import Counter
cat_counts = Counter(v['category'] for v in videos)

# build data for JS
data = [{
    'id': v['id'], 'title': v['title'], 'summary': v['summary'],
    'category': v['category'], 'year': v['year'], 'date': fmt_date(v['upload_date']),
    'ts': v['upload_date'] or '0', 'views': v['view_count'] or 0,
    'viewsFmt': fmt_views(v['view_count']), 'dur': fmt_dur(v['duration']),
    'url': v['url'], 'thumb': v['thumb'],
} for v in videos]

cats_json = json.dumps(CATS)
data_json = json.dumps(data)

def views_h(n):
    if n >= 1_000_000: return f'{n/1_000_000:.0f}M'
    return f'{n/1000:.0f}K'

html_out = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vlogbrothers — The Serious Ones</title>
<meta name="description" content="A curated, searchable archive of the most substantial Vlogbrothers video-essays by John & Hank Green — the big-ideas videos on politics, health, philosophy, economics, and mortality.">
<style>
  :root {{
    --bg: #0d1117; --bg2: #161b22; --card: #161b22; --card-hover:#1c2230;
    --border: #232b39; --text: #e6edf3; --muted: #8b98a9; --faint:#5b6674;
    --accent: #4f7cff;
  }}
  * {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    margin: 0; background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Inter, Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.5; -webkit-font-smoothing: antialiased;
  }}
  a {{ color: inherit; text-decoration: none; }}
  .wrap {{ max-width: 1180px; margin: 0 auto; padding: 0 20px; }}

  header.hero {{
    background:
      radial-gradient(1200px 400px at 15% -10%, rgba(79,124,255,0.18), transparent 60%),
      radial-gradient(900px 380px at 90% 0%, rgba(224,105,159,0.14), transparent 55%),
      var(--bg);
    border-bottom: 1px solid var(--border);
    padding: 56px 0 34px;
  }}
  .eyebrow {{ letter-spacing: .16em; text-transform: uppercase; font-size: 12px; color: var(--accent); font-weight: 700; }}
  h1 {{ font-size: clamp(30px, 5vw, 46px); margin: 10px 0 6px; line-height:1.1; font-weight: 800; letter-spacing:-0.02em; }}
  .sub {{ color: var(--muted); max-width: 680px; font-size: 16px; }}
  .stats {{ display: flex; flex-wrap: wrap; gap: 28px; margin-top: 26px; }}
  .stat .n {{ font-size: 26px; font-weight: 800; }}
  .stat .l {{ font-size: 12px; color: var(--faint); text-transform: uppercase; letter-spacing: .08em; }}

  .controls {{ position: sticky; top: 0; z-index: 20; background: rgba(13,17,23,0.86); backdrop-filter: blur(10px); border-bottom: 1px solid var(--border); padding: 14px 0; }}
  .controls .wrap {{ display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }}
  #search {{
    flex: 1 1 260px; min-width: 200px; background: var(--bg2); border: 1px solid var(--border);
    color: var(--text); padding: 11px 14px; border-radius: 10px; font-size: 15px; outline: none;
  }}
  #search:focus {{ border-color: var(--accent); }}
  select {{
    background: var(--bg2); border: 1px solid var(--border); color: var(--text);
    padding: 11px 12px; border-radius: 10px; font-size: 14px; cursor: pointer; outline:none;
  }}
  .count {{ color: var(--muted); font-size: 13px; margin-left: auto; }}

  .chips {{ display: flex; flex-wrap: wrap; gap: 8px; padding: 18px 0 4px; }}
  .chip {{
    border: 1px solid var(--border); background: var(--bg2); color: var(--muted);
    padding: 6px 13px; border-radius: 999px; font-size: 13px; cursor: pointer; user-select:none;
    display:flex; align-items:center; gap:7px; transition: all .12s;
  }}
  .chip:hover {{ color: var(--text); border-color: var(--faint); }}
  .chip .dot {{ width: 9px; height: 9px; border-radius: 50%; }}
  .chip.active {{ color: #fff; border-color: transparent; font-weight: 600; }}
  .chip .cnt {{ opacity:.65; font-size:12px; }}

  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 18px; padding: 22px 0 60px; }}
  .card {{
    background: var(--card); border: 1px solid var(--border); border-radius: 14px; overflow: hidden;
    display: flex; flex-direction: column; transition: transform .13s, border-color .13s, background .13s;
  }}
  .card:hover {{ transform: translateY(-3px); border-color: var(--faint); background: var(--card-hover); }}
  .thumb {{ position: relative; aspect-ratio: 16/9; background: #000; overflow: hidden; }}
  .thumb img {{ width: 100%; height: 100%; object-fit: cover; display:block; }}
  .thumb .dur {{ position: absolute; bottom: 8px; right: 8px; background: rgba(0,0,0,.82); color:#fff; font-size: 12px; padding: 2px 6px; border-radius: 5px; }}
  .thumb .play {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; opacity:0; transition:opacity .13s; background:rgba(0,0,0,.28); }}
  .card:hover .thumb .play {{ opacity:1; }}
  .thumb .play svg {{ width:52px; height:52px; filter: drop-shadow(0 2px 6px rgba(0,0,0,.5)); }}
  .body {{ padding: 14px 15px 16px; display: flex; flex-direction: column; gap: 9px; flex: 1; }}
  .meta {{ display: flex; align-items: center; gap: 9px; font-size: 12px; color: var(--faint); flex-wrap:wrap; }}
  .badge {{ padding: 3px 9px; border-radius: 999px; font-size: 11.5px; font-weight: 600; color:#fff; }}
  .title {{ font-size: 16.5px; font-weight: 700; line-height: 1.28; letter-spacing:-0.01em; }}
  .summary {{ font-size: 13.5px; color: var(--muted); flex: 1; }}
  .summary.clamp {{ display: -webkit-box; -webkit-line-clamp: 5; -webkit-box-orient: vertical; overflow: hidden; }}
  .more {{ align-self: flex-start; background:none; border:none; color: var(--accent); font-size:12.5px; cursor:pointer; padding:0; font-weight:600; }}
  .foot {{ display:flex; gap:14px; color: var(--faint); font-size:12px; margin-top:2px; }}

  .empty {{ text-align:center; color: var(--muted); padding: 80px 20px; }}
  footer {{ border-top: 1px solid var(--border); padding: 30px 0 50px; color: var(--faint); font-size: 13px; }}
  footer a {{ color: var(--accent); }}
  @media (max-width:560px) {{ .grid {{ grid-template-columns: 1fr; }} .count {{ display:none; }} }}
</style>
</head>
<body>
<header class="hero">
  <div class="wrap">
    <div class="eyebrow">Vlogbrothers · Curated Archive</div>
    <h1>The Serious Ones</h1>
    <p class="sub">A searchable archive of the most substantial video-essays from John &amp; Hank Green — the big-ideas videos on politics, health, philosophy, economics, and mortality. Curated from their most-watched uploads; the jokes, songs, and giraffe videos left on the cutting-room floor.</p>
    <div class="stats">
      <div class="stat"><div class="n">{len(videos)}</div><div class="l">Essays</div></div>
      <div class="stat"><div class="n">{len(cat_counts)}</div><div class="l">Topics</div></div>
      <div class="stat"><div class="n">{years[0]}–{years[-1]}</div><div class="l">Span</div></div>
      <div class="stat"><div class="n">{views_h(total_views)}</div><div class="l">Total views</div></div>
    </div>
  </div>
</header>

<div class="controls">
  <div class="wrap">
    <input id="search" type="search" placeholder="Search titles &amp; summaries…" autocomplete="off">
    <select id="sort">
      <option value="new">Newest first</option>
      <option value="old">Oldest first</option>
      <option value="views">Most viewed</option>
      <option value="az">Title A–Z</option>
    </select>
    <span class="count" id="count"></span>
  </div>
</div>

<div class="wrap">
  <div class="chips" id="chips"></div>
  <div class="grid" id="grid"></div>
  <div class="empty" id="empty" style="display:none">No videos match your filters.</div>
</div>

<footer>
  <div class="wrap">
    Unofficial fan-made archive. Videos, titles, and thumbnails belong to <a href="https://www.youtube.com/@vlogbrothers" target="_blank" rel="noopener">Vlogbrothers</a> (John &amp; Hank Green).
    Summaries written from each video's actual transcript. Not affiliated with or endorsed by the Green brothers.
  </div>
</footer>

<script>
const CATS = {cats_json};
const DATA = {data_json};
let activeCat = null;
let q = '';
let sortMode = 'new';

const grid = document.getElementById('grid');
const countEl = document.getElementById('count');
const emptyEl = document.getElementById('empty');

// build category chips
const chipWrap = document.getElementById('chips');
const catCounts = {{}};
DATA.forEach(v => catCounts[v.category] = (catCounts[v.category]||0)+1);
const sortedCats = Object.keys(catCounts).sort((a,b)=>catCounts[b]-catCounts[a]);
function renderChips() {{
  chipWrap.innerHTML = '';
  const all = document.createElement('div');
  all.className = 'chip' + (activeCat===null?' active':'');
  all.style.background = activeCat===null ? 'var(--accent)' : '';
  all.innerHTML = `All <span class="cnt">${{DATA.length}}</span>`;
  all.onclick = ()=>{{ activeCat=null; render(); }};
  chipWrap.appendChild(all);
  sortedCats.forEach(c => {{
    const el = document.createElement('div');
    const on = activeCat===c;
    el.className = 'chip' + (on?' active':'');
    if (on) el.style.background = CATS[c] || 'var(--accent)';
    el.innerHTML = `<span class="dot" style="background:${{CATS[c]||'#888'}}"></span>${{c}} <span class="cnt">${{catCounts[c]}}</span>`;
    el.onclick = ()=>{{ activeCat = on?null:c; render(); }};
    chipWrap.appendChild(el);
  }});
}}

function esc(s){{ return (s||'').replace(/[&<>"]/g, c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c])); }}

function cardHTML(v) {{
  const color = CATS[v.category] || '#888';
  return `<a class="card" href="${{v.url}}" target="_blank" rel="noopener">
    <div class="thumb">
      <img loading="lazy" src="${{v.thumb}}" alt="">
      ${{v.dur?`<span class="dur">${{v.dur}}</span>`:''}}
      <span class="play"><svg viewBox="0 0 68 48"><path fill="#f00" d="M66.5 7.7a8 8 0 0 0-5.6-5.7C56 .6 34 .6 34 .6s-22 0-26.9 1.4A8 8 0 0 0 1.5 7.7 84 84 0 0 0 0 24a84 84 0 0 0 1.5 16.3 8 8 0 0 0 5.6 5.7C12 47.4 34 47.4 34 47.4s22 0 26.9-1.4a8 8 0 0 0 5.6-5.7A84 84 0 0 0 68 24a84 84 0 0 0-1.5-16.3z"/><path fill="#fff" d="M27 34l18-10-18-10z"/></svg></span>
    </div>
    <div class="body">
      <div class="meta">
        <span class="badge" style="background:${{color}}">${{esc(v.category)}}</span>
        <span>${{v.date}}</span>
      </div>
      <div class="title">${{esc(v.title)}}</div>
      <div class="summary clamp">${{esc(v.summary)}}</div>
      ${{v.summary.length > 260 ? `<button class="more" onclick="event.preventDefault();event.stopPropagation();this.previousElementSibling.classList.toggle('clamp');this.textContent=this.textContent==='Show more'?'Show less':'Show more'">Show more</button>` : ''}}
      <div class="foot"><span>▶ ${{v.viewsFmt}} views</span></div>
    </div>
  </a>`;
}}

function render() {{
  renderChips();
  let list = DATA.filter(v => {{
    if (activeCat && v.category !== activeCat) return false;
    if (q) {{
      const hay = (v.title + ' ' + v.summary + ' ' + v.category).toLowerCase();
      if (!hay.includes(q)) return false;
    }}
    return true;
  }});
  const s = {{
    new:  (a,b)=> b.ts.localeCompare(a.ts),
    old:  (a,b)=> a.ts.localeCompare(b.ts),
    views:(a,b)=> b.views - a.views,
    az:   (a,b)=> a.title.localeCompare(b.title),
  }}[sortMode];
  list.sort(s);
  grid.innerHTML = list.map(cardHTML).join('');
  countEl.textContent = `${{list.length}} of ${{DATA.length}} essays`;
  emptyEl.style.display = list.length ? 'none':'block';
}}

document.getElementById('search').addEventListener('input', e=>{{ q = e.target.value.trim().toLowerCase(); render(); }});
document.getElementById('sort').addEventListener('change', e=>{{ sortMode = e.target.value; render(); }});
render();
</script>
</body>
</html>'''

with open('index.html', 'w') as f:
    f.write(html_out)
print('wrote index.html', len(html_out), 'bytes,', len(videos), 'videos')
