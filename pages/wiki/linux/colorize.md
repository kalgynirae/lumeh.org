---
title: Colorize
show_authors: true
---

# Colorize

**Colorize** is a Python program that makes it easier to understand interleaved
log lines by coloring each line based on a matching part.

Source: <a href=https://github.com/kalgynirae/dotfiles/blob/main/bin/colorize rel=external target=_blank>kalgynirae/dotfiles:bin/colorize</a>

Example:

<pre><samp><span class=comment># Color some logs from systemd based on service name</span>
<span class=prompt>$</span> <kbd>journalctl _COMM=systemd --since -20m | grep '\.service' | colorize '\S+\.service'</kbd>
<span class=fg-green>Jun 07 14:36:03 iroh systemd[1]: Starting NetworkManager-dispatcher.service - Network Manager Script Dispatcher Service...</span>
<span class=fg-green>Jun 07 14:36:03 iroh systemd[1]: Started NetworkManager-dispatcher.service - Network Manager Script Dispatcher Service.</span>
<span class=fg-green>Jun 07 14:36:13 iroh systemd[1]: NetworkManager-dispatcher.service: Deactivated successfully.</span>
<span class=fg-blue>Jun 07 14:37:59 iroh systemd[1]: Starting packagekit.service - PackageKit Daemon...</span>
<span class=fg-blue>Jun 07 14:37:59 iroh systemd[1]: Started packagekit.service - PackageKit Daemon.</span>
<span class=fg-yellow>Jun 07 14:37:59 iroh systemd[1]: Starting flatpak-system-helper.service - flatpak system helper...</span>
<span class=fg-yellow>Jun 07 14:37:59 iroh systemd[1]: Started flatpak-system-helper.service - flatpak system helper.</span>
<span class=fg-blue>Jun 07 14:43:09 iroh systemd[1]: packagekit.service: Deactivated successfully.</span>
<span class=fg-blue>Jun 07 14:43:09 iroh systemd[1]: packagekit.service: Consumed 1.177s CPU time, 120.1M memory peak.</span>
<span class=fg-yellow>Jun 07 14:47:59 iroh systemd[1]: flatpak-system-helper.service: Deactivated successfully.</span>
<span class=fg-red>Jun 07 14:51:10 iroh systemd[1]: Starting fprintd.service - Fingerprint Authentication Daemon...</span>
<span class=fg-red>Jun 07 14:51:10 iroh systemd[1]: Started fprintd.service - Fingerprint Authentication Daemon.</span>
<span class=fg-red>Jun 07 14:51:40 iroh systemd[1]: fprintd.service: Deactivated successfully.</span>
</samp></pre>

Usage:
<pre><samp><span class=prompt>$</span> <kbd>colorize --help</kbd>
usage: colorize [-h] [--cycle] [--once] [--no-true-color] [PATTERN]

Color each output line based on the part of the line that matches PATTERN.

If PATTERN contains one or more capturing groups, only the final capturing
group will be used as the matching part of the line. Otherwise, the entire
match will be used.

positional arguments:
  PATTERN          what to match (default: ^[\w.-/]+)

options:
  -h, --help       show this help message and exit
  --cycle          shift color when key changes instead of assigning colors to keys
  --once           assign each color once; then stop coloring
  --no-true-color  use the terminal's color palette instead of true color
</samp></pre>
