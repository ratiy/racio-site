// RACIO — shared nav/footer/sticky injection + interactions
(function(){
  const OP_LINKS = [
    ['Аутсорсинг', 'autsorsynh.html'],
    ['Аудит ОП', 'audit.html'],
    ['Документація', 'dokumentatsiia.html'],
    ['Пакет документів', 'pakety-dokumentiv.html'],
    ['Тренінги з ОП', 'treningy-z-ohorony-pratsi.html'],
    ['Розслідування НВ', 'rozsliduvannia-nv.html'],
    ['Супровід перевірок Держпраці', 'suprovid-derzhpratsi.html'],
  ];
  const PB_LINKS = [
    ['Аутсорсинг ПБ', 'autsorsynh-pojejna-bezpeka.html'],
    ['Аудит ПБ', 'audit-pojejna-bezpeka.html'],
    ['Документація', 'dokumentatsiia-pojejna-bezpeka.html'],
    ['Тренінги з ПБ', 'treningy-z-pojejnoi-bezpeky.html'],
    ['Декларація ДСНС', 'deklaratsiia-dsns.html'],
  ];
  const RISK_LINKS = [
    ['Оцінка ризиків', 'otsinka-ryzykiv.html'],
    ['Цивільний захист', 'tsyvilnyi-zakhyst.html'],
    ['Тренінги з безпеки праці', 'treningy-z-bezpeky-pratsi.html'],
  ];
  const ABOUT_LINKS = [
    ['Про компанію', 'pro-kompaniyu.html'],
    ['Клієнти та Кейси', 'kliyenty-ta-keysu.html'],
    ['Галузі', 'halusi.html'],
    ['Контакти', 'kontakty.html'],
  ];
  // Additional pages (not in main menu, available via footer + contextual links)
  const EXTRA_LINKS = [
    ['Тарифи', 'tarify.html'],
    ['RACIO Safety Standard', 'pro-kompaniyu.html#rss'],
  ];
  const BLOG_LINKS = [
    ['Статті', 'blog.html'],
    ['Корисне (шаблони, чек-листи)', 'koryisne.html'],
  ];

  const caret = '<svg class="caret" width="10" height="6" viewBox="0 0 10 6" fill="none"><path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>';

  function ddList(items){
    return items.map(([l,h]) => `<a href="${h}">${l}</a>`).join('');
  }

  const navHTML = `
    <div class="container nav-in">
      <a class="logo" href="index.html"><b>RACIO</b></a>
      <ul class="menu" role="menubar">
        <li data-dd><button>Охорона праці ${caret}</button>
          <div class="dd">${ddList(OP_LINKS)}</div></li>
        <li data-dd><button>Пожежна безпека ${caret}</button>
          <div class="dd">${ddList(PB_LINKS)}</div></li>
        <li data-dd><button>Керування ризиками ${caret}</button>
          <div class="dd">${ddList(RISK_LINKS)}</div></li>
        <li data-dd><button>Про нас ${caret}</button>
          <div class="dd">${ddList(ABOUT_LINKS)}</div></li>
        <li data-dd><button>Блог ${caret}</button>
          <div class="dd">${ddList(BLOG_LINKS)}</div></li>
      </ul>
      <div class="nav-right">
        <a class="nav-phone" href="tel:+380501234567">+38 050 123 45 67</a>
        <div class="lang"><a href="#" class="on">UA</a><a href="#">EN</a></div>
        <a href="#quiz" class="btn btn-primary btn-sm">Отримати прорахунок →</a>
        <button class="burger" aria-label="Menu"><span></span><span></span><span></span></button>
      </div>
    </div>
    <div class="mobile-drawer">
      <details><summary>Охорона праці</summary><div class="sub">${ddList(OP_LINKS)}</div></details>
      <details><summary>Пожежна безпека</summary><div class="sub">${ddList(PB_LINKS)}</div></details>
      <details><summary>Керування ризиками</summary><div class="sub">${ddList(RISK_LINKS)}</div></details>
      <details><summary>Про нас</summary><div class="sub">${ddList(ABOUT_LINKS)}</div></details>
      <details><summary>Блог</summary><div class="sub">${ddList(BLOG_LINKS)}</div></details>
      <div class="lead-cta">
        <a class="btn btn-primary" href="#quiz">Отримати прорахунок →</a>
        <a class="btn btn-ghost" href="tel:+380501234567">+38 050 123 45 67</a>
      </div>
    </div>
  `;

  const footHTML = `
    <div class="container">
      <div class="foot-grid">
        <div>
          <a class="brand-logo" href="index.html"><b>RACIO</b></a>
          <p class="brand-line">ISO 45001 · 14001 · 9001 · RSS · 15+ років · 500+ клієнтів</p>
          <p class="brand-line">м. Київ, вул. Прикладна, 10, офіс 501<br/>Пн-Пт 9:00–18:00</p>
        </div>
        <div>
          <h5>Охорона праці</h5>
          <ul>${OP_LINKS.map(([l,h])=>`<li><a href="${h}">${l}</a></li>`).join('')}</ul>
        </div>
        <div>
          <h5>Пожежна безпека</h5>
          <ul>${PB_LINKS.map(([l,h])=>`<li><a href="${h}">${l}</a></li>`).join('')}</ul>
          <h5 style="margin-top:24px">Керування ризиками</h5>
          <ul>${RISK_LINKS.map(([l,h])=>`<li><a href="${h}">${l}</a></li>`).join('')}</ul>
        </div>
        <div>
          <h5>Про нас</h5>
          <ul>${ABOUT_LINKS.map(([l,h])=>`<li><a href="${h}">${l}</a></li>`).join('')}</ul>
          <h5 style="margin-top:20px">Ще</h5>
          <ul>${EXTRA_LINKS.map(([l,h])=>`<li><a href="${h}">${l}</a></li>`).join('')}</ul>
          <h5 style="margin-top:20px">Блог</h5>
          <ul>${BLOG_LINKS.map(([l,h])=>`<li><a href="${h}">${l}</a></li>`).join('')}</ul>
        </div>
      </div>
      <div class="foot-contacts">
        <div><h6>Телефон</h6><a href="tel:+380501234567">+38 050 123 45 67</a></div>
        <div><h6>Email</h6><a href="mailto:sales@racio.ua">sales@racio.ua</a></div>
        <div><h6>Адреса</h6><p>м. Київ, вул. Прикладна, 10</p></div>
        <div><h6>Графік</h6><p>Пн-Пт 9:00–18:00</p></div>
      </div>
      <div class="foot-bottom">
        <div>© 2026 RACIO — Охорона праці та пожежна безпека</div>
        <div class="links">
          <a href="#">Політика конфіденційності</a>
          <a href="#">Cookies</a>
          <a href="#">Договір публічної оферти</a>
          <a href="#">Мапа сайту</a>
        </div>
        <div class="foot-social">
          <a href="#" aria-label="LinkedIn"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.5 6S0 4.88 0 3.5 1.12 1 2.5 1s2.48 1.12 2.48 2.5zM.22 8h4.56v14H.22V8zm7.29 0h4.37v1.91h.06c.61-1.15 2.1-2.37 4.32-2.37 4.62 0 5.47 3.04 5.47 6.99V22h-4.56v-6.2c0-1.48-.03-3.39-2.07-3.39-2.07 0-2.39 1.62-2.39 3.28V22H7.51V8z"/></svg></a>
          <a href="#" aria-label="Facebook"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12c0-6.63-5.37-12-12-12S0 5.37 0 12c0 5.99 4.39 10.95 10.13 11.85V15.47H7.08V12h3.05V9.36c0-3.01 1.79-4.67 4.53-4.67 1.31 0 2.69.23 2.69.23v2.96h-1.52c-1.49 0-1.96.93-1.96 1.87V12h3.33l-.53 3.47h-2.8v8.38C19.61 22.95 24 17.99 24 12z"/></svg></a>
          <a href="#" aria-label="YouTube"><svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2c-.3-1.1-1.1-1.9-2.1-2.2C19.4 3.5 12 3.5 12 3.5s-7.4 0-9.4.5C1.6 4.3.8 5.1.5 6.2 0 8.2 0 12 0 12s0 3.8.5 5.8c.3 1.1 1.1 1.9 2.1 2.2 2 .5 9.4.5 9.4.5s7.4 0 9.4-.5c1-.3 1.8-1.1 2.1-2.2.5-2 .5-5.8.5-5.8s0-3.8-.5-5.8zM9.6 15.8V8.2l6.3 3.8-6.3 3.8z"/></svg></a>
        </div>
      </div>
    </div>
  `;

  const stickyHTML = `<a href="#quiz" class="btn btn-primary">Отримати прорахунок →</a>`;

  function injectChrome(){
    const header = document.getElementById('site-header');
    const footer = document.getElementById('site-footer');
    const sticky = document.getElementById('site-sticky');
    if(header) header.innerHTML = navHTML;
    if(footer) footer.innerHTML = footHTML;
    if(sticky) sticky.innerHTML = stickyHTML;
  }

  function wireNav(){
    // Desktop dropdowns — hover + click
    document.querySelectorAll('.menu [data-dd]').forEach(li=>{
      const btn = li.querySelector('button');
      let timeout;
      li.addEventListener('mouseenter', ()=>{clearTimeout(timeout); closeAll(li); li.classList.add('open')});
      li.addEventListener('mouseleave', ()=>{timeout=setTimeout(()=>li.classList.remove('open'),160)});
      btn.addEventListener('click', (e)=>{e.stopPropagation(); const wasOpen=li.classList.contains('open'); closeAll(); if(!wasOpen) li.classList.add('open')});
    });
    document.addEventListener('click', ()=>closeAll());

    function closeAll(except){
      document.querySelectorAll('.menu .open').forEach(el=>{if(el!==except) el.classList.remove('open')});
    }

    // Burger
    const burger = document.querySelector('.burger');
    const drawer = document.querySelector('.mobile-drawer');
    if(burger && drawer){
      burger.addEventListener('click', ()=>{
        const active = burger.classList.toggle('active');
        drawer.classList.toggle('open', active);
        document.body.style.overflow = active ? 'hidden' : '';
      });
    }
  }

  function wireQuiz(){
    const quiz = document.querySelector('.quiz');
    if(!quiz) return;
    const steps = quiz.querySelectorAll('.quiz-step');
    const bar = quiz.querySelector('.quiz-progress i');
    const total = steps.length;
    let cur = 1;
    function go(n){
      cur = Math.max(1, Math.min(total, n));
      steps.forEach(s => s.classList.toggle('active', +s.dataset.step === cur));
      if(bar) bar.style.width = (cur/total*100) + '%';
    }
    go(1);
    quiz.querySelectorAll('.quiz-opt').forEach(btn=>{
      btn.addEventListener('click', ()=>{
        const step = btn.closest('.quiz-step');
        step.querySelectorAll('.quiz-opt').forEach(b=>b.classList.remove('selected'));
        btn.classList.add('selected');
        setTimeout(()=>go(cur+1), 200);
      });
    });
  }

  function wireTabs(){
    document.querySelectorAll('.tabs').forEach(tabs=>{
      const panels = document.querySelectorAll(tabs.dataset.targets || '.tab-panel');
      tabs.querySelectorAll('button').forEach((btn,i)=>{
        btn.addEventListener('click', ()=>{
          tabs.querySelectorAll('button').forEach(b=>b.classList.remove('active'));
          btn.classList.add('active');
          panels.forEach((p,j)=>p.classList.toggle('active', i===j));
        });
      });
    });
  }

  document.addEventListener('DOMContentLoaded', ()=>{
    injectChrome();
    wireNav();
    wireQuiz();
    wireTabs();
  });
})();
