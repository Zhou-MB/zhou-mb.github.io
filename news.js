// Keep entries readable without JavaScript; enhance dated lists with sorting and expansion.
for (const [selector, moreLabel, lessLabel] of [
  ['#news-list', 'View all news', 'Show less news'],
  ['#teaching-list', 'Show more', 'Show less'],
]) {
  const list = document.querySelector(selector);
  if (!list) continue;
  const entries = Array.from(list.children);
  const dateOf = (entry) => entry.getAttribute('data-sort-date') || entry.querySelector('time')?.getAttribute('datetime') || '';
  entries.sort((a, b) => dateOf(b).localeCompare(dateOf(a)));
  entries.forEach((entry) => list.append(entry));

  if (entries.length > 5) {
    const toggle = document.createElement('button');
    toggle.type = 'button';
    toggle.className = 'news-toggle';
    toggle.setAttribute('aria-controls', list.id);
    let expanded = false;
    const render = () => {
      entries.forEach((entry, index) => { entry.hidden = !expanded && index >= 5; });
      toggle.textContent = expanded ? lessLabel : moreLabel;
      toggle.setAttribute('aria-expanded', String(expanded));
    };
    toggle.addEventListener('click', () => {
      expanded = !expanded;
      render();
    });
    render();
    list.after(toggle);
  }
}
