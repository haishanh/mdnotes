## mdnotes - turning your markdown files into beautiful well structured htmls

[mdnotes][] enable Python markdown [admonition][admonition] extension by default.

for example lines below in markdown:

```
!!! note
    This is a note.
```

will yield:

```
<div class="admonition note">
  <p class="admonition-title">Note</p>
  <p>This is a note.</p>
</div>
```

You can place any world after "!!!", but currently, only `note`, `warning`, and `danger` will be properly styled. 


### Write in markdown

There are many tutorials or blog posts tell you the syntax about markdown. By here are some sugars in `mdnotes`:

<kbd>CTRL</kbd>+<kbd>SHIFT</kbd>


[mdnotes]: TODO
[admonition]: https://pythonhosted.org/Markdown/extensions/admonition.html
