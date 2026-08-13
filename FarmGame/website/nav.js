/* =============================================
   SHARED NAVIGATION & UTILITY SCRIPT
   ============================================= */

document.addEventListener('DOMContentLoaded', () => {

  // ── Active nav link ───────────────────────────
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-links a').forEach(link => {
    if (link.getAttribute('href') === currentPage) {
      link.classList.add('active');
    }
  });

  // ── Hamburger toggle ─────────────────────────
  const toggle = document.getElementById('nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (toggle && navLinks) {
    toggle.addEventListener('click', () => {
      navLinks.classList.toggle('open');
      const isOpen = navLinks.classList.contains('open');
      toggle.setAttribute('aria-expanded', isOpen);
    });

    // Close on outside click
    document.addEventListener('click', e => {
      if (!toggle.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ── Animate stat bars on scroll ──────────────
  const statFills = document.querySelectorAll('.stat-bar-fill[data-value]');

  const observeStat = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const fill = entry.target;
        fill.style.width = fill.dataset.value + '%';
        observeStat.unobserve(fill);
      }
    });
  }, { threshold: 0.3 });

  statFills.forEach(fill => observeStat.observe(fill));

  // ── Gallery lightbox ─────────────────────────
  const lightbox      = document.getElementById('lightbox');
  const lightboxImg   = document.getElementById('lightbox-img');
  const lightboxCap   = document.getElementById('lightbox-caption');
  const lightboxClose = document.getElementById('lightbox-close');

  if (lightbox) {
    document.querySelectorAll('.gallery-item').forEach(item => {
      item.addEventListener('click', () => {
        const src     = item.querySelector('img').src;
        const caption = item.querySelector('.gallery-item-label')?.textContent || '';
        lightboxImg.src  = src;
        lightboxCap.textContent = caption;
        lightbox.classList.add('open');
        document.body.style.overflow = 'hidden';
      });
    });

    const closeLightbox = () => {
      lightbox.classList.remove('open');
      document.body.style.overflow = '';
    };

    lightboxClose.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', e => {
      if (e.target === lightbox) closeLightbox();
    });

    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') closeLightbox();
    });
  }

  // ── Pixel particles (hero) ────────────────────
  const particleContainer = document.querySelector('.pixel-particles');
  if (particleContainer) {
    for (let i = 0; i < 18; i++) {
      spawnParticle(particleContainer);
    }
  }

  function spawnParticle(container) {
    const p = document.createElement('div');
    p.className = 'particle';

    const size     = [4, 6, 8][Math.floor(Math.random() * 3)];
    const colors   = ['#e8832a','#7ec850','#f5e6c8','#4a8c2a','#c47c3e'];
    const color    = colors[Math.floor(Math.random() * colors.length)];
    const left     = Math.random() * 100;
    const duration = 8 + Math.random() * 14;
    const delay    = Math.random() * duration;

    p.style.cssText = `
      width:${size}px; height:${size}px;
      background:${color};
      left:${left}%;
      bottom:0;
      animation-duration:${duration}s;
      animation-delay:-${delay}s;
    `;

    container.appendChild(p);
  }

  // ── Typewriter for .typewriter elements ───────
  document.querySelectorAll('.typewriter').forEach(el => {
    const text = el.textContent;
    el.textContent = '';
    el.style.visibility = 'visible';
    let i = 0;
    const speed = parseInt(el.dataset.speed || '60');

    const type = () => {
      if (i < text.length) {
        el.textContent += text[i++];
        setTimeout(type, speed);
      }
    };

    // Trigger when visible
    const obs = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting) {
        type();
        obs.disconnect();
      }
    });
    obs.observe(el);
  });

  // ── Scroll-reveal cards ───────────────────────
  const revealItems = document.querySelectorAll('.card, .feature-row, .gallery-item, .about-profile');

  const revealObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = entry.target.style.transform.replace('translateY(24px)', 'translateY(0)');
        revealObs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  revealItems.forEach(item => {
    item.style.opacity = '0';
    item.style.transform += ' translateY(24px)';
    item.style.transition = 'opacity 0.4s ease, transform 0.4s ease, box-shadow 0.15s';
    revealObs.observe(item);
  });

});
