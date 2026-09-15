---
title: Index
---

<h1 class=hidden>lumeh.org</h1>

**lumeh.org** is Colin Chan’s personal website. Can I interest you in some…
<button id=dice-button>
  <l-icon id=dice-1 name=dice-1 right></l-icon>
  <l-icon id=dice-2 name=dice-2 right></l-icon>
  <l-icon id=dice-3 name=dice-3 right></l-icon>
  <l-icon id=dice-4 name=dice-4 right></l-icon>
  <l-icon id=dice-5 name=dice-5 right></l-icon>
  <l-icon id=dice-6 name=dice-6 right></l-icon>
  <l-icon id=dice-1-fill name=dice-1-fill right></l-icon>
  <l-icon id=dice-2-fill name=dice-2-fill right></l-icon>
  <l-icon id=dice-3-fill name=dice-3-fill right></l-icon>
  <l-icon id=dice-4-fill name=dice-4-fill right></l-icon>
  <l-icon id=dice-5-fill name=dice-5-fill right></l-icon>
  <l-icon id=dice-6-fill name=dice-6-fill right></l-icon>
</button>
<a id=randomized-link href=/recipes/>tasty recipes</a>?

<style>
#dice-button {
  border: none;
  background: none;
  padding: 0;

  cursor: pointer;

  &:hover {
    color: var(--color-green);
  }

  l-icon {
    display: none;
  }

  #dice-1 {
    display: inline-block;
  }
}

#randomized-link {
  display: inline-block;
  transition: transform 0.1s ease-out;
  transform-origin: center center;
}
</style>

<script>
const diceButton = document.querySelector("#dice-button");
const diceLink = document.querySelector("#randomized-link");
const diceIcons = [
  document.querySelector("#dice-1"),
  document.querySelector("#dice-2"),
  document.querySelector("#dice-3"),
  document.querySelector("#dice-4"),
  document.querySelector("#dice-5"),
  document.querySelector("#dice-6"),
  document.querySelector("#dice-1-fill"),
  document.querySelector("#dice-2-fill"),
  document.querySelector("#dice-3-fill"),
  document.querySelector("#dice-4-fill"),
  document.querySelector("#dice-5-fill"),
  document.querySelector("#dice-6-fill"),
];
const diceLinks = [
  {href: "/recipes/", text: "tasty recipes"},
  {href: "/projects/", text: "software projects"},
  {href: "/hymns/", text: "hymn arrangements"},
  {href: "/tools/", text: "useful tools"},
  {href: "/wiki/", text: "intriguing information"},
  {href: "/music/", text: "groovy music"},
];
const diceNext = {0: 2, 2: 3, 3: 5, 5: 1, 1: 4, 4: 0};
let diceCurrentLink = 0;
let diceCurrentlyRolling = false;
let diceCurrentIndex = 0;
function swapDice(newIndex) {
  diceIcons[diceCurrentIndex].style.display = "none";
  diceCurrentIndex = newIndex;
  diceIcons[diceCurrentIndex].style.display = "inline-block";
}
async function diceRoll() {
  let nextNumber = null;
  for (let i = 0; i < 15; i++) {
    const currentNumber = diceCurrentIndex % 6;
    nextNumber = currentNumber;
    while (nextNumber == currentNumber) {
      nextNumber = Math.floor(Math.random() * 6);
    }
    swapDice(nextNumber + 6);
    await new Promise(r => setTimeout(r, 100));
  }
  swapDice(diceNext[diceCurrentLink] + 6);
  await new Promise(r => setTimeout(r, 500));
  swapDice(diceNext[diceCurrentLink]);
}
async function shuffleLinks() {
  if (diceCurrentlyRolling) return;
  diceCurrentlyRolling = true;
  diceLink.style.transform = "scaleY(0%)";
  await diceRoll();
  diceCurrentLink = diceCurrentIndex % 6;
  const link = diceLinks[diceCurrentLink];
  diceLink.href = link.href;
  diceLink.textContent = link.text;
  diceLink.style.transform = "none";
  diceCurrentlyRolling = false;
}
diceButton.addEventListener("click", shuffleLinks);
</script>

## Recent updates

<div class=recent-updates>

<p><time datetime=2026-09-13>2026-09-13</time></p>

* [Recent updates](/#recent-updates) was completely redesigned.
  [Let me know](https://airtable.com/appopNVjvtXgt5gQQ/pagZqMmjT3MfIjFi3/form) what you think!
* [Hymns](/hymns/) was completely redesigned. The hymns can now be sorted and filtered.

<p><time datetime=2026-09-08>2026-09-08</time></p>

* Underline offset and thickness were adjusted. Underlines now have a more consistent appearance across browsers.

<p><time datetime=2026-09-06>2026-09-06</time></p>

* Underlines were added to most links so they are no longer distinguished by color alone.
* [Poetry](/poetry/) was moved to the navigation bar.

<p><time datetime=2026-08-23>2026-08-23</time></p>

* [lumeh.org](/projects/lumeh.org/) was given a [new section](https://www.lumeh.org/projects/lumeh.org/#no-llms) clarifying that all parts of the site were created without assistance from LLMs.

</div>

## Miscellaneous

Most of this website’s content can be reached via the navigation bar above. The things below
are here either for ease of access or because they don’t have a proper home yet.

*   [<l-icon name=document right>my résumé</l-icon>](/files/Colin%20Chan%20resume%202025-07.pdf)
*   [my GitHub profile](https://github.com/kalgynirae/)
*   [my preferred Google Docs stylesheet](https://docs.google.com/document/d/1HnU8OpUeEzo_AIq4NqNBGNsGCAvGBrmvfOCYuv5SR5w/edit?usp=sharing)
*   [polar graph paper](/media/polar%20graph%20paper.pdf)
