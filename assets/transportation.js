(() => {
  'use strict';
  const configured = window.PORTFOLIO_TABLEAU?.url;
  if (!configured) return;
  let url;
  try { url = new URL(configured); } catch { return; }
  if (url.protocol !== 'https:' || url.hostname !== 'public.tableau.com' || !url.pathname.startsWith('/views/')) return;
  const publicUrl = url.toString();
  url.searchParams.set(':showVizHome', 'no');
  url.searchParams.set(':embed', 'yes');
  url.searchParams.set(':tabs', 'yes');
  url.searchParams.set(':toolbar', 'yes');
  const frame = document.createElement('iframe');
  frame.title = 'Transportation Performance and Risk — Tableau Public dashboard';
  frame.src = url.toString();
  frame.loading = 'lazy';
  frame.referrerPolicy = 'strict-origin-when-cross-origin';
  frame.allowFullscreen = true;
  document.getElementById('tableau-embed').append(frame);
  document.getElementById('tableau-link').href = publicUrl;
  document.getElementById('tableau-section').hidden = false;
})();
