---
title: Fractions
---

# Fractions

I often write recipes, and I think <samp>1⁄2 cup</samp> looks a lot better than <samp>1/2 cup</samp>
or <samp>0.5 cup</samp>. This page documents the complications I ran into while achieving this.

## Predefined fraction characters

Unicode defines codepoints for commonly-used fractions. At time of writing, the full set is: ¼ ½
¾ ⅐ ⅑ ⅒ ⅓ ⅔ ⅕ ⅖ ⅗ ⅘ ⅙ ⅚ ⅛ ⅜ ⅝ ⅞ ↉. But these have a few problems. For my use case, the main issue
is that most of these fractions *look wrong*. That’s because the font I’m using (Crimson Pro)
only supplies glyphs for the first three of these fractions; the rest end up being rendered using
fallback fonts chosen by the OS or browser.

## The fraction slash

It’s possible to write arbitrary fractions using the character <span class=codepoint>U+2044 FRACTION
SLASH</span> with one or more ordinary decimal digits on each side. The Unicode spec says that fractions written this way should be “displayed as a unit.”<a href=#ref1><sup>[1]</sup></a> For
example, the sequence of characters `3` `7` `⁄` `4` `2` should be displayed as 37⁄42. However, this
only happens if the font and the font rendering system both support this.

From my brief testing, fractions written with the fraction slash render correctly in:

* Firefox on Linux, Windows, Android
* Chrome on Linux, Windows, Android

But they don’t render correctly in:

* Safari on iOS
* Chrome on iOS

These lists are obviously incomplete, but the takeaway for me was that I needed to do something
different for iOS browsers.

## Fixing fractions for iOS browsers

Ideally, I would be able to detect whether the browser supports rendering fraction slashes
correctly, but this isn’t currently possible (as far as I can tell). The next best option is to
detect whether the browser is running on iOS. It’s not possible to do this 100% reliably, but
based on a <a href=https://stackoverflow.com/a/19883965 rel=external target=_blank>StackOverflow
answer</a> I came up with the following test:

<pre><code>if (<span class=fg-magenta>/^(ipad|iphone|ipod|mac)/i</span>.test(navigator.<em>platform</em>)) {
  replaceFractions(document.body);
}
</code></pre>

This correctly triggers in Safari on an iPad Pro (the only iOS device I have access to).

The next step is to process the whole document and add structure around fractions so that I can
style them with CSS. I did this by looking for relevant text nodes (those whose text contains a
fraction slash) and replacing them with new span elements. Because I’m adding HTML tags to the
existing text and then using it as the new span’s `innerHTML`, I first need to escape characters in
the existing text that could have special meaning to the HTML parser.

<pre><code>function replaceFractions(element) {
  for (let <span class=fg-cyan>child</span> of element.childNodes) {
    switch (<span class=fg-cyan>child</span>.nodeType) {
      case Node.ELEMENT_NODE:
        replaceFractions(<span class=fg-cyan>child</span>);
        break;
      case Node.TEXT_NODE:
        if (<span class=fg-cyan>child</span>.<em>textContent</em>.includes("\u2044")) {
          let <span class=fg-violet>span</span> = document.createElement(<span class=fg-green>"span"</span>);
          <span class=fg-violet>span</span>.<em>innerHTML</em> = <span class=fg-cyan>child</span>.<em>textContent</em>
            <span class=comment>// Encode the existing text as HTML</span>
            .replaceAll("&amp;", <span class=fg-green>"&amp;amp;"</span>)
            .replaceAll("&lt;", <span class=fg-green>"&amp;lt;"</span>)
            .replaceAll("&gt;", <span class=fg-green>"&amp;gt;"</span>)
            <span class=comment>// Surround fraction slash occurrences with spans</span>
            .replaceAll(
              <span class=fg-magenta>/(\d+)\u2044(\d+)/g</span>,
              <span class=fg-green>"&lt;span class=replaced-fraction&gt;"</span> +
                <span class=fg-green>"&lt;span class=numerator&gt;<span class=fg-orange>$1</span>&lt;/span&gt;"</span> +
                <span class=fg-green>"&lt;span class=slash&gt;\u2044&lt;/span&gt;"</span> +
                <span class=fg-green>"&lt;span class=denominator&gt;<span class=fg-orange>$2</span>&lt;/span&gt;"</span> +
              <span class=fg-green>"&lt;/span&gt;"</span>
            );
          <span class=fg-cyan>child</span>.replaceWith(<span class=fg-violet>span</span>);
        }
        break;
    }
  }
}
</code></pre>

And here’s the CSS:

<pre><code>.replaced-fraction {
  .numerator {
    font-variant-position: super;
  }
  .denominator {
    font-variant-position: sub;
  }
}
</code></pre>

## References

<p id=ref1 class=footnote>[1] <a href=https://www.unicode.org/versions/Unicode16.0.0/core-spec/chapter-6/#G2001 rel=external target=_blank>Unicode 16.0.0 Core Spec, 6.2.9 <em>Other Punctuation</em></a></p>
