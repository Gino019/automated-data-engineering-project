const money = n => '$' + Math.round(n).toLocaleString('en-US');
const num = n => Math.round(n).toLocaleString('en-US');
const palette = ['#9e78ff', '#41d8e8', '#578ffb', '#ef8db6', '#51d5a7'];
let dataset = null;
let charts = [];
const byId = id => document.getElementById(id);

function sums(rows) {
  return rows.reduce((a, r) => ({
    revenue: a.revenue + r.revenue, profit: a.profit + r.profit,
    orders: a.orders + r.orders, units: a.units + r.units
  }), {revenue: 0, profit: 0, orders: 0, units: 0});
}
function bucket(rows, key) {
  let m = new Map();
  for (const row of rows) {
    const k = row[key], old = m.get(k) || 0;
    m.set(k, old + row.revenue);
  }
  return [...m.entries()].sort((a,b) => a[0].localeCompare(b[0]));
}
function renderChart(id, type, labels, values, colors, fill = false) {
  if (!window.Chart) { byId(id).replaceWith(Object.assign(document.createElement('p'), {textContent:'Charts require the Chart.js CDN. See the data table below.'})); return; }
  const existing = Chart.getChart(byId(id));
  if (existing) existing.destroy();
  charts.push(new Chart(byId(id), {
    type,
    data: {labels, datasets:[{label:'Revenue ($)', data:values,
      borderColor: colors[0], backgroundColor: type === 'doughnut' ? colors :
      (type === 'bar' ? colors[0] : 'rgba(157,115,255,.13)'),
      borderWidth: type === 'line' ? 2 : 0, tension:.35, fill,
      borderRadius: type === 'bar' ? 6 : 0, pointRadius:type === 'line' ? 3 : 0}]},
    options: {responsive:true, maintainAspectRatio:false,
      plugins:{legend:{display:type==='doughnut',position:'right',labels:{color:'#b2c0db',boxWidth:12}},
      tooltip:{callbacks:{label:c=>`${c.label||''}: ${money(c.parsed.y ?? c.parsed)}`}}},
      scales:type==='doughnut'?{}:{x:{ticks:{color:'#8696bb'},grid:{display:false}},
        y:{ticks:{color:'#8696bb',callback:v=>'$'+(v/1000).toFixed(0)+'k'},grid:{color:'#26304a'}}}}
  }));
}
function render() {
  if (!dataset) return;
  const y = byId('year').value, region = byId('region').value;
  const rows = dataset.rows.filter(r => (y==='all'||String(r.year)===y) &&
    (region==='all'||r.region===region));
  const totals = sums(rows);
  byId('revenue').textContent = money(totals.revenue);
  byId('orders').textContent = num(totals.orders);
  byId('profit').textContent = money(totals.profit);
  byId('margin').textContent = totals.revenue ? (100*totals.profit/totals.revenue).toFixed(1)+'%' : '—';
  const monthly = bucket(rows,'month');
  renderChart('monthlyChart','line',monthly.map(e=>e[0]),monthly.map(e=>e[1]),palette,true);
  const categories = bucket(rows,'category').sort((a,b)=>b[1]-a[1]);
  renderChart('categoryChart','bar',categories.map(e=>e[0]),categories.map(e=>e[1]),palette);
  const regions = bucket(rows,'region');
  renderChart('regionChart','doughnut',regions.map(e=>e[0]),regions.map(e=>e[1]),palette);
  byId('rows').innerHTML = rows.slice(0,13).map(r=>`<tr><td>${r.month}</td><td>${r.region}</td><td>${r.category}</td><td>${num(r.orders)}</td><td>${money(r.revenue)}</td><td>${money(r.profit)}</td></tr>`).join('') || '<tr><td colspan="6">No rows</td></tr>';
  byId('download').onclick = () => {
    const header = ['month','year','region','category','orders','units','revenue','profit'];
    const csv = [header.join(','),...rows.map(r=>header.map(k=>r[k]).join(','))].join('\n');
    const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([csv],{type:'text/csv'}));
    a.download='flowforge-curated-sales.csv';a.click();URL.revokeObjectURL(a.href);
  };
}
async function start() {
  try {
    const resp = await fetch('./data/metrics.json');
    if(!resp.ok) throw new Error('HTTP '+resp.status);
    dataset = await resp.json();
    const years = [...new Set(dataset.rows.map(r=>r.year))].sort((a,b)=>b-a);
    const regions = [...new Set(dataset.rows.map(r=>r.region))].sort();
    for(const y of years) byId('year').add(new Option(y,y));
    for(const r of regions) byId('region').add(new Option(r,r));
    byId('year').addEventListener('change', render);
    byId('region').addEventListener('change', render);
    const q = dataset.quality;
    for(const [id,val] of Object.entries({rawOrders:q.raw_orders,completed:q.completed_orders,
      excluded:q.excluded_cancelled_or_refunded,customers:q.customers})) byId(id).textContent=num(val);
    byId('source').textContent=dataset.source;
    byId('timestamp').textContent=dataset.generated_at_utc;
    byId('runId').textContent=dataset.run_id;
    render();
  } catch(e) {
    byId('rows').innerHTML='<tr><td colspan="6">Unable to load pipeline results. See the repository Actions logs.</td></tr>';
    console.error(e);
  }
}
start();
