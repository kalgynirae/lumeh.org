---
title: Index
---

<div class=compact-headings>
<h1 class=hidden>lumeh.org</h1>

**lumeh.org** is Colin Chan’s personal website.  It is <del>currently</del>
<ins style="font-style: italic; text-decoration: none">always</ins>
under <span id=construction>construction</span>. If you find anything that seems
broken or wrong, you can
<a href="https://github.com/kalgynirae/lumeh.org/issues/new" target=_blank>file an
issue on GitHub</a> or <a href="mailto:admin@lumeh.org">email me</a>.

<style>
#construction:hover {text-decoration: underline; cursor: pointer}
</style>
<script>
function toggleConstruction() {
  const construction = document.getElementById("construction");
  if (construction.innerHTML == "construction") {
    construction.innerHTML = '<img alt="construction" src="/image/construction.gif">';
  } else {
    construction.innerHTML = "construction";
  }
}
document.getElementById("construction").addEventListener("click", toggleConstruction);
</script>

## Recent updates

<style>
.recent-updates {
  display: flex;
  gap: 0.5rem;
  > a {
    background: var(--color-bg-dark);
    border-radius: 0.5rem;
    padding: 0.5rem;

    strong {
      display: block;
      font-size: inherit;
      font-weight: 650;
      margin-bottom: 0;
    }
  }
}
</style>
<div class=recent-updates>
  <a href=/wiki/audio/stop-adjusting-my-microphone/>
    <strong>Stop adjusting my microphone!</strong>
    <span>Put Chrome and Discord in their place</span>
  </a>
  <a href=/wiki/web/fractions/>
    <strong>Fractions</strong>
    <span>Become 3⁄2 as familiar with U+2044</span>
  </a>
  <a href=/wiki/linux/colorize/>
    <strong>Colorize</strong>
    <span>On-the-fly coloring for interleaved logs</span>
  </a>
</div>

## Highlights

### Serious things

*   [hymn arrangements](/hymns/)
*   [recipes](/recipes/)
*   [<l-icon name=document right>my résumé</l-icon>](/files/Colin%20Chan%20resume%202025-07.pdf)
*   [my GitHub profile](https://github.com/kalgynirae/)
*   [my preferred Google Docs stylesheet](https://docs.google.com/document/d/1HnU8OpUeEzo_AIq4NqNBGNsGCAvGBrmvfOCYuv5SR5w/edit?usp=sharing)

### Semi-Serious things

*   [Krypto generator](/tools/krypto-generator/)
*   [stopwatch](/tools/stopwatch/)
*   [polar graph paper](/media/polar%20graph%20paper.pdf)

### Silly things

*   [Lumeh, God of Light Bulbs](/poetry/lumeh-god-of-light-bulbs/)
*   [Jabberwockus](/poetry/jabberwockus/)
*   [Poetry Yay](/poetry/poetry-yay/)

</div>
