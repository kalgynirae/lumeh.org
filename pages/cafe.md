---
title: Café Chan
---

## Now playing

If Café Chan is currently playing music, you can tune in here. Note that using
the browser's built-in audio player is frequently unreliable (especially on
smartphones). It's more reliable to listen via an external audio player that can
open HTTP streams (for example, [VLC] or [mpv]). Open this URL:
<code>https://radio.lumeh.org/christmas<em style="color: green; font-weight: bold">#</em>.ogg</code> (where <em style="color: green; font-weight: bold">#</em> is 1–4 corresponding with the streams below).

**Christmas Orchestral**

<audio src="https://radio.lumeh.org/christmas1.ogg" preload="none" controls>
  <a href="https://radio.lumeh.org/christmas1.ogg" target="cafe-music-stream">christmas1 stream</a>
</audio>

**Christmas New Age**

<audio src="https://radio.lumeh.org/christmas2.ogg" preload="none" controls>
  <a href="https://radio.lumeh.org/christmas2.ogg" target="cafe-music-stream">christmas2 stream</a>
</audio>

**Christmas Country**

<audio src="https://radio.lumeh.org/christmas3.ogg" preload="none" controls>
  <a href="https://radio.lumeh.org/christmas3.ogg" target="cafe-music-stream">christmas3 stream</a>
</audio>

**Christmas Sing-Along**

<audio src="https://radio.lumeh.org/christmas4.ogg" preload="none" controls>
  <a href="https://radio.lumeh.org/christmas4.ogg" target="cafe-music-stream">christmas4 stream</a>
</audio>

[VLC]: https://www.videolan.org/vlc/
[mpv]: https://mpv.io/

<!--
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
-->
