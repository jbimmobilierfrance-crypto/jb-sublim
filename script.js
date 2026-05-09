// === BANDEAU DISMISS ===
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
  var burgerBtn = document.getElementById('burger-btn');
  var mobileMenu = document.getElementById('mobile-menu');
  var closeBtn = document.getElementById('mobile-menu-close');
  if (!burgerBtn || !mobileMenu) return;

  function openMenu() {
    mobileMenu.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    mobileMenu.classList.remove('open');
    document.body.style.overflow = '';
  }

  burgerBtn.addEventListener('click', openMenu);
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);

  mobileMenu.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', closeMenu);
  });
})();

// === FAQ ACCORDION ===
(function () {
  document.querySelectorAll('.faq-item').forEach(function (item) {
    var btn = item.querySelector('.faq-question');
    var answer = item.querySelector('.faq-answer');
    if (!btn || !answer) return;

    btn.addEventListener('click', function () {
      var isOpen = item.classList.contains('open');

      // Close all other items
      document.querySelectorAll('.faq-item.open').forEach(function (other) {
        if (other !== item) {
          other.classList.remove('open');
          var otherAnswer = other.querySelector('.faq-answer');
          if (otherAnswer) otherAnswer.style.maxHeight = '0px';
        }
      });

      // Toggle current
      if (isOpen) {
        item.classList.remove('open');
        answer.style.maxHeight = '0px';
      } else {
        item.classList.add('open');
        answer.style.maxHeight = answer.scrollHeight + 'px';
      }
    });
  });
})();

// === SMOOTH SCROLL for anchor links ===
(function () {
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (!target) return;
      e.preventDefault();
      var offset = 70;
      var top = target.getBoundingClientRect().top + window.pageYOffset - offset;
      window.scrollTo({ top: top, behavior: 'smooth' });
    });
  });
})();
