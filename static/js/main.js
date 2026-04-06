(function () {
  var siteNav = document.getElementById("siteNav");
  var navVisible = document.getElementById("navVisible");
  var navMore = document.getElementById("navMore");
  var moreBtn = document.getElementById("moreBtn");
  var navHidden = document.getElementById("navHidden");

  if (!siteNav || !navVisible || !navMore || !moreBtn || !navHidden) {
    return;
  }

  function closeMore() {
    navMore.classList.remove("is-open");
    moreBtn.setAttribute("aria-expanded", "false");
  }

  function moveHiddenBack() {
    while (navHidden.firstElementChild) {
      navVisible.appendChild(navHidden.firstElementChild);
    }
  }

  function rebalanceMenu() {
    closeMore();
    moveHiddenBack();

    navMore.style.display = "inline-flex";

    var availableWidth = siteNav.clientWidth - navMore.offsetWidth - 8;

    while (navVisible.scrollWidth > availableWidth && navVisible.lastElementChild) {
      navHidden.insertBefore(navVisible.lastElementChild, navHidden.firstElementChild);
    }

    if (navHidden.children.length === 0) {
      navMore.style.display = "none";
      closeMore();
    } else {
      navMore.style.display = "inline-flex";
    }
  }

  moreBtn.addEventListener("click", function (event) {
    event.stopPropagation();

    if (navHidden.children.length === 0) {
      return;
    }

    var willOpen = !navMore.classList.contains("is-open");
    navMore.classList.toggle("is-open", willOpen);
    moreBtn.setAttribute("aria-expanded", willOpen ? "true" : "false");
  });

  document.addEventListener("click", function (event) {
    if (!navMore.contains(event.target)) {
      closeMore();
    }
  });

  navHidden.addEventListener("click", function (event) {
    if (event.target.closest("a")) {
      closeMore();
    }
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      closeMore();
    }
  });

  var resizeTimer = null;
  function onResize() {
    window.clearTimeout(resizeTimer);
    resizeTimer = window.setTimeout(rebalanceMenu, 150);
  }

  document.addEventListener("DOMContentLoaded", rebalanceMenu);
  window.addEventListener("resize", onResize);
  window.addEventListener("load", rebalanceMenu);
})();

(function () {
  var heroElements = Array.prototype.slice.call(
    document.querySelectorAll("[data-home-hero], [data-page-hero]")
  );

  if (heroElements.length === 0) {
    return;
  }

  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  var rafId = 0;
  var heroStates = [];

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function getTargetProgress(hero) {
    var rect = hero.getBoundingClientRect();
    var travelled = clamp(-rect.top, 0, hero.offsetHeight * 1.25);
    var maxTravel = Math.max(hero.offsetHeight * 1.25, 1);
    return travelled / maxTravel;
  }

  function render(hero, progress) {
    var opacity = 1 - progress * 0.48;
    var shift = prefersReducedMotion.matches ? 0 : progress * 64;

    hero.style.setProperty("--hero-image-opacity", opacity.toFixed(3));
    hero.style.setProperty("--hero-image-shift", shift.toFixed(2) + "px");
  }

  function stopAnimation() {
    if (rafId) {
      window.cancelAnimationFrame(rafId);
      rafId = 0;
    }
  }

  function animate() {
    var shouldContinue = false;

    heroStates.forEach(function (state) {
      var delta = state.target - state.current;
      state.current += delta * (prefersReducedMotion.matches ? 1 : 0.12);
      render(state.element, state.current);

      if (Math.abs(delta) < 0.0015) {
        state.current = state.target;
        render(state.element, state.current);
        return;
      }

      shouldContinue = true;
    });

    if (!shouldContinue) {
      stopAnimation();
      return;
    }

    rafId = window.requestAnimationFrame(animate);
  }

  function syncHeroState() {
    heroStates.forEach(function (state) {
      state.target = getTargetProgress(state.element);

      if (prefersReducedMotion.matches) {
        state.current = state.target;
        render(state.element, state.current);
      }
    });

    if (prefersReducedMotion.matches) {
      stopAnimation();
      return;
    }

    if (!rafId) {
      rafId = window.requestAnimationFrame(animate);
    }
  }

  heroStates = heroElements.map(function (hero) {
    var progress = getTargetProgress(hero);
    render(hero, progress);
    return {
      element: hero,
      current: progress,
      target: progress,
    };
  });

  window.addEventListener("scroll", syncHeroState, { passive: true });
  window.addEventListener("resize", syncHeroState);

  if (typeof prefersReducedMotion.addEventListener === "function") {
    prefersReducedMotion.addEventListener("change", syncHeroState);
  } else if (typeof prefersReducedMotion.addListener === "function") {
    prefersReducedMotion.addListener(syncHeroState);
  }
})();
