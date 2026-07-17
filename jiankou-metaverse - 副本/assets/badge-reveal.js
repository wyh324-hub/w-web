(function () {
  const BADGE_IMAGES = {
    '情报尖兵': 'assets/badges/qingbaojianbing.png',
    '无名坚守者': 'assets/badges/wumingjianshouzhe.png',
    '古道交通员': 'assets/badges/gudaojiaotongyuan.png',
    '初心铭记者': 'assets/badges/chuxinmingjizhe.png',
    '英雄致敬人': 'assets/badges/yingxiongzhiqingren.png',
  };

  let active = false;
  let timer = null;

  function ensureOverlay() {
    let el = document.getElementById('badgeRevealOverlay');
    if (el) return el;
    el = document.createElement('div');
    el.id = 'badgeRevealOverlay';
    el.innerHTML =
      '<div class="badge-reveal-bg"></div>' +
      '<div class="badge-reveal-rays"></div>' +
      '<div class="badge-reveal-content">' +
      '<p class="badge-reveal-label">获得徽章</p>' +
      '<img class="badge-reveal-img" alt="" />' +
      '<p class="badge-reveal-name"></p>' +
      '</div>';
    document.body.appendChild(el);
    return el;
  }

  window.playBadgeReveal = function (badgeName, onDone) {
    const src = BADGE_IMAGES[badgeName];
    if (!src) {
      if (onDone) onDone();
      return;
    }
    if (active) {
      if (onDone) onDone();
      return;
    }
    active = true;
    const overlay = ensureOverlay();
    const img = overlay.querySelector('.badge-reveal-img');
    const nameEl = overlay.querySelector('.badge-reveal-name');
    img.src = src;
    img.alt = badgeName;
    nameEl.textContent = '「' + badgeName + '」';
    overlay.classList.remove('hide', 'animate');
    overlay.classList.add('show');
    requestAnimationFrame(() => {
      requestAnimationFrame(() => overlay.classList.add('animate'));
    });

    if (timer) clearTimeout(timer);
    timer = setTimeout(() => {
      overlay.classList.remove('animate', 'show');
      overlay.classList.add('hide');
      active = false;
      timer = null;
      if (onDone) onDone();
    }, 3000);
  };

  window.hasBadgeRevealImage = function (badgeName) {
    return !!BADGE_IMAGES[badgeName];
  };
})();
