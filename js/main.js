/* Vance Dental Studio: site behaviors */
(function () {
  "use strict";

  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));

  /* Theme */
  const root = document.documentElement;
  const themeKey = "vd-theme";
  function preferredTheme() {
    const stored = localStorage.getItem(themeKey);
    if (stored === "light" || stored === "dark") return stored;
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function applyTheme(t) {
    root.classList.toggle("dark", t === "dark");
    root.classList.toggle("light", t === "light");
    const meta = $('meta[name="theme-color"]');
    if (meta) meta.setAttribute("content", t === "dark" ? "#151310" : "#F3F0EA");
    $$("[data-theme-toggle]").forEach((btn) => {
      btn.setAttribute("aria-checked", t === "dark" ? "true" : "false");
      btn.setAttribute("aria-label", t === "dark" ? "Switch to light mode" : "Switch to dark mode");
    });
    localStorage.setItem(themeKey, t);
  }
  applyTheme(preferredTheme());
  $$("[data-theme-toggle]").forEach((btn) => {
    btn.addEventListener("click", () => applyTheme(root.classList.contains("dark") ? "light" : "dark"));
  });
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
    if (!localStorage.getItem(themeKey)) applyTheme(e.matches ? "dark" : "light");
  });

  /* Scroll progress + header + floating controls */
  const header = $("[data-header]");
  const progress = $("[data-scroll-progress] span");
  const backTop = $("[data-back-top]");
  const mobileCta = $("[data-mobile-cta]");
  function onScroll() {
    const y = window.scrollY || 0;
    const doc = document.documentElement;
    const max = doc.scrollHeight - doc.clientHeight;
    if (progress && max > 0) progress.style.width = `${Math.min(100, (y / max) * 100)}%`;
    if (header) header.classList.toggle("is-scrolled", y > 12);
    if (backTop) backTop.classList.toggle("is-visible", y > 480);
    if (mobileCta) {
      const show = y > 320;
      mobileCta.classList.toggle("is-visible", show);
      document.body.classList.toggle("has-mobile-cta", show);
    }
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
  if (backTop) backTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));

  /* Drawer */
  const drawer = $("[data-drawer]");
  const drawerOverlay = $("[data-drawer-overlay]");
  const menuBtn = $("[data-menu-open]");
  const menuClose = $("[data-menu-close]");
  let lastFocus = null;
  function openDrawer() {
    if (!drawer) return;
    lastFocus = document.activeElement;
    drawer.classList.add("is-open");
    drawerOverlay?.classList.add("is-open");
    drawer.setAttribute("aria-hidden", "false");
    menuBtn?.setAttribute("aria-expanded", "true");
    document.body.style.overflow = "hidden";
    menuClose?.focus();
  }
  function closeDrawer() {
    if (!drawer) return;
    drawer.classList.remove("is-open");
    drawerOverlay?.classList.remove("is-open");
    drawer.setAttribute("aria-hidden", "true");
    menuBtn?.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
    lastFocus?.focus?.();
  }
  menuBtn?.addEventListener("click", openDrawer);
  menuClose?.addEventListener("click", closeDrawer);
  drawerOverlay?.addEventListener("click", closeDrawer);
  drawer?.querySelectorAll("a").forEach((a) => a.addEventListener("click", closeDrawer));

  /* Modal booking */
  const modal = $("[data-booking-modal]");
  function openModal() {
    if (!modal) return;
    lastFocus = document.activeElement;
    closeDrawer();
    modal.classList.add("is-open");
    modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    const first = modal.querySelector("input, select, button");
    setTimeout(() => first?.focus(), 50);
  }
  function closeModal() {
    if (!modal) return;
    modal.classList.remove("is-open");
    modal.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    lastFocus?.focus?.();
  }
  $$("[data-book-open]").forEach((el) => el.addEventListener("click", (e) => {
    e.preventDefault();
    openModal();
  }));
  modal?.querySelector("[data-book-close]")?.addEventListener("click", closeModal);
  modal?.addEventListener("click", (e) => { if (e.target === modal) closeModal(); });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeModal();
      closeDrawer();
      closeSearch();
    }
  });

  /* Toasts */
  const toastRegion = $("[data-toast-region]");
  function toast(message, opts = {}) {
    if (!toastRegion) return;
    const el = document.createElement("div");
    el.className = "toast";
    el.setAttribute("role", "status");
    el.setAttribute("aria-live", "polite");
    el.innerHTML = `<div>${message}</div>`;
    toastRegion.appendChild(el);
    const ttl = opts.ttl || 4200;
    setTimeout(() => {
      el.style.opacity = "0";
      el.style.transform = "translateY(6px)";
      el.style.transition = "opacity 200ms ease, transform 200ms ease";
      setTimeout(() => el.remove(), 220);
    }, ttl);
  }
  window.vdToast = toast;

  /* Booking form */
  const bookingForm = $("[data-booking-form]");
  bookingForm?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.currentTarget;
    let valid = true;
    $$("[required]", form).forEach((field) => {
      const wrap = field.closest(".field");
      const ok = field.value && String(field.value).trim().length > 0 && field.checkValidity();
      wrap?.classList.toggle("has-error", !ok);
      field.classList.toggle("is-error", !ok);
      if (!ok) valid = false;
    });
    if (!valid) {
      const firstErr = form.querySelector(".is-error");
      firstErr?.focus();
      toast("Please correct the highlighted fields.");
      return;
    }
    const btn = form.querySelector('[type="submit"]');
    const original = btn.innerHTML;
    btn.classList.add("is-loading");
    btn.innerHTML = `<span class="spinner" aria-hidden="true"></span> Confirming…`;
    await wait(900);
    btn.classList.remove("is-loading");
    btn.innerHTML = original;
    closeModal();
    form.reset();
    toast("Request received. We will confirm within 24 hours.");
    // Soft navigate to thank-you if present
    if (window.location.pathname.endsWith("index.html") || window.location.pathname.endsWith("/") || window.location.pathname === "") {
      // stay; toast is enough on home. Optional:
    }
  });

  /* Newsletter */
  $$("[data-newsletter]").forEach((form) => {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = form.querySelector('input[type="email"]');
      if (!email?.checkValidity()) {
        email?.classList.add("is-error");
        email?.focus();
        toast("Enter a valid email address.");
        return;
      }
      const btn = form.querySelector('[type="submit"]');
      const original = btn.innerHTML;
      btn.classList.add("is-loading");
      btn.disabled = true;
      btn.innerHTML = `<span class="spinner" aria-hidden="true"></span>`;
      await wait(700);
      btn.classList.remove("is-loading");
      btn.disabled = false;
      btn.innerHTML = original;
      email.value = "";
      toast("Subscribed. Oral health notes will arrive monthly.");
    });
  });

  /* FAQ accordion (details): keep only one open, optional */
  $$("[data-faq] details").forEach((d) => {
    d.addEventListener("toggle", () => {
      if (d.open) {
        $$("[data-faq] details").forEach((other) => {
          if (other !== d) other.open = false;
        });
      }
    });
  });

  /* Tabs */
  $$("[data-tabs]").forEach((tabs) => {
    const triggers = $$('[role="tab"]', tabs);
    const panels = $$('[role="tabpanel"]', tabs.parentElement || document);
    triggers.forEach((tab) => {
      tab.addEventListener("click", () => {
        const id = tab.getAttribute("aria-controls");
        triggers.forEach((t) => {
          t.setAttribute("aria-selected", t === tab ? "true" : "false");
          t.tabIndex = t === tab ? 0 : -1;
        });
        panels.forEach((p) => {
          if (!p.id) return;
          const match = p.id === id;
          p.hidden = !match;
        });
        // URL as state
        const key = tab.dataset.tab;
        if (key) {
          const url = new URL(window.location.href);
          url.searchParams.set("view", key);
          history.replaceState({}, "", url);
        }
      });
    });
    const urlView = new URL(window.location.href).searchParams.get("view");
    if (urlView) {
      const match = triggers.find((t) => t.dataset.tab === urlView);
      match?.click();
    }
  });

  /* Opening hours status */
  function updateOpenStatus() {
    const badge = $("[data-open-status]");
    if (!badge) return;
    const now = new Date();
    // Convert to America/New_York approximation via Intl
    const parts = new Intl.DateTimeFormat("en-US", {
      timeZone: "America/New_York",
      weekday: "short",
      hour: "numeric",
      hour12: false,
    }).formatToParts(now);
    const weekday = parts.find((p) => p.type === "weekday")?.value;
    const hour = Number(parts.find((p) => p.type === "hour")?.value);
    const map = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    const day = map[weekday] ?? now.getDay();
    let open = false;
    if (day >= 1 && day <= 5 && hour >= 8 && hour < 19) open = true;
    if (day === 6 && hour >= 9 && hour < 16) open = true;
    badge.textContent = open ? "Open now" : "Closed now";
    badge.className = `badge badge-dot ${open ? "badge-success" : "badge-danger"}`;
    badge.setAttribute("role", "status");
  }
  updateOpenStatus();
  setInterval(updateOpenStatus, 60000);

  /* Copy buttons */
  $$("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const value = btn.getAttribute("data-copy") || "";
      try {
        await navigator.clipboard.writeText(value);
        const prev = btn.textContent;
        btn.textContent = "Copied";
        toast("Copied to clipboard.");
        setTimeout(() => { btn.textContent = prev; }, 1600);
      } catch {
        toast("Could not copy. Select the text manually.");
      }
    });
  });

  /* Cookie banner + optional analytics (only after accept) */
  const cookie = $("[data-cookie]");
  function loadAnalytics() {
    if (window.__vdGa) return;
    window.__vdGa = true;
    // Privacy-respecting stub: replace MEASUREMENT_ID after Netlify deploy if desired.
    // Loads only when the visitor accepts cookies.
    const id = window.VD_GA_ID;
    if (!id || id === "G-XXXXXXXX") return;
    const s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(id);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag("js", new Date());
    gtag("config", id, { anonymize_ip: true });
  }
  const cookiePref = localStorage.getItem("vd-cookie");
  if (cookie && !cookiePref) cookie.classList.add("is-visible");
  if (cookiePref === "accepted") loadAnalytics();
  $("[data-cookie-accept]")?.addEventListener("click", () => {
    localStorage.setItem("vd-cookie", "accepted");
    cookie?.classList.remove("is-visible");
    loadAnalytics();
  });
  $("[data-cookie-reject]")?.addEventListener("click", () => {
    localStorage.setItem("vd-cookie", "rejected");
    cookie?.classList.remove("is-visible");
  });

  /* Site search */
  const searchInput = $("[data-site-search]");
  const searchResults = $("[data-search-results]");
  const SEARCH_INDEX = [
    { title: "Cosmetic dentistry", url: "services.html#cosmetic", body: "Veneers, bonding and whitening. Shade matched to your own enamel, with a mock-up before any tooth is prepared." },
    { title: "Dental implants", url: "services.html#implants", body: "Planned on a CBCT scan and placed through a printed surgical guide. Single tooth to full arch." },
    { title: "Invisalign", url: "services.html#invisalign", body: "Clear aligners staged from an intraoral scan. Check-ups every six to eight weeks, one refinement phase included." },
    { title: "General checkup", url: "services.html#checkup", body: "Exams and cleanings with periodontal charting at every visit. X-rays only when a finding needs following up." },
    { title: "Book an appointment", url: "contact.html", body: "Ask for a date by form or phone. Requests are answered within 24 hours." },
    { title: "Studio location", url: "visit.html", body: "1200 Avenue of the Americas, Suite 400, New York, NY 10036." },
    { title: "Opening hours", url: "visit.html#hours", body: "Monday to Friday 08:00-19:00. Saturday 09:00-16:00. Sunday closed." },
    { title: "Patient forms", url: "patients.html", body: "New-patient paperwork sent by secure link after booking, or filled in at reception 15 minutes early." },
    { title: "Insurance information", url: "patients.html#insurance", body: "Out-of-network with most PPO plans. The office files the claim. HSA and FSA cards accepted." },
    { title: "Privacy Policy", url: "privacy.html", body: "What the site collects, who it is shared with, cookie settings and how to request a copy." },
    { title: "Terms of Service", url: "terms.html", body: "Rules for using the website, booking requests, site content and liability." },
    { title: "Gallery", url: "gallery.html", body: "Photographs of the treatment rooms, waiting room and sterilization area on Avenue of the Americas." },
    { title: "About Dr. Alistair Vance", url: "about.html", body: "DDS, restorative and implant dentistry, 18 years in practice. One address, no second location." },
    { title: "FAQs", url: "index.html#faq", body: "How soon you can be seen, insurance, access, what to bring, sedation and parking." },
    { title: "Case studies", url: "cases.html", body: "Three write-ups: veneers after grinding wear, a guided lower molar implant, aligners for adult crowding." },
  ];
  function renderSearch(q) {
    if (!searchResults) return;
    const query = (q || "").trim().toLowerCase();
    if (!query) {
      searchResults.innerHTML = `<div class="search-empty">Start typing to search the site.</div>`;
      return;
    }
    const hits = SEARCH_INDEX.filter((item) =>
      (item.title + " " + item.body).toLowerCase().includes(query)
    ).slice(0, 8);
    if (!hits.length) {
      searchResults.innerHTML = `<div class="search-empty">No matches for "${escapeHtml(q)}". Try "implants", "hours" or "insurance".</div>`;
      return;
    }
    searchResults.innerHTML = hits.map((h) => `
      <a class="search-hit" href="${h.url}">
        <h3>${escapeHtml(h.title)}</h3>
        <p>${escapeHtml(h.body)}</p>
      </a>
    `).join("");
  }
  searchInput?.addEventListener("input", (e) => renderSearch(e.target.value));
  if (searchInput) renderSearch("");
  function closeSearch() {}

  /* UTM capture */
  try {
    const params = new URLSearchParams(window.location.search);
    const utm = {};
    ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content"].forEach((k) => {
      if (params.get(k)) utm[k] = params.get(k);
    });
    if (Object.keys(utm).length) sessionStorage.setItem("vd-utm", JSON.stringify(utm));
  } catch (_) { /* ignore */ }

  /* Map */
  const mapEl = $("#map");
  if (mapEl && window.L) {
    const lat = 40.758896;
    const lng = -73.985130;
    const map = L.map(mapEl, { scrollWheelZoom: false, attributionControl: true }).setView([lat, lng], 15);
    L.tileLayer("https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
      maxZoom: 19,
    }).addTo(map);
    const icon = L.divIcon({
      className: "",
      html: `<div style="width:32px;height:32px;background:#A67C52;border-radius:50%;border:3px solid #fff;box-shadow:0 4px 12px rgba(0,0,0,.18);display:flex;align-items:center;justify-content:center;">
        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
      </div>`,
      iconSize: [32, 32],
      iconAnchor: [16, 32],
    });
    L.marker([lat, lng], { icon })
      .addTo(map)
      .bindPopup(`<strong>Vance Dental Studio</strong><br><span style="color:#5A554C;font-size:12px;">1200 Ave of the Americas</span>`)
      .openPopup();
  }

  /* Helpers */
  function wait(ms) {
    return new Promise((r) => setTimeout(r, ms));
  }
  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    })[c]);
  }

  /* Year */
  $$("[data-year]").forEach((el) => { el.textContent = String(new Date().getFullYear()); });
})();
