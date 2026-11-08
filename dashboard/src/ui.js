import { createIcons, icons } from 'lucide';

const METRICS = [
  { icon: 'heart-pulse', label: 'Heart rate',     unit: 'bpm', min: 40, max: 180, value: 72 },
  { icon: 'wind',        label: 'SpO₂',           unit: '%',   min: 80, max: 100, value: 98 },
  { icon: 'thermometer', label: 'Body temp',      unit: '°C',  min: 35, max: 40,  value: 36.8 },
  { icon: 'radiation',   label: 'Radiation dose', unit: 'mSv', min: 0,  max: 50,  value: 12 },
  { icon: 'brain',       label: 'Stress index',   unit: '',    min: 0,  max: 100, value: 30 },
];

export function createUI() {
  let active = 0;
  const $ = id => document.getElementById(id);
  const nav = $('icons'), slider = $('slider');

  nav.innerHTML = METRICS.map((m, i) =>
    `<button data-i="${i}"><i data-lucide="${m.icon}"></i></button>`).join('');
  createIcons({ icons });

  nav.onclick = e => { const b = e.target.closest('button'); if (b) select(+b.dataset.i); };
  slider.oninput = () => setFraction(slider.value / 100);

  function render() {
    const m = METRICS[active];
    [...nav.children].forEach((b, i) => b.classList.toggle('active', i === active));
    $('metric-title').textContent = m.label;
    $('metric-value').textContent = `${m.value.toFixed(1)} ${m.unit}`;
    slider.value = ((m.value - m.min) / (m.max - m.min)) * 100;
  }
  function select(i) { active = (i + METRICS.length) % METRICS.length; render(); }
  function setFraction(f) {
    const m = METRICS[active];
    f = Math.min(1, Math.max(0, f));
    m.value = m.min + f * (m.max - m.min);
    render();
  }
  function nudge(d) {
    const m = METRICS[active];
    setFraction((m.value - m.min) / (m.max - m.min) + d);
  }

  render();
  return { next: () => select(active + 1), prev: () => select(active - 1), nudge };
}
