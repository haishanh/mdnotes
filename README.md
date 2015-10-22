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


### Configuration

The global config file is `config.yml`

```
TODO example
```

#### source_dir

`source_dir` is the the path where you put your markdown files. Please be noted, directory place directly in `source_dir` will be treated as kind of category. So if your `source_dir` is `notes`

 * The url of the file `notes/dir1/dir2/this-is-a-test.md` will be '<yoursite.com>/<root_dir>/dir1/this-is-a-test'
 * The url of the file `notes/dir1/this-is-a-test.md` will be '<yoursite.com>/<root_dir>/dir1/this-is-a-test'
 * The url of the file `notes/this-is-a-test.md` will be '<yoursite.com>/<root_dir>/this-is-a-test'

### Write in markdown

There are many tutorials or blog posts tell you the syntax about markdown. By here are some sugars in `mdnotes`:

<kbd>CTRL</kbd>+<kbd>SHIFT</kbd>


[mdnotes]: TODO
[admonition]: https://pythonhosted.org/Markdown/extensions/admonition.html
