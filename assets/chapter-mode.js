/* Turn long course pages into one-chapter-at-a-time study views. */
(function () {
  function ready(fn) {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
    else fn();
  }

  ready(function () {
    var content = document.querySelector('.content');
    if (!content || content.dataset.chapterMode === 'ready') return;
    var headings = Array.prototype.slice.call(content.children).filter(function (node) {
      return node.tagName === 'H2' && node.id && node.textContent.trim() !== '目录';
    });
    if (headings.length < 2) return;

    content.dataset.chapterMode = 'ready';
    var units = [];
    headings.forEach(function (heading, index) {
      var unit = document.createElement('section');
      unit.className = 'chapter-unit';
      unit.dataset.chapterId = heading.id;
      unit.dataset.chapterIndex = index;
      heading.parentNode.insertBefore(unit, heading);
      var current = heading;
      var boundary = headings[index + 1];
      while (current && current !== boundary) {
        var next = current.nextElementSibling;
        unit.appendChild(current);
        current = next;
      }
      units.push(unit);
    });

    var switcher = document.createElement('section');
    switcher.className = 'chapter-switcher';
    switcher.innerHTML = '<div><span class="chapter-eyebrow">章节阅读</span><strong>一次专注一章</strong><p>切换章节后只展示当前知识点与真题速查，避免长页面连续下滑。</p></div><div class="chapter-chips" role="tablist"></div>';
    content.insertBefore(switcher, units[0]);
    var chips = switcher.querySelector('.chapter-chips');

    function labelOf(unit) {
      return unit.querySelector('h2').textContent.replace(/^第\s*\d+\s*章\s*/, '').replace(/^第[一二三四五六七八九十]+部分[：:]?/, '').trim();
    }
    function unitForHash(hash) {
      var target = hash && document.getElementById(decodeURIComponent(hash.slice(1)));
      return target && target.closest('.chapter-unit');
    }
    function select(unit, updateHash) {
      if (!unit) return;
      units.forEach(function (item) { item.hidden = item !== unit; });
      Array.prototype.forEach.call(chips.children, function (chip) {
        chip.classList.toggle('selected', chip.dataset.chapterId === unit.dataset.chapterId);
        chip.setAttribute('aria-selected', chip.dataset.chapterId === unit.dataset.chapterId ? 'true' : 'false');
      });
      if (updateHash) history.replaceState(null, '', '#' + unit.dataset.chapterId);
      window.scrollTo({ top: Math.max(0, switcher.getBoundingClientRect().top + window.scrollY - 58), behavior: 'instant' });
    }

    units.forEach(function (unit) {
      var chip = document.createElement('button');
      chip.type = 'button';
      chip.dataset.chapterId = unit.dataset.chapterId;
      chip.setAttribute('role', 'tab');
      chip.textContent = (Number(unit.dataset.chapterIndex) + 1) + '. ' + labelOf(unit);
      chip.addEventListener('click', function () { select(unit, true); });
      chips.appendChild(chip);
    });

    document.addEventListener('click', function (event) {
      var link = event.target.closest('a[href^="#"]');
      if (!link) return;
      var unit = unitForHash(link.getAttribute('href'));
      if (unit) select(unit, false);
    }, true);
    window.addEventListener('hashchange', function () {
      var unit = unitForHash(location.hash);
      if (unit) select(unit, false);
    });

    select(unitForHash(location.hash) || units[0], false);
  });
})();
