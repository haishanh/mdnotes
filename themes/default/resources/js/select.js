(function () {
    var tagSelect = document.getElementById('tagSelect');
    tagSelect.onchange = function () { window.location.href = this.value;};

    var all_headings = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7'];
    var article_headings = '';
    for (var i=0; i<all_headings.length, i++)
    {
      article_headings += 'article > ' + all_headings[i];
    }
    article_headings = document.querySelectorAll(article_headings);
    for (var i=0; i<article_headings.length, i++)
    {
      var headerlink = article_headings[i].querySelector('.headerlink');
      article_headings[i].onmouseover = function (){ headerlink.style.display = 'inline';};
      article_headings[i].onmouseout  = function (){ headerlink.style.display = 'none';};
    }
})();
