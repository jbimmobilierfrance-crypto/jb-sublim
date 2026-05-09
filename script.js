// === BANDEAU ===
(function () {
  var bandeau = document.getElementById('bandeau');
  var closeBtn = document.getElementById('bandeau-close');
  if (!bandeau || !closeBtn) return;
  if (sessionStorage.getItem('bandeau-dismissed')) {
    bandeau.style.display = 'none';
  }
  closeBtn.addEventListener('click', function () {
    bandeau.style.display = 'none';
    sessionStorage.setItem('bandeau-dismissed', '1');
  });
})();

// === BURGER MENU ===
(function () {
  var btn = document.getElementById('burger-btn');
  var menu = document.getElementById('mobile-menu');
  var close = document.getElementById('mobile-menu-close');
  if (!btn || !menu) return;

  function open() { menu.classList.add('open'); document.body.style.overflow = 'hidden'; }
  function shut() { menu.classList.remove('open'); document.body.style.overflow = ''; }

  btn.addEventListener('click', open);
  if (close) close.addEventListener('click', shut);
  menu.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', shut); });
})();

// === FAQ ACCORDION ===
(function () {
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var btn = item.querySelector('.faq-question');
    var ans = item.querySelector('.faq-answer');
    if (!btn || !ans) return;
    btn.addEventListener('click', function () {
      var open = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(function (other) {
        other.classList.remove('open');
        var a = other.querySelector('.faq-answer');
        if (a) a.style.maxHeight = '0px';
      });
      if (!open) {
        item.classList.add('open');
        ans.style.maxHeight = ans.scrollHeight + 'px';
      }
    });
  });
})();

// === SMOOTH SCROLL ===
(function () {
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      var offset = document.getElementById('site-header') ? document.getElementById('site-header').offsetHeight + 8 : 70;
      window.scrollTo({ top: target.getBoundingClientRect().top + window.pageYOffset - offset, behavior: 'smooth' });
    });
  });
})();

// === FADE-IN ON SCROLL (Intersection Observer) ===
(function () {
  if (!window.IntersectionObserver) {
    document.querySelectorAll('.fade-in').forEach(function (el) { el.classList.add('visible'); });
    return;
  }
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.fade-in').forEach(function (el) { observer.observe(el); });
})();
