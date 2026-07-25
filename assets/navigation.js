/* Keep same-page chapter links reliable across all course pages. */
(function () {
  window.__navigationReady = true;
  var topOffset = 58;

  function targetForHash(hash) {
    if (!hash || hash === '#') return null;
    try {
      return document.getElementById(decodeURIComponent(hash.slice(1)));
    } catch (_) {
      return null;
    }
  }

  function scrollToHash(hash, behavior) {
    var target = targetForHash(hash);
    if (!target) return false;
    var top = target.getBoundingClientRect().top + window.scrollY - topOffset;
    window.scrollTo({ top: Math.max(0, top), behavior: behavior || 'instant' });
    return true;
  }

  document.addEventListener('click', function (event) {
    var link = event.target.closest('a[href^="#"]');
    if (!link || link.target || event.defaultPrevented) return;
    var hash = link.getAttribute('href');
    if (!targetForHash(hash)) return;
    event.preventDefault();
    history.pushState(null, '', hash);
    scrollToHash(hash, 'instant');
  });

  window.addEventListener('hashchange', function () {
    scrollToHash(location.hash, 'instant');
  });

  window.addEventListener('DOMContentLoaded', function () {
    if (location.hash) requestAnimationFrame(function () {
      scrollToHash(location.hash, 'auto');
    });
  });
})();
