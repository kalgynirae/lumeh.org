---
title: Characters
---

This is Colin’s personal collection of useful characters for easy copying & pasting.

<div class=characters>

<div class=char>‘</div>
<div class=code>U+2018</div>
<div class=name>LEFT SINGLE QUOTATION MARK</div>

<div class=char>’</div>
<div class=code>U+2019</div>
<div class=name>RIGHT SINGLE QUOTATION MARK (apostrophe)</div>

<div class=char>“</div>
<div class=code>U+201C</div>
<div class=name>LEFT DOUBLE QUOTATION MARK</div>

<div class=char>”</div>
<div class=code>U+201D</div>
<div class=name>RIGHT DOUBLE QUOTATION MARK</div>

<div class=char>‑</div>
<div class=code>U+2011</div>
<div class=name>NON-BREAKING HYPHEN</div>

<div class=char>‒</div>
<div class=code>U+2012</div>
<div class=name>FIGURE DASH</div>

<div class=char>–</div>
<div class=code>U+2013</div>
<div class=name>EN DASH</div>

<div class=char>—</div>
<div class=code>U+2014</div>
<div class=name>EM DASH</div>

<div class=char>&#x00A0;</div>
<div class=code>U+00A0</div>
<div class=name>NO-BREAK SPACE</div>

<div class=char>&#x2007;</div>
<div class=code>U+2007</div>
<div class=name>FIGURE SPACE</div>

<div class=char>&#x2009;</div>
<div class=code>U+2009</div>
<div class=name>THIN SPACE</div>

<div class=char>&#x200A;</div>
<div class=code>U+200A</div>
<div class=name>HAIR SPACE</div>

<div class=char>&#x200B;</div>
<div class=code>U+200B</div>
<div class=name>ZERO WIDTH SPACE</div>

<div class=char>&#x202F;</div>
<div class=code>U+202F</div>
<div class=name>NARROW NO-BREAK SPACE</div>

<div class=char>•</div>
<div class=code>U+2022</div>
<div class=name>BULLET</div>

<div class=char>…</div>
<div class=code>U+2026</div>
<div class=name>HORIZONTAL ELLIPSIS</div>

<div class=char>␤</div>
<div class=code>U+2424</div>
<div class=name>SYMBOL FOR NEWLINE</div>

<div class=char>♭</div>
<div class=code>U+266D</div>
<div class=name>MUSIC FLAT SIGN</div>

<div class=char>♮</div>
<div class=code>U+266E</div>
<div class=name>MUSIC NATURAL SIGN</div>

<div class=char>♯</div>
<div class=code>U+266F</div>
<div class=name>MUSIC SHARP SIGN</div>

<div class=char><a class=pentagon href=https://aac.unicode.org/sponsors#bronze-2bc2 rel=external target=_blank>⯂</a></div>
<div class=code>U+2BC2</div>
<div class=name>TURNED BLACK PENTAGON</div>

</div>

<script>
document.querySelectorAll(".char").forEach((div) => {
  div.addEventListener("click", (event) => {
    document.querySelectorAll(".char").forEach((e) => {
      e.classList.remove("copied");
    });
    var char = event.target.textContent;
    navigator.clipboard.writeText(char).then(() => {
      event.target.classList.add("copied");
    }, () => {
      event.target.classList.add("failed-copy");
    });
  });
});
</script>
