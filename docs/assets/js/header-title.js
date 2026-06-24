/* ==========================================================================
   Dynamic header title — breadcrumb with visual hierarchy
   Updates on every navigation (including instant)
   ========================================================================== */

document$.subscribe(function () {
  var path = window.location.pathname;
  var parts = path.replace(/\/$/, "").split("/").filter(Boolean);
  var siteName = "Documentación";
  var title;

  if (parts.length === 0) {
    // Homepage — plain title, full opacity
    title = siteName;
  } else {
    // Section + page title
    var section = parts[0];
    var h1 = document.querySelector("h1");
    var pageTitle = h1 ? h1.textContent.trim() : parts[parts.length - 1];
    title =
      '<span class="header-breadcrumb-base">' + siteName + '</span>'
      + ' <span class="header-breadcrumb-sep">/</span> '
      + '<span class="header-breadcrumb-section">' + section + '</span>'
      + ' <span class="header-breadcrumb-sep">/</span> '
      + '<span class="header-breadcrumb-page">' + pageTitle + '</span>';
  }

  // Update the first header topic (site name area)
  var headerTopic = document.querySelector(
    '[data-md-component="header-title"] .md-header__topic:not([data-md-component="header-topic"]) .md-ellipsis'
  );
  if (headerTopic) {
    headerTopic.innerHTML = title;
  }
});
