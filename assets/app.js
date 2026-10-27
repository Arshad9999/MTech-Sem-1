const $ = (selector, root = document) => root.querySelector(selector);
const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
const esc = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));

async function loadJson(file) {
  const depth = document.body.dataset.depth || '';
  const response = await fetch(depth + 'assets/' + file);
  if (!response.ok) throw new Error(`${file} unavailable`);
  return response.json();
}

function nav(depth = '') {
  return `<header class="topbar"><nav class="nav shell" aria-label="Main navigation"><a class="brand" href="${depth}index.html">MTech<span>/01</span></a><div class="navlinks"><a href="${depth}index.html#courses">Courses</a><a href="${depth}index.html#study-path">Study path</a><a href="${depth}README.md">Repository guide</a></div></nav></header>`;
}

function foot() {
  return `<footer class="footer"><div class="shell">MTech Semester I learning companion • Built from the supplied syllabus • Verify examination guidance with your institution.</div></footer>`;
}

function credit(course) {
  return typeof course.credits === 'number' ? `${course.credits} credits` : 'Credit not stated';
}

function courseCard(course) {
  return `<article class="card course-card" style="--accent:${course.accent};--soft:${course.accent}14"><div class="code">${course.code} · ${credit(course)}</div><h3>${esc(course.title)}</h3><p>${esc(course.tagline)}</p><div class="chips"><span class="chip">${course.modules.length} study blocks</span><span class="chip">Mastery hub</span><span class="chip">Worked examples</span></div><a class="button" href="${course.slug}/index.html">Open course →</a></article>`;
}

async function home() {
  const data = await loadJson('course-data.json');
  $('#nav').innerHTML = nav();
  $('#courseGrid').innerHTML = data.courses.map(courseCard).join('');
  $('#foot').innerHTML = foot();
  $('#q').addEventListener('input', event => {
    const query = event.target.value.toLowerCase();
    $$('.course-card').forEach((element, index) => {
      element.hidden = !JSON.stringify(data.courses[index]).toLowerCase().includes(query);
    });
  });
}

function comparisonTable(table) {
  return `<article class="comparison-card"><h3>${esc(table.title)}</h3><div class="table-scroll"><table><thead><tr>${table.headers.map(header => `<th>${esc(header)}</th>`).join('')}</tr></thead><tbody>${table.rows.map(row => `<tr>${row.map(value => `<td>${esc(value)}</td>`).join('')}</tr>`).join('')}</tbody></table></div></article>`;
}

function mastery(supplement) {
  return `<section class="mastery-intro" id="mastery"><div class="eyebrow">Deep study layer</div><h2>Course mastery hub</h2><p>This reference layer turns the syllabus map into revision-ready definitions, classifications, equations, comparisons, error checks, and practice. Use it after the study blocks above.</p><div class="mastery-nav"><a href="#objectives">Objectives</a><a href="#glossary">Definitions</a><a href="#types">Types</a><a href="#formulas">Formula sheet</a><a href="#comparisons">Differences</a><a href="#pitfalls">Mistakes</a><a href="#practice">Practice</a><a href="#applications">Applied work</a></div></section>
  <section class="reference-section" id="objectives"><div class="section-kicker">01 · Direction</div><h2>What you should be able to do</h2><div class="objective-grid">${supplement.objectives.map((text,index) => `<article><span>${String(index + 1).padStart(2,'0')}</span><p>${esc(text)}</p></article>`).join('')}</div></section>
  <section class="reference-section" id="glossary"><div class="section-kicker">02 · Definitions</div><h2>Essential terminology</h2><p class="section-note">Open each term, recall the definition first, then compare your answer.</p><div class="accordion-grid">${supplement.glossary.map((item,index) => `<details ${index === 0 ? 'open' : ''}><summary>${esc(item[0])}</summary><p>${esc(item[1])}</p></details>`).join('')}</div></section>
  <section class="reference-section" id="types"><div class="section-kicker">03 · Classification</div><h2>Types and how they differ</h2><div class="type-grid">${supplement.types.map(item => `<article class="type-card"><h3>${esc(item[0])}</h3><p class="members">${esc(item[1])}</p><p>${esc(item[2])}</p></article>`).join('')}</div></section>
  <section class="reference-section" id="formulas"><div class="section-kicker">04 · Recall</div><h2>Formula and relationship sheet</h2><p class="section-note">A formula is only valid under its assumptions. Learn its purpose and interpretation with the symbols.</p><div class="formula-grid">${supplement.formulas.map(item => `<article class="formula-card"><h3>${esc(item[0])}</h3><code>${esc(item[1])}</code><p>${esc(item[2])}</p></article>`).join('')}</div></section>
  <section class="reference-section" id="comparisons"><div class="section-kicker">05 · Distinctions</div><h2>Difference tables</h2>${supplement.comparisons.map(comparisonTable).join('')}</section>
  <section class="reference-section" id="pitfalls"><div class="section-kicker">06 · Error prevention</div><h2>Common mistakes to avoid</h2><div class="pitfall-list">${supplement.pitfalls.map((text,index) => `<article><strong>${String(index + 1).padStart(2,'0')}</strong><p>${esc(text)}</p></article>`).join('')}</div></section>
  <section class="reference-section" id="practice"><div class="section-kicker">07 · Retrieval practice</div><h2>Questions with progressive hints</h2><p class="section-note">Attempt each question before revealing its hint. Write the complete answer, assumptions, and interpretation.</p><div class="practice-list">${supplement.practice.map((item,index) => `<details><summary><span>Q${index + 1}</span>${esc(item[0])}</summary><p><strong>Hint:</strong> ${esc(item[1])}</p></details>`).join('')}</div></section>
  <section class="reference-section" id="applications"><div class="section-kicker">08 · Application</div><h2>Applied exercises</h2><div class="application-grid">${supplement.applications.map((item,index) => `<article><div class="app-number">0${index + 1}</div><h3>${esc(item[0])}</h3><p>${esc(item[1])}</p></article>`).join('')}</div><div class="completion-note"><strong>Independent study checkpoint</strong><p>Work through the study blocks, reproduce the formula sheet, answer the practice prompts without hints, and finish at least one applied exercise before moving to assessment-focused revision. Use this portal alongside instructor materials and prescribed readings.</p></div></section>`;
}

