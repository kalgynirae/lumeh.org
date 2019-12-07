% Café Chan

## Now playing (maybe)

If Café Chan is currently playing music, you can tune in here. (If you try to
play it and nothing happens after a while (~15 seconds), and you refresh the
page and try again and still nothing happens, then Café Chan is probably not
playing any music.)

<audio src="https://radio.lumeh.org/café.ogg" preload="none" controls>
  <a href="https://radio.lumeh.org/café.ogg" target="cafe-music-stream">music stream</a>
</audio>

<p><em id="song-artist">&nbsp;</em> – <em id="song-title">&nbsp;</em>
(<span id="song-current-time">&nbsp;</span>/<span id="song-length">&nbsp;</span>)
<br>from <em id="song-album">&nbsp;</em></p>
<p>Up next: <em id="next-title">&nbsp;</em></p>

<script src="/js/jquery-2.1.4.min.js"></script>
<script>
$(document).ready(function() {
 var update = function() {
  $.ajax({
   url: "https://cafe.lumeh.org:61321/",
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
 setInterval(update, 5000);
});
</script>
