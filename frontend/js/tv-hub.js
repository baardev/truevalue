/**
 * tv-hub.js — shared rendering helper for TrueValue Analytics hub pages.
 *
 * Usage:
 *   tvHub.render('reports', document.getElementById('tv-hub-content'));
 *   tvHub.render('research', document.getElementById('tv-hub-content'));
 *   tvHub.render('tvpci',    document.getElementById('tv-hub-content'));
 */
window.tvHub = (function () {
  var INDEX_URL = '/frontend/site-index.json';

  function esc(s) {
    return String(s || '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderLinks(links) {
    return (links || []).map(function (l) {
      var cls = 'card-link' + (l.type === 'pdf' ? ' pdf' : '');
      return '<a class="' + cls + '" href="' + esc(l.url) + '">' + esc(l.label) + '</a>';
    }).join('');
  }

  function renderTags(tags) {
    return (tags || []).map(function (t) {
      return '<span class="tag ' + esc(t.cls || '') + '">' + esc(t.label) + '</span>';
    }).join('');
  }

  function renderItem(item) {
    var featuredCls = item.featured ? ' featured' : '';
    return '<div class="card' + featuredCls + '">'
      + '<div class="card-top">'
      + '<div class="card-icon">' + (item.icon || '') + '</div>'
      + '<div>'
      + '<div class="card-title">' + esc(item.title) + '</div>'
      + '<div class="card-sub">' + esc(item.desc) + '</div>'
      + '</div>'
      + '</div>'
      + (item.tags && item.tags.length ? '<div class="card-tags">' + renderTags(item.tags) + '</div>' : '')
      + (item.links && item.links.length ? '<div class="card-links">' + renderLinks(item.links) + '</div>' : '')
      + '</div>';
  }

  function renderSections(sections) {
    return (sections || []).map(function (sec) {
      return '<div class="section-title">' + esc(sec.title) + '</div>'
        + '<div class="grid">'
        + (sec.items || []).map(renderItem).join('')
        + '</div>';
    }).join('');
  }

  function render(key, target) {
    if (!target) return;
    fetch(INDEX_URL)
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (data) {
        var section = data[key];
        if (!section) throw new Error('Key "' + key + '" not found in site-index.json');
        target.innerHTML = renderSections(section.sections || []);
      })
      .catch(function (err) {
        target.innerHTML = '<p style="color:#f87171;padding:20px 0;">Could not load site-index.json: ' + esc(err.message) + '</p>';
      });
  }

  return { render: render };
})();
