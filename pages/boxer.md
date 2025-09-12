---
title: Shoot the Boxer
---

# Shoot the Boxer

(Note: Sound effects are loud. Turn down your volume first.)

<div id="boxer"></div>
<script>
  window.RufflePlayer = window.RufflePlayer || {};
  window.addEventListener("load", (event) => {
    const ruffle = window.RufflePlayer.newest();
    const player = ruffle.createPlayer();
    const container = document.getElementById("boxer");
    container.appendChild(player);
    player.ruffle().load({
      url: "/media/boxer.swf",
      autoplay: "on",
      unmuteOverlay: "hidden",
    });
    player.style.width = "720px";
    player.style.height = "210px";
  });
</script>
<script src="https://unpkg.com/@ruffle-rs/ruffle"></script>
