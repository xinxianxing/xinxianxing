(function () {
  'use strict';

  /** Replace ⭐️ N/10 with a colored badge in h2, h3, and li elements */
  function processScoreBadges() {
    var scoreRe = /⭐️\s*(\d+(?:\.\d+)?)\/10/;
    var targets = document.querySelectorAll('.main-content h2, .main-content h3, .main-content li');
    targets.forEach(function (el) {
      var m = el.innerHTML.match(scoreRe);
      if (!m) return;
      var score = parseFloat(m[1]);
      var tier;
      if (score >= 9) tier = 'high';
      else if (score >= 7) tier = 'good';
      else if (score >= 5) tier = 'mid';
      else tier = 'low';
      el.innerHTML = el.innerHTML.replace(
        scoreRe,
        '<span class="score-badge" data-tier="' + tier + '">' + m[1] + '</span>'
      );
    });
  }

  /** Add semantic classes to tag lines, source lines, and background paragraphs */
  function markSemanticElements() {
    var paragraphs = document.querySelectorAll('.main-content p');
    paragraphs.forEach(function (p) {
      var text = p.textContent.trim();

      // Tag line: starts with Tags or 标签 (bold prefix rendered by Markdown)
      if (/^(Tags|标签)\s*:/.test(text)) {
        p.classList.add('tag-line');
        return;
      }

      // Source line: pattern like "source · site · date"
      if (/^(rss|reddit|github|hackernews|hn|telegram)\s*·/i.test(text)) {
        p.classList.add('source-line');
        return;
      }
    });
  }

  /** Set up EN/中文 language toggle as a page-level control */
  function setupLanguageToggle() {
    if (document.body.classList.contains('tutorial-page')) return;

    // Create toggle buttons
    var toggle = document.createElement('div');
    toggle.className = 'lang-toggle';

    var btnEn = document.createElement('button');
    btnEn.textContent = 'EN';
    btnEn.type = 'button';

    var btnZh = document.createElement('button');
    btnZh.textContent = '中文';
    btnZh.type = 'button';

    toggle.appendChild(btnEn);
    toggle.appendChild(btnZh);

    // Prefer the site header when present; fall back to the body for older pages.
    var mount = document.querySelector('.site-actions');
    if (mount) {
      mount.appendChild(toggle);
    } else {
      document.body.insertBefore(toggle, document.body.firstChild);
    }

    // Read saved preference, default to zh
    var saved = null;
    try { saved = localStorage.getItem('xinxianxing-lang'); } catch (e) { /* noop */ }
    var currentLang = saved === 'en' ? 'en' : 'zh';

    function updateButtons(lang) {
      if (lang === 'en') {
        btnEn.classList.add('active');
        btnZh.classList.remove('active');
      } else {
        btnZh.classList.add('active');
        btnEn.classList.remove('active');
      }
    }

    // Index page: toggle lang-section visibility
    var zhSection = document.getElementById('lang-zh');
    var enSection = document.getElementById('lang-en');

    function showSection(lang) {
      if (!zhSection || !enSection) return;
      if (lang === 'en') {
        enSection.classList.remove('hidden');
        zhSection.classList.add('hidden');
      } else {
        zhSection.classList.remove('hidden');
        enSection.classList.add('hidden');
      }
    }

    // Article page: redirect to the other language version
    function switchArticleLang(lang) {
      var path = window.location.pathname;
      var target = null;
      if (lang === 'en' && /-zh(?:\.html)?$/.test(path.replace(/\/$/, ''))) {
        target = path.replace(/-zh(\.html)?$/, '-en$1').replace(/-zh\/$/, '-en/');
      } else if (lang === 'zh' && /-en(?:\.html)?$/.test(path.replace(/\/$/, ''))) {
        target = path.replace(/-en(\.html)?$/, '-zh$1').replace(/-en\/$/, '-zh/');
      }
      if (target) window.location.href = target;
    }

    function setLang(lang) {
      currentLang = lang;
      updateButtons(lang);
      try { localStorage.setItem('xinxianxing-lang', lang); } catch (e) { /* noop */ }
      if (zhSection && enSection) {
        showSection(lang);
      } else {
        switchArticleLang(lang);
      }
    }

    btnEn.addEventListener('click', function () { setLang('en'); });
    btnZh.addEventListener('click', function () { setLang('zh'); });

    // Initialize
    updateButtons(currentLang);
    if (zhSection && enSection) {
      showSection(currentLang);
    }
  }

  /** Add local review buttons to every generated Action Card */
  function setupActionCardFeedback() {
    var cards = document.querySelectorAll('.action-card[data-card-id]');
    if (!cards.length) return;

    var buttons = [
      { type: 'useful', label: '👍 有用' },
      { type: 'favorite', label: '⭐ 收藏' },
      { type: 'ignore', label: '👎 忽略' }
    ];

    function postFeedback(cardId, buttonType) {
      var payload = JSON.stringify({
        card_id: cardId,
        button_type: buttonType,
        origin: 'website'
      });
      var options = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: payload
      };

      var config = window.XINXIANXING_FEEDBACK_CONFIG || {};
      if (config.url && config.key) {
        return fetch(config.url.replace(/\/$/, '') + '/rest/v1/card_feedback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'apikey': config.key,
            'Authorization': 'Bearer ' + config.key,
            'Prefer': 'return=minimal'
          },
          body: payload
        }).then(function (response) {
          if (response.ok) return response;
          throw new Error('Supabase feedback API unavailable');
        });
      }

      var host = window.location.hostname;
      var isLocal = host === '127.0.0.1' || host === 'localhost' || host === '::1';
      if (!isLocal) {
        return Promise.reject(new Error('feedback collection is not configured'));
      }

      return fetch('/api/feedback', options).then(function (response) {
        if (response.ok) return response;
        throw new Error('same-origin feedback API unavailable');
      }).catch(function () {
        return fetch('http://127.0.0.1:8765/api/feedback', options);
      });
    }

    cards.forEach(function (card) {
      if (card.querySelector('.action-card-feedback')) return;

      var cardId = card.getAttribute('data-card-id');
      var toolbar = document.createElement('div');
      toolbar.className = 'action-card-feedback';
      toolbar.setAttribute('aria-label', 'Action Card feedback');

      buttons.forEach(function (cfg) {
        var button = document.createElement('button');
        button.type = 'button';
        button.textContent = cfg.label;
        button.setAttribute('data-feedback-type', cfg.type);
        button.addEventListener('click', function () {
          button.disabled = true;
          postFeedback(cardId, cfg.type).then(function (response) {
            if (!response.ok) throw new Error('feedback API error');
            toolbar.querySelectorAll('button').forEach(function (btn) {
              btn.classList.remove('active');
            });
            button.classList.add('active');
            button.textContent = cfg.label + ' ✓';
          }).catch(function () {
            button.disabled = false;
            button.classList.add('error');
            button.title = '反馈暂未记录，请稍后再试';
          });
        });
        toolbar.appendChild(button);
      });

      var heading = card.querySelector('h2');
      if (heading && heading.parentNode) {
        heading.parentNode.insertBefore(toolbar, heading.nextSibling);
      } else {
        card.insertBefore(toolbar, card.firstChild);
      }
    });
  }

  /** Unlock tutorial member sections with a simple local code list */
  function setupTutorialUnlock() {
    var lock = document.querySelector('[data-tutorial-lock]');
    var content = document.querySelector('[data-tutorial-member-content]');
    if (!lock || !content) return;

    var storageKey = 'xinxianxing-tutorial-unlocked';
    var form = lock.querySelector('.tutorial-unlock-form');
    var input = lock.querySelector('input[name="code"]');
    var message = lock.querySelector('.tutorial-unlock-message');
    var codes = [];

    var script = document.getElementById('tutorial-access-codes');
    if (script) {
      try {
        var payload = JSON.parse(script.textContent || '{}');
        if (Array.isArray(payload.codes)) codes = payload.codes.map(function (code) {
          return String(code).trim();
        }).filter(Boolean);
      } catch (e) {
        codes = [];
      }
    }

    function reveal() {
      content.classList.remove('is-locked');
      lock.hidden = true;
    }

    try {
      if (localStorage.getItem(storageKey) === 'true') {
        reveal();
        return;
      }
    } catch (e) { /* noop */ }

    if (!form || !input) return;

    form.addEventListener('submit', function (event) {
      event.preventDefault();
      var value = input.value.trim();
      if (codes.indexOf(value) !== -1) {
        try { localStorage.setItem(storageKey, 'true'); } catch (e) { /* noop */ }
        reveal();
        return;
      }
      if (message) {
        message.textContent = codes.length ? '授权码不正确，请检查后再试。' : '授权码暂未配置，请联系站点管理员。';
      }
    });
  }

  /** Filter tutorial category cards on the categories page */
  function setupTutorialFilters() {
    var buttons = document.querySelectorAll('.tutorial-filter-button[data-category]');
    var cards = document.querySelectorAll('.tutorial-card[data-category]');
    if (!buttons.length || !cards.length) return;

    var empty = document.querySelector('.tutorial-filter-empty');

    function setCategory(category) {
      var shown = 0;
      buttons.forEach(function (button) {
        button.classList.toggle('active', button.getAttribute('data-category') === category);
      });
      cards.forEach(function (card) {
        var match = category === 'all' || card.getAttribute('data-category') === category;
        card.hidden = !match;
        if (match) shown += 1;
      });
      if (empty) empty.hidden = shown !== 0;
      if (category !== 'all') {
        try { history.replaceState(null, '', '#' + encodeURIComponent(category)); } catch (e) { /* noop */ }
      }
    }

    buttons.forEach(function (button) {
      button.addEventListener('click', function () {
        setCategory(button.getAttribute('data-category') || 'all');
      });
    });

    var initial = decodeURIComponent((window.location.hash || '').replace(/^#/, ''));
    if (initial) {
      var hasInitial = Array.prototype.some.call(buttons, function (button) {
        return button.getAttribute('data-category') === initial;
      });
      if (hasInitial) setCategory(initial);
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    processScoreBadges();
    markSemanticElements();
    setupLanguageToggle();
    setupActionCardFeedback();
    setupTutorialUnlock();
    setupTutorialFilters();
  });
})();
