#!/usr/bin/python
# coding=UTF-8

from random import choice

first = ['Ya', 'At', 'Ma', 'Ta', 'Ko', 'Yo', 'No', 'Ma', 'Mo', 'Shi', 'Yu', 'Aki', 'To', 'Ka', 'Yu', 'Hi', 'Fu', 'Jyu', 'So', 'Shu', 'Sho', 'Ichi', 'Ichu', 'Ryou', 'Ru', 'Ryo', 'A', 'O']
other = ['zu', 'tchu', 'ki', 'shi', 'ka', 'ro', 'hei', 'su', 'ge', 'ri', 'to', 'ji', 'yo', 'ho', 'ndo', 'ra', 'na', 'ya', 'sa', 'ru', 'mo', 'buo', 'tsu', 'ma', 'bi']
single = ['Ryu', 'Yo', 'Bo', 'Yu']

def generate(fsyl,lsyl):
    f = choice(first)
    for i in range(1,fsyl):
        f += choice(other)
    
    l = choice(first)
    for i in range(1,lsyl):
        l += choice(other)
    
    return f + ' ' + l

syllables = [[1,2],[1,3],[2,2],[2,3],[2,3],[2,4],[3,2],[3,3],[3,3],[3,4],[4,3],[4,4],[4,5]]
names = [generate(s[0],s[1]) for s in syllables]

print 'Content-type: text/html; charset=UTF-8'
print
print """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <title>Japanese name generator | lumeh.org</title>
  <link rel="stylesheet" type="text/css" href="./style.css" />
</head>
<body>
  <div id="header">
    <img alt="lumeh.org" src="./img/lumpybox.png" width="48" height="48" />
    <h1 id="title">Japanese name generator</h1>
    <ul id="menu">
      <li> </li>
    </ul>
  </div>
  <div id="body">
    <h2>Background information</h2>
    <p>I programmed this a while ago in Java and then lost it for a while. Recently, I rediscovered it among some old backed-up website stuff and converted it to Python.</p>
    <h2>How it works</h2>
    <p>The program is pretty simple: specify the number of syllables you want, and the program picks random syllables from a list and sticks them together. For ease of use, I have ordered the program to generate several names of different lengths so you can see several at the same time.</p>
    <h2>How to use it</h2>
    <p>You should see a list of about 10 names below. The names at the top are shorter than the names at the bottom. Reload the page to see a new selection.</p>
    <ul>"""

for n in names:
    print '      <li>%s</li>' % n

print """    </ul>
  </div>
  <div id="footer">
    <span id="contact">
      Contact: <img class="inline-text" alt="" src="./img/admin_email.png" width="106" height="11" />
    </span>
  </div>
</body>
</html>"""
