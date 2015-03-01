% Café Chan

## Now playing (maybe)

If Café Chan is currently playing music, you can tune in here. (If you try to
play it and nothing happens after a while (~15 seconds), and you refresh the
page and try again and still nothing happens, then Café Chan is probably not
playing any music.)

<audio src="http://cafe.lumeh.org/" preload="none" controls>
  <a href="http://cafe.lumeh.org/" target="cafe-music-stream">music stream</a>
</audio>

### Current song

<p><em id="song-artist">&nbsp;</em> – <em id="song-title">&nbsp;</em>
<br>from <em id="song-album">&nbsp;</em></p>

<script src="http://code.jquery.com/jquery-2.0.3.min.js"></script>
<script>
$(document).ready(function() {
 var update = function() {
  $.ajax({
   url: "http://cafe.lumeh.org:61321/",
   cache: false,
   dataType: "json"
  }).done(function(song) {
   $("title").text(song.title + " – " + song.artist);
   $("#song-title").text(song.title);
   $("#song-artist").text(song.artist);
   $("#song-album").text(song.album);
  });
 };
 update();
 setInterval(update, 5000);
});
</script>
