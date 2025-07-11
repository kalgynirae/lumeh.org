---
title: Fractions
show_authors: true
---

# Fractions

I’m on a quest to have nice-looking fractions for my [recipes]. How do these look on your device?

[recipes]: /recipes/

<figure>
  <div class=fraction-comparison>
    <div><strong>¼</strong><span>single character</span><tt>[U+00BC]</tt></div>
    <div><strong class=skip-fraction-replacement>1⁄4</strong><span>fraction slash</span><tt>[U+0031, U+2044, U+0034]</tt></div>
    <div><strong><span class=hide-if-replaced>–</span><span class=frac>1⁄4</span></strong><span>fixed fraction slash</span><span>(HTML + CSS)</span></div>
  </div>
</figure>
<style>
.fraction-comparison {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  margin-bottom: var(--paragraph-spacing);
  > div {
    display: flex;
    flex-direction: column;
    column-gap: 0.5rem;
    row-gap: 0.5em;
    text-wrap: balance;
    text-align: center;
    strong {
      font-size: 1.5em;
    }
    > *:not(:first-child) {
      line-height: 1;
    }
    > *:nth-child(3) {
      font-size: 0.8em;
    }
  }
}
.hide-if-replaced {
  &:has(+ .frac .replaced-fraction) {
    display: none;
  }
  + .frac {
    display: none;
  }
  + .frac:has(.replaced-fraction) {
    display: inline;
  }
}
</style>

A dash in the rightmost column means that my fix didn’t activate on your device. If anything is
wrong (if the fix is needed but didn’t activate, or if the fix produced weird results), please
<a href="https://github.com/kalgynirae/lumeh.org/issues/new?title=Fraction+disaster&body=%3CPlease+include+a+screenshot+showing+the+difference+and+mention+your+OS+and+browser+version%3E" rel=external target=_blank>let me know</a>!

## Common fractions