function lessonVisual(visual) {
  if (!visual) return '';
  return `<figure class="lesson-visual"><img src="${esc(visual.src)}" alt="${esc(visual.alt)}" loading="lazy" decoding="async"><figcaption><strong>${esc(visual.title)}</strong><span>${esc(visual.caption)}</span></figcaption></figure>`;
}

function lesson(module, index, visuals) {
  const visual = visuals.find(item => item.afterModule === index + 1);
  return `<section class="module" id="m${index + 1}"><div class="eyebrow">Study block ${String(index + 1).padStart(2,'0')}</div><h2>${esc(module.title)}</h2><div class="topic-list">${module.topics.map(topic => `<span>${esc(topic)}</span>`).join('')}</div><p>${esc(module.definition)}</p><div class="equation" role="math">${esc(module.equation)}</div><div class="worked"><strong>Worked example</strong><br>${esc(module.example)}</div><p class="check">✓ Must understand: ${esc(module.checkpoint)}</p>${lessonVisual(visual)}</section>`;
}

async function course() {
  const [data, supplements] = await Promise.all([loadJson('course-data.json'), loadJson('course-supplements.json')]);
  const slug = document.body.dataset.course;
  const selected = data.courses.find(course => course.slug === slug);
  const supplement = supplements[slug];
  if (!selected || !supplement) throw new Error('Unknown course');
  document.documentElement.style.setProperty('--accent', selected.accent);
  document.documentElement.style.setProperty('--soft', selected.accent + '14');
  document.title = `${selected.code} · ${selected.title}`;
  $('#nav').innerHTML = nav('../');
  $('#courseHero').innerHTML = `<div><div class="eyebrow">${selected.code} · ${credit(selected)}</div><h1>${esc(selected.title)}</h1><p class="lede">${esc(selected.tagline)}</p><div class="downloads"><a href="#m1">Start learning</a><a href="#mastery">Mastery hub</a><a href="${selected.code}-${selected.slug}.pdf">PDF handbook</a><a href="../index.html#courses">All courses</a></div></div><div class="hero-art"><img src="../assets/${selected.diagram}" alt="Concept diagram for ${esc(selected.title)}"></div>`;
  $('#toc').innerHTML = '<strong>Course lessons</strong>' + selected.modules.map((module,index) => `<a href="#m${index + 1}">${index + 1}. ${esc(module.title)}</a>`).join('') + '<strong class="toc-group">Mastery hub</strong><a href="#glossary">Definitions</a><a href="#types">Types</a><a href="#formulas">Formula sheet</a><a href="#comparisons">Difference tables</a><a href="#practice">Practice</a><a href="#applications">Applied work</a>';
  $('#modules').innerHTML = selected.modules.map((module, index) => lesson(module, index, supplement.visuals || [])).join('') + mastery(supplement);
  $('#foot').innerHTML = foot();
  if (location.hash) setTimeout(() => document.querySelector(location.hash)?.scrollIntoView(), 80);
}

window.addEventListener('DOMContentLoaded', () => {
  (document.body.dataset.page === 'home' ? home() : course()).catch(error => {
    document.body.innerHTML = `<main class="shell"><h1>Unable to load the course</h1><p>${esc(error.message)}</p></main>`;
  });
});
