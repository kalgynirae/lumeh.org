% The Stopwatch

Programmed by Colin <span id="programmed-hours">many</span> hours ago.

<p id="time">0:00.0</p>
<fieldset id="controls">
  <button id="start">Start</button>
  <button id="pause" disabled>Pause</button>
  <button id="reset">Reset</button>
</fieldset>
<fieldset id="options">
  <p>Start at <input id="start-minutes" size=1 value="0">:<input id="start-seconds" maxlength=2 size=2 value="00"></p>
  <p>Count
    <label><input id="direction-up" name="d" type="radio" value="up" checked>up</label>
    <label><input id="direction-down" name="d" type="radio" value="down">down</label>
  </p>
</fieldset>
