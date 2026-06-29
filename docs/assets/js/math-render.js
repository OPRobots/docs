/* KaTeX auto-render para arithmatex en modo generic.
   Escucha el evento document$ de MkDocs Material para re-renderizar
   tras navegación instantánea. */

document$.subscribe(function () {
  document.querySelectorAll('.arithmatex').forEach(function (el) {
    var tex = el.textContent;
    // Display math: \[ ... \] (generado desde $$...$$)
    if (tex.startsWith('\\[') && tex.endsWith('\\]')) {
      tex = tex.slice(2, -2);
      katex.render(tex, el, {
        displayMode: true,
        throwOnError: false,
      });
    }
    // Inline math: \( ... \) (generado desde $...$)
    else if (tex.startsWith('\\(') && tex.endsWith('\\)')) {
      tex = tex.slice(2, -2);
      katex.render(tex, el, {
        displayMode: false,
        throwOnError: false,
      });
    }
  });
});
