---
title: "Makeshift Type=notify Services"
---

# Makeshift Type=notify Services

A collection of techniques for running systemd-unaware programs as Type=notify services.

<aside class=important>

**Work in progress:** This article is still being written and might not make any sense in its
current state. Read at your own peril!

</aside>

## What is Type=notify?

`Type=notify` is used in the service files for programs that are *systemd-aware*.

systemd can run *any* program as a service, but some functionality is lacking when the program is
not systemd-aware. For example, a systemd-aware program will tell systemd when it is fully started,
and systemd will wait for this before considering its service *started*. Without this integration,
systemd considers the service started immediately after spawning the program. This difference can
be important if you need to delay the starting of a second service until the first is started, or if
you need to know whether the starting was successful in a script.

<aside>

To illustrate this, imagine a program *exampled* which reads a config file during startup and
immediately exits if the config isn’t valid. A minimal service file for this program might look
like this:

<figure class=fullwidth>
<figcaption><l-icon name=file>~/.config/systemd/user/exampled.service</l-icon></figcaption>
<pre><code>[Service]
<b>Type</b>=<i>exec</i>
<b>ExecStart</b>=<i><span class=placeholder>%h</span>/bin/exampled</i>
</code></pre>
</figure>

Starting the service might appear successful, but checking the service’s state immediately afterward reveals that it actually failed:

<pre><samp><span class=prompt>$</span> <kbd>systemctl --user start exampled && echo success</kbd>
success
<span class=prompt>$</span> <kbd>systemctl --user status exampled</kbd>
<span class=abridged>[…]</span>
     Active: <em class=fg-red>failed</em> (Result: exit-code) since<span class=abridged>[…]</span>
   Duration: 51ms
<span class=abridged>[…]</span>
</samp></pre>

If the service were systemd-aware and used Type=notify, `systemctl` could report the failure immediately:

<pre><samp><span class=prompt>$</span> <kbd>systemctl --user start exampled && echo success</kbd>
Job for exampled.service failed because the control process exited with error code.
<span class=abridged>[…]</span>
</samp></pre>

</aside>

If you try to set `Type=notify` in the service file for a program that is not systemd-aware, systemd will wait for the service’s `TimeoutStartSec=` before giving up and declaring the service failed.

<figure class=fullwidth>
<figcaption><l-icon name=file-partial>~/.config/systemd/user/waybar.service</l-icon> <span class=excerpt>(excerpt)</span></figcaption>
<pre><code>[Service]
<b>Type</b>=<i>notify</i>
<b>NotifyAccess</b>=<i>all</i>
<span class=abridged>[…]</span>
</code></pre>
</figure>

<figure class=fullwidth>
<figcaption><l-icon name=file-partial>~/.config/systemd/user/waybar.service</l-icon> <span class=excerpt>(excerpt)</span></figcaption>
<pre><code>[Service]
<span class=abridged>[…]</span>
<b>Restart</b>=<i>on-failure</i>
<b>TimeoutStartSec</b>=<i>5s</i>
</code></pre>
</figure>
