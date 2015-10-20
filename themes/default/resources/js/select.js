function addAnchors() {
  var all_headings = ['h1, ', 'h2, ', 'h3, ', 'h4, ', 'h5, ', 'h6, ', 'h7'];
  var article_headings = '';
  for (var i=0; i<all_headings.length; i++)
  {
    article_headings += 'article > ' + all_headings[i];
  }
  for (var a = document.querySelectorAll(article_headings), b = 0, c = a.length; c > b; b++) {
    var d = a[b],
      e = document.createElement("a");
    e.href = "#" + d.id, e.textContent = "§", e.className = "header-anchor", d.insertBefore(e, d.firstChild);
    d.onmouseover = function () { this.firstElementChild.style.display = 'inline'; };
    d.onmouseout  = function () { this.firstElementChild.style.display = 'none'; };
  }
}

(function () {
  var tagSelect = document.getElementById('tagSelect');
  if (tagSelect) {
    tagSelect.onchange = function () { window.location.href = this.value;};
  }

  addAnchors();
})();
