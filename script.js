(() => {
  'use strict';

  const body = document.body;
  const header = document.querySelector('#siteHeader');
  const menuToggle = document.querySelector('.menu-toggle');
  const primaryNav = document.querySelector('#primaryNav');
  const navScrim = document.querySelector('[data-nav-close]');
  const navLinks = Array.from(document.querySelectorAll('.nav-link'));
  const home = document.querySelector('#home');
  const contact = document.querySelector('#contact');
  const footer = document.querySelector('.site-footer');
  const mobileCall = document.querySelector('.mobile-call');
  const backToTop = document.querySelector('.back-to-top');
  const mobileBreakpoint = window.matchMedia('(max-width: 1080px)');
  const mobileCallBreakpoint = window.matchMedia('(max-width: 700px)');
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  let menuPreviouslyFocused = null;
  let scrollFrame = null;

  const focusableSelector = [
    'a[href]',
    'button:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
  ].join(',');

  function setMenuState(isOpen, restoreFocus = true) {
    if (!menuToggle || !primaryNav) return;

    body.classList.toggle('nav-open', isOpen);
    menuToggle.setAttribute('aria-expanded', String(isOpen));
    menuToggle.setAttribute('aria-label', isOpen ? '关闭主导航' : '打开主导航');

    if (isOpen) {
      menuPreviouslyFocused = document.activeElement;
      const firstFocusable = primaryNav.querySelector(focusableSelector);
      window.setTimeout(() => firstFocusable?.focus(), 80);
    } else if (restoreFocus && menuPreviouslyFocused instanceof HTMLElement) {
      menuPreviouslyFocused.focus();
      menuPreviouslyFocused = null;
    }

    requestScrollUpdate();
  }

  menuToggle?.addEventListener('click', () => {
    const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
    setMenuState(!isOpen);
  });

  navScrim?.addEventListener('click', () => setMenuState(false));

  primaryNav?.addEventListener('click', (event) => {
    const link = event.target.closest('a[href^="#"]');
    if (link && mobileBreakpoint.matches) setMenuState(false, false);
  });

  document.addEventListener('keydown', (event) => {
    if (!body.classList.contains('nav-open')) return;

    if (event.key === 'Escape') {
      event.preventDefault();
      setMenuState(false);
      return;
    }

    if (event.key !== 'Tab' || !primaryNav) return;

    const focusable = [
      menuToggle,
      ...Array.from(primaryNav.querySelectorAll(focusableSelector))
    ].filter((element) => element instanceof HTMLElement && !element.hasAttribute('hidden'));

    if (!focusable.length) return;

    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  mobileBreakpoint.addEventListener?.('change', (event) => {
    if (!event.matches && body.classList.contains('nav-open')) {
      setMenuState(false, false);
    }
    requestScrollUpdate();
  });

  mobileCallBreakpoint.addEventListener?.('change', requestScrollUpdate);

  function setFloatingControlState(control, isVisible) {
    if (!control) return;
    control.classList.toggle('is-visible', isVisible);
    control.setAttribute('aria-hidden', String(!isVisible));
    if (isVisible) {
      control.removeAttribute('tabindex');
    } else {
      control.setAttribute('tabindex', '-1');
    }
  }

  function updateScrollUI() {
    const scrollY = window.scrollY;
    const menuOpen = body.classList.contains('nav-open');
    const headerHeight = header?.offsetHeight || 0;
    const heroPassed = home
      ? home.getBoundingClientRect().bottom <= headerHeight
      : scrollY > window.innerHeight;
    const contactEntered = contact
      ? contact.getBoundingClientRect().top <= window.innerHeight
      : false;
    const footerEntered = footer
      ? footer.getBoundingClientRect().top <= window.innerHeight
      : false;
    const closingPlaneEntered = contactEntered || footerEntered;

    header?.classList.toggle('is-scrolled', scrollY > 16);
    setFloatingControlState(
      mobileCall,
      mobileCallBreakpoint.matches && heroPassed && !closingPlaneEntered && !menuOpen
    );
    setFloatingControlState(
      backToTop,
      scrollY > window.innerHeight * 2.25 && !closingPlaneEntered && !menuOpen
    );

    const marker = scrollY + window.innerHeight * 0.38;
    let currentId = 'home';

    navLinks.forEach((link) => {
      const targetId = link.getAttribute('href')?.slice(1);
      const target = targetId ? document.getElementById(targetId) : null;
      if (target && target.offsetTop <= marker) currentId = targetId;
    });

    navLinks.forEach((link) => {
      const isActive = link.getAttribute('href') === `#${currentId}`;
      link.classList.toggle('is-active', isActive);
      if (isActive) {
        link.setAttribute('aria-current', 'page');
      } else {
        link.removeAttribute('aria-current');
      }
    });

    scrollFrame = null;
  }

  function requestScrollUpdate() {
    if (scrollFrame !== null) return;
    scrollFrame = window.requestAnimationFrame(updateScrollUI);
  }

  window.addEventListener('scroll', requestScrollUpdate, { passive: true });
  window.addEventListener('resize', requestScrollUpdate, { passive: true });
  updateScrollUI();

  backToTop?.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: reducedMotion.matches ? 'auto' : 'smooth'
    });
  });

  const revealElements = Array.from(document.querySelectorAll('.reveal'));

  revealElements.forEach((element) => {
    const delay = Number(element.dataset.delay || 0);
    if (delay > 0) element.style.setProperty('--reveal-delay', `${delay}ms`);
  });

  if (reducedMotion.matches || !('IntersectionObserver' in window)) {
    revealElements.forEach((element) => element.classList.add('is-visible'));
  } else {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      });
    }, {
      threshold: 0.08,
      rootMargin: '0px 0px -7% 0px'
    });

    revealElements.forEach((element) => revealObserver.observe(element));
  }

  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener('click', (event) => {
      const targetId = link.getAttribute('href');
      if (!targetId || targetId === '#') return;

      const target = document.querySelector(targetId);
      if (!target) return;

      event.preventDefault();
      target.scrollIntoView({
        behavior: reducedMotion.matches ? 'auto' : 'smooth',
        block: 'start'
      });

      if (history.replaceState) history.replaceState(null, '', targetId);
    });
  });

  document.querySelectorAll('[data-current-year]').forEach((element) => {
    element.textContent = String(new Date().getFullYear());
  });
})();
