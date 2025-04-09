---
title: The Stopwatch
---

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

<style>
#time {
  text-align: center;
}
#time {
  color: #000000;
  font-family: "Inter";
  font-feature-settings: "tnum";
  font-size: 12em;
  font-weight: bold;
  line-height: 1em;
}
#controls, #options {
  align-items: baseline;
  display: flex;
  justify-content: center;
}
#controls button {
  font-size: 1.5em;
  font-weight: bold;
  line-height: 2em;
  width: 5em;
}
#controls button:disabled {
  color: inherit;
}
#start {
  color: #35710b;
}
#reset {
  color: #75237d;
}
#options p {
  margin: 0.5rem;
}
#options input[type=radio] {
  margin-left: .5em;
}
</style>

<script>
(function () {
  var direction = 'up';
  var initialTime = 0;
  var startTime = 0;
  var pauseTime = 0;
  var timer;

  function toggleState(state) {
    switch (state) {
      case 'paused': {
        document.getElementById('start').disabled = false;
        document.getElementById('start').className = '';
        document.getElementById('pause').disabled = true;
        document.getElementById('pause').className = 'disabled';
        document.getElementById('start-minutes').disabled = false;
        document.getElementById('start-seconds').disabled = false;
        document.getElementById('direction-up').disabled = false;
        document.getElementById('direction-down').disabled = false;
        break;
      }
      case 'running': {
        document.getElementById('start').disabled = true;
        document.getElementById('start').className = 'disabled';
        document.getElementById('pause').disabled = false;
        document.getElementById('pause').className = '';
        document.getElementById('start-minutes').disabled = true;
        document.getElementById('start-seconds').disabled = true;
        document.getElementById('direction-up').disabled = true;
        document.getElementById('direction-down').disabled = true;
        break;
      }
    }
  }

  function stopwatchUpdate(time) {
    // Assuming time is in milliseconds,
    const hours   = Math.floor(time / 1000 / 60 / 60);
    const minutes = Math.floor(time / 1000 / 60 - (hours * 60));
    const seconds = Math.floor(time / 1000 - (hours * 60 * 60) - (minutes * 60));
    const tenths  = Math.floor(time / 100 - (hours * 60 * 60 * 10) - (minutes * 60 * 10) - (seconds * 10));

    const html = ((hours > 0) ? hours + 'h<br />' : '') + minutes + ':' + ((seconds < 10) ? '0' : '') + seconds + '.' + tenths;
    document.getElementById('time').innerHTML = html;
  }

  function stopwatchStart() {
    startTime = Date.now();
    stopwatchCheck();
    toggleState('running');
  }

  function stopwatchCheck() {
    timer = window.requestAnimationFrame(stopwatchCheck);
    switch (direction) {
      case 'up': {
        const time = Date.now() - startTime + initialTime + pauseTime;
        stopwatchUpdate(time);
        break;
      }
      case 'down': {
        const time = Math.max(0, initialTime - (Date.now() - startTime + pauseTime));
        stopwatchUpdate(time);
        if (time == 0) {
          alert("Time's up!");
          stopwatchReset();
        }
        break;
      }
    }
  }

  function stopwatchPause() {
    pauseTime = (Date.now() - startTime) + pauseTime;
    window.cancelAnimationFrame(timer);
    toggleState('paused');
  }

  function stopwatchReset() {
    stopwatchPause();
    startTime = 0;
    pauseTime = 0;
    direction = document.getElementById('direction-up').checked ? 'up' : 'down';
    const startMinutes = +document.getElementById('start-minutes').value || 0;
    const startSeconds = +document.getElementById('start-seconds').value || 0;
    initialTime = (startMinutes * 60 + startSeconds) * 1000;
    stopwatchUpdate(initialTime);
  }

  function stopwatchInitialize() {
    stopwatchReset();
    document.getElementById('start').addEventListener('click', stopwatchStart);
    document.getElementById('pause').addEventListener('click', stopwatchPause);
    document.getElementById('reset').addEventListener('click', stopwatchReset);
    document.getElementById('start-minutes').addEventListener('input', stopwatchReset);
    document.getElementById('start-seconds').addEventListener('input', stopwatchReset);
    document.getElementById('direction-up').addEventListener('change', stopwatchReset);
    document.getElementById('direction-down').addEventListener('change', stopwatchReset);
  };

  function updateHours() {
    const programmedDate = 1213655000000;
    const timeSince = Math.round((Date.now() - programmedDate) / 3600000);
    document.getElementById('programmed-hours').innerHTML = timeSince;
  }

  document.addEventListener('DOMContentLoaded', stopwatchInitialize);
  document.addEventListener('DOMContentLoaded', updateHours);
})();
</script>
