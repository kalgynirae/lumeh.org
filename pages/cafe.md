---
title: Café Chan
---

## Now playing

If Café Chan is currently playing music, you can tune in here. Note that using
the browser's built-in audio player is frequently unreliable (especially on
smartphones). It's more reliable to listen via an external audio player that can
open HTTP streams (for example, [VLC] or [mpv]). Open this URL:
`https://radio.lumeh.org/cafe.ogg`.

<audio src="https://radio.lumeh.org/cafe.ogg" preload="none" controls>
  <a href="https://radio.lumeh.org/cafe.ogg" target="cafe-music-stream">café stream</a>
</audio>

[VLC]: https://www.videolan.org/vlc/
[mpv]: https://mpv.io/

<p><em id="song-artist">&nbsp;</em> – <em id="song-title">&nbsp;</em>
(<span id="song-current-time">&nbsp;</span>/<span id="song-length">&nbsp;</span>)
<br>from <em id="song-album">&nbsp;</em></p>
<p>Up next: <em id="next-title">&nbsp;</em></p>

<script src="/js/jquery-2.1.4.min.js"></script>
<script>
$(document).ready(function() {
 var update = function() {
  $.ajax({
   url: "https://radio.lumeh.org:61321/",
   cache: false,
   dataType: "json"
  }).done(function(data) {
   $("title").text(data.title + " – " + data.artist);
   $("#song-title").text(data.title);
   $("#song-artist").text(data.artist);
   $("#song-album").text(data.album);
   $("#song-current-time").fadeTo(200, 0, function() {
    $("#song-current-time").text(data.current_time).fadeTo(150, 1);
   });
   $("#song-length").text(data.length);
   $("#next-title").text(data.next_title);
  });
 };
 update();
 setInterval(update, 8000);
});
</script>