Common fractions have their own Unicode codepoints. At time of writing, the full set is:
¼ ½ ¾ ⅐ ⅑ ⅒ ⅓ ⅔ ⅕ ⅖ ⅗ ⅘ ⅙ ⅚ ⅛ ⅜ ⅝ ⅞ ↉. But these have a few problems. They’re limited—no
1⁄16, for example—and many of them just look *wrong*. That’s because this font (<a
href=https://fonts.google.com/specimen/Crimson+Pro rel=external target=_blank>Crimson Pro</a>) only
supplies glyphs for the first three of these fractions; the rest, if you can see them at all, are
coming from fallback fonts chosen by your browser or OS.

<style>
.fraction-images {
  background-color: var(--color-bg-dark);
  padding-bottom: 0.5rem;
  display: grid;
  grid-template-columns: minmax(max-content, 1fr) 2fr;
  column-gap: 0.5rem;
  align-items: center;
  span {
    grid-column: 1;
    text-align: right;
  }
  img {
    grid-column: 2;
    max-width: 26em;
  }
}
</style>
<figure>
  <div class="fraction-images bleed">
    <span>my PC (Linux):</span><img src=unicode-fractions-linux.png>
    <span>my phone (Android):</span><img src=unicode-fractions-android.png>
    <span>my iPad (iPadOS):</span><img src=unicode-fractions-ios.png>
  </div>
  <figcaption>Common fractions as displayed by various devices</figcaption>
</figure>

## The fraction slash

It’s possible to write arbitrary fractions using the character <span class=codepoint>U+2044 FRACTION
SLASH</span> together with ordinary decimal digits. The Unicode spec says that fractions written
this way should be “displayed as a unit.”<a href=#ref1><sup>[1]</sup></a> For example, the sequence
of characters `3` `7` `⁄` `4` `2` should be displayed as 37⁄42. However, this only happens if the
font and the font rendering system both support this.

From my brief testing, fractions written with the fraction slash render correctly in:

* Firefox on Linux, Windows, Android
* Chrome on Linux, Windows, Android

But they don’t render correctly in:

* Safari on iPadOS
* Chrome on iPadOS

These lists are obviously incomplete, but the takeaway for me was that I needed to do something
different for iPadOS devices (and, I’m assuming, other Apple devices).

## Fixing fractions for Apple devices

Goal: Surround each fraction on the page with HTML spans that can be styled with CSS, and, ideally,
only do this when it’s actually needed.

I didn’t like the idea of explicitly marking fractions with special syntax when authoring, so
instead I decided to scan for them later. I used the regular expression `(\d+)\u2044(\d+)` which
matches a sequence of digits, the fraction slash, and another sequence of digits.

To scan each page for fractions, I had two options: I could scan when generating the pages (in my
site generator code) or at page-load time using JavaScript. I opted for the latter because it seemed
easier to implement, but I might revisit this decision.

Here’s the code that replaces the fractions within a particular element. It calls itself recursively
for each child element. When it reaches a text node, if the node’s *textContent* contains a fraction
slash, it replaces the text node with a new *span* element and replaces each contained fraction with
its span-ified version.

<pre><code><span class=kw>function</span> replaceFractions(element) {
  <span class=kw>for</span> (<span class=kw>let</span> <span class=fg-cyan>child</span> <span class=kw>of</span> element.childNodes) {
    <span class=kw>switch</span> (<span class=fg-cyan>child</span>.nodeType) {
      <span class=kw>case</span> Node.ELEMENT_NODE:
        replaceFractions(<span class=fg-cyan>child</span>);
        <span class=kw>break</span>;
      <span class=kw>case</span> Node.TEXT_NODE:
        <span class=kw>if</span> (<span class=fg-cyan>child</span>.textContent.includes("\u2044")) {
          <span class=kw>let</span> <span class=fg-violet>span</span> = document.createElement("span");
          <span class=fg-violet>span</span>.<em>innerHTML</em> = <span class=fg-cyan>child</span>.<em>textContent</em>
            <span class=comment>// Encode the existing text as HTML</span>
            .replaceAll("&amp;", <span class=fg-green>"&amp;amp;"</span>)
            .replaceAll("&lt;", <span class=fg-green>"&amp;lt;"</span>)
            .replaceAll("&gt;", <span class=fg-green>"&amp;gt;"</span>)
            <span class=comment>// Surround fractions with spans</span>
            .replaceAll(
              <span class=fg-red>/(\d+)\u2044(\d+)/g</span>,
              <span class=fg-green>"&lt;span class=replaced-fraction&gt;"</span> +
                <span class=fg-green>"&lt;span class=numerator&gt;<span class=fg-orange>$1</span>&lt;/span&gt;"</span> +
                <span class=fg-green>"&lt;span class=slash&gt;<span class=fg-yellow>\u2044</span>&lt;/span&gt;"</span> +
                <span class=fg-green>"&lt;span class=denominator&gt;<span class=fg-orange>$2</span>&lt;/span&gt;"</span> +
              <span class=fg-green>"&lt;/span&gt;"</span>
            );
          <span class=fg-cyan>child</span>.replaceWith(<span class=fg-violet>span</span>);
        }
        <span class=kw>break</span>;
    }
  }
}
</code></pre>

Note that it would be **wrong** to take the text node’s *textContent* and directly assign it to the
new span’s *innerHTML*. The *textContent* is text, not HTML. It might contain characters like “&lt;”
which would gain undesired meaning if the text were parsed as HTML. So, it’s necessary to convert
the text to HTML by replacing each `&` with `&amp;`, and so on. You can think of this as *encoding*
the text into something that the HTML parser will *decode* back into the original text. Once I have
HTML instead of text, I can replace each bare fraction with its HTML version.

Here’s the CSS I’m using to style these fractions. Note that using *font-variant-position* for
superscript and subscript styles won’t look good unless the font specifically supports it.

<pre><code>.replaced-fraction {
  .numerator {
    font-variant-position: super;
  }
  .denominator {
    font-variant-position: sub;
  }
}
</code></pre>

The final piece of the puzzle is to actually run this code over the whole page, but only on
devices that need it. Ideally, I would be able to detect whether the browser supports fraction
slash rendering, but as far as I can tell this isn’t possible. I settled instead for a simple test
of *navigator.platform*. A Stack Overflow answer<a href=#ref2><sup>[2]</sup></a> suggested some
potential values to check for, but I had to add *mac* to the list to get this to trigger on my iPad.

<pre><code><span class=kw>if</span> (<span class=fg-red>/^(ipad|iphone|ipod|mac)/i</span>.test(navigator.platform)) {
  replaceFractions(document.body);
}
</code></pre>

I expect there to be other devices that need the fix but aren’t covered by this check, but I’ll just
have to wait until people report them to me. I suppose it might be possible to write some code to
measure the width of a rendered fraction and decide based on that… but I’ll save that for later.

## References

<p id=ref1 class=footnote><span class=ref>[1]</span> <a href=https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-6/#G2001 rel=external target=_blank>Unicode 16.0.0 Core Spec, 6.2.9 <em>Other Punctuation</em></a></p>
<p id=ref2 class=footnote><span class=ref>[2]</span> <a href=https://stackoverflow.com/a/19883965 rel=external target=_blank>“What is the list of possible values for navigator.platform as of today?” on Stack Overflow</a></p>
