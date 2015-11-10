function addAnchors() {
  var all_headings = ['h1, ', 'h2, ', 'h3, ', 'h4, ', 'h5, ', 'h6, ', 'h7'];
  var article_headings = '';
  for (var i=0; i<all_headings.length; i++) {
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

function stickToc() {
  var toc = $("#toc");
  var window_top = $(window).scrollTop();
  var left_top = $("#left").offset().top;
  if (window_top > left_top) {
    toc.addClass("fixed");
  } else {
    toc.removeClass("fixed");
  }
}

(function () {
  var dropdownElements = document.getElementsByClassName('dropdown-select');
  for (var i = 0; i < dropdownElements.length; i++) {
    dropdownElements[i].onchange = function () { 
      window.location.href = this.value;
    };
  }
  addAnchors();
  //$(window).scroll(stickToc);
})();


$(function () {
  $(window).scroll(stickToc);
  stickToc();
});
