---
title: Index
---

**lumeh.org** is Colin Chan’s personal website.  It is ~~currently~~ *always*
under <span id=construction>construction</span>. If you find anything that seems
broken or wrong, you can file an issue on GitHub or email the admin (see info
about both in the footer).

<style>
#construction:hover {text-decoration: underline}
</style>
<script>
function increaseConstruction() {
  const construction = document.getElementById("construction");
  construction.innerHTML = '<img alt="construction" src="/image/construction.gif">';
  construction.removeEventListener("click", increaseConstruction);
}
document.getElementById("construction").addEventListener("click", increaseConstruction);
</script>

## Highlights

### Serious things

*   [music I’ve written](/music/)
*   [my GitHub profile](https://github.com/kalgynirae/)
*   [my preferred Google Docs styles](https://docs.google.com/document/d/1HnU8OpUeEzo_AIq4NqNBGNsGCAvGBrmvfOCYuv5SR5w/edit?usp=sharing)
*   [my recipes](/recipes/)
*   [my résumé (PDF)](/docs/resume-20241215.pdf)

### Semi-Serious things

*   [NarChanSo Ball](/wiki/games/narchanso-ball/)
*   [Krypto generator](/tools/krypto-generator/)
*   [stopwatch](/tools/stopwatch/)
*   [polar graph paper](/media/polar%20graph%20paper.pdf)

### Silly things

*   [Lumeh, God of Light Bulbs](/poetry/lumeh-god-of-light-bulbs/)
*   [Jabberwockus](/poetry/jabberwockus/)
*   [Poetry Yay](/poetry/poetry-yay/)
