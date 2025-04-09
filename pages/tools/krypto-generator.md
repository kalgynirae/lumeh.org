---
title: Krypto Generator
---

Programmed by Colin <span id="hours">many</span> hours ago.

<table id="krypto-table">
  <tr id="goal">
   <td colspan="5">&nbsp;</td>
  </tr>
  <tr id="numbers">
   <td>&nbsp;</td>
   <td>&nbsp;</td>
   <td>&nbsp;</td>
   <td>&nbsp;</td>
   <td>&nbsp;</td>
  </tr>
</table>
<button id="krypto-button" onclick="generateKryptoNumbers()">Generate</button>

<style type="text/css">
#krypto-table {
    background-color: #efefef;
    font-family: "Crimson Pro", "Georgia", serif;
    font-size: 3.5em;
    font-weight: bold;
    margin-bottom: 0.5em;
    width: 100%;
}
#krypto-table td {
    border: solid 1px #cccccc;
    padding: 0.25em 0;
    text-align: center;
}
#numbers td {
    width: 20%;
}
#krypto-button {
    font-size: 2em;
    font-weight: bold;
    padding: 1em;
    width: 100%;
}
</style>

<script type="text/javascript">
(function () {
  var cards;

  function updateHours() {
    var programmedDate = 1275489000000;
    var timeSince = Math.round((Date.now() - programmedDate) / 3600000);
    document.getElementById('hours').innerHTML = timeSince;
  }
  document.addEventListener('DOMContentLoaded', updateHours);

  function drawCard() {
    var rand = Math.floor(Math.random() * cards.length);
    var card = cards[rand];
    cards = cards.slice(0, rand).concat(cards.slice(rand + 1));
    return card;
  }

  function generateKryptoNumbers() {
    cards = [
      1,1,1,2,2,2,3,3,3,4,4,4,5,5,5,6,6,6,7,7,7,8,8,8,9,9,9,10,10,10,
      11,11,12,12,13,13,14,14,15,15,16,16,17,17,18,19,20,21,22,23,24,25,
    ];
    var numbers = [];
    for (var i = 0; i < 5; i++) {
      document.getElementById('numbers').cells[i].innerHTML = drawCard();
    }
    document.getElementById('goal').cells[0].innerHTML = drawCard();
  }
  window.generateKryptoNumbers = generateKryptoNumbers;
})();
</script>
