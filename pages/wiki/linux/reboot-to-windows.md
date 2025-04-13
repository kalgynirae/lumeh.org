---
title: Reboot to Windows
---

# Reboot to Windows

My PC dual-boots Windows and Linux, but I use Linux ~95% of the time. Since I like my PC to boot as
quickly as possible, I’ve settled on the following setup:

* The PC boots directly into Linux. There is no interactive boot menu.
* I’ve added *Reboot to Windows* options to my login manager and desktop environment.
* The PC reboots to Windows automatically after two minutes if I haven’t logged in.

If you’re curious how any of this works, read on!

## Prerequisites

Before I dive into the details, please note that these solutions require that your machine:

1. boots using [UEFI],
2. has separate EFI boot entries for Linux and Windows,
3. doesn’t use a fancy boot menu that remembers your previous selection.

[UEFI]: https://wiki.archlinux.org/title/Unified_Extensible_Firmware_Interface

The first two criteria are easy to verify from Linux: run `efibootmgr`, and check that there are
entries for both Linux and Windows.

<pre><samp><span class=prompt>$</span> <kbd>efibootmgr</kbd>
BootCurrent: 0000
Timeout: 0 seconds
BootOrder: 0000,0002,0001,0003,0004,0005,0006
Boot0000* Arch Linux	HD(2,GPT,47be9262-66d7-7743-be45-99e62de<span class=abridged>[…]</span>
Boot0001* UEFI OS	HD(1,GPT,dd9ddf9f-afcd-4776-9d72-db7cc81<span class=abridged>[…]</span>
Boot0002* Windows Boot Manager	HD(2,GPT,7dd2e191-7af4-4540-a427<span class=abridged>[…]</span>
<span class=abridged>[…]</span>
</samp></pre>

You can see that, for my machine, `0000` is Linux and `0002` is Windows, and `0000` is the one that
will be booted first.

The third criterion is important because these solutions assume that the machine will boot directly
into Linux by default. If your Linux installation came with an interactive boot menu (such as
[GRUB]), you can likely reconfigure that boot menu to automatically default to Linux.

[GRUB]: https://wiki.archlinux.org/title/GRUB

## BootNext

UEFI supports overriding the boot order for the next boot only by setting the `BootNext` EFI
variable. For example, if I want my machine to boot into Windows next, I can run:

<pre><samp><span class=prompt>$</span> <kbd>sudo efibootmgr --bootnext 0002</kbd>
BootNext: 0002
BootCurrent: 0000
<span class=abridged>[…remaining output same as before]</span>
</samp></pre>

## reboot-to-windows script

In the above sections, we saw that my machine’s boot ID for Windows is `0002`. I didn’t want to
hard-code this ID (since it could change if I re-install in the future), so I wrote a script to find
it and reboot the machine.

<figure class=fullwidth>
<figcaption><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-fill" viewBox="0 0 16 16">
  <path d="M4 0h5.293A1 1 0 0 1 10 .293L13.707 4a1 1 0 0 1 .293.707V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2m5.5 1.5v2a1 1 0 0 0 1 1h2z"/>
</svg>/home/colin/bin/reboot-to-windows</figcaption>
<pre><code><span class=shebang>#!/bin/bash</span>
<br>if output=$(<span class=command>efibootmgr | grep Windows</span>) && [[ $output =~ Boot([[:xdigit:]]{4}) ]]; then
  windows_id=${BASH_REMATCH[1]}
else
  echo &gt;&2 "No EFI boot entry found matching 'Windows'"
  exit 1
fi
<br>if ! <span class=command>sudo efibootmgr --bootnext "$windows_id"</span>; then
  echo &gt;&2 "Failed to set next boot; aborting"
  exit 1
fi
<br><span class=command>systemctl --quiet --no-block reboot</span>
</code></pre>
</figure>

### sudo configuration

`efibootmgr` needs elevated privileges to modify EFI variables. To avoid being prompted
for a password, I added the following to <span class=path>/etc/sudoers</span>.

<figure class=fullwidth>
<figcaption><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-minus-fill" viewBox="0 0 16 16">
  <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1M6 8.5h4a.5.5 0 0 1 0 1H6a.5.5 0 0 1 0-1"/>
</svg>/etc/sudoers <span class=excerpt>(excerpt)</span></figcaption>
<pre><code>%wheel ALL=(ALL:ALL) NOPASSWD: /usr/bin/efibootmgr ^--bootnext [[:xdigit:]]+$
</code></pre>
</figure>

This allows any member of the [*wheel* group] to run this specific command without providing a
password. In case you’re not familiar with configuring sudo, note that you should always [use the `visudo` command] to do so.

[*wheel* group]: https://en.wikipedia.org/wiki/Wheel_(computing)#Wheel_group
[use the `visudo` command]: https://wiki.archlinux.org/title/Sudo#Using_visudo

## Login manager configuration

I use [greetd] as my login manager, but this should work for any login manager that supports Wayland sessions.

[greetd]: https://wiki.archlinux.org/title/Greetd

<figure class=fullwidth>
<figcaption><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-fill" viewBox="0 0 16 16">
  <path d="M4 0h5.293A1 1 0 0 1 10 .293L13.707 4a1 1 0 0 1 .293.707V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2m5.5 1.5v2a1 1 0 0 0 1 1h2z"/>
</svg>/usr/share/wayland-sessions/reboot-to-windows.desktop</figcaption>
<pre><code>[Desktop Entry]
Name=Reboot to Windows
Exec=/home/colin/bin/reboot-to-windows
Type=Application
</code></pre>
</figure>

## Automatic reboot to Windows

I achieve this with a systemd service and timer.

<figure class=fullwidth>
<figcaption><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-fill" viewBox="0 0 16 16">
  <path d="M4 0h5.293A1 1 0 0 1 10 .293L13.707 4a1 1 0 0 1 .293.707V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2m5.5 1.5v2a1 1 0 0 0 1 1h2z"/>
</svg>/etc/systemd/system/reboot-to-windows.service</figcaption>
<pre><code>[Service]
Type=oneshot
ExecCondition=bash -c "! loginctl list-sessions --json=short | jq -e '.[]|select(.seat != null && .user != \"greeter\")'"
ExecStart=/home/colin/bin/reboot-to-windows
</code></pre>
</figure>

The interesting part of this service is the `ExecCondition`, which uses [jq] to parse the JSON from
`loginctl` and look for any active sessions for users other than *greeter* (the user that my login
manager runs as). The `-e` flag makes jq’s exit code reflect whether a session was found, and the
`!` at the start of the pipeline negates the result so that the condition fails if any session was
found (meaning the reboot should not proceed).

[jq]: https://jqlang.org/

The corresponding timer triggers this service to start two minutes after the machine boots. 

<figure class=fullwidth>
<figcaption><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-fill" viewBox="0 0 16 16">
  <path d="M4 0h5.293A1 1 0 0 1 10 .293L13.707 4a1 1 0 0 1 .293.707V14a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2a2 2 0 0 1 2-2m5.5 1.5v2a1 1 0 0 0 1 1h2z"/>
</svg>/etc/systemd/system/reboot-to-windows.timer</figcaption>
<pre><code>[Timer]
OnActiveSec=2m
<br>[Install]
WantedBy=multi-user.target
</code></pre>
</figure>

Remember to enable the timer with `systemctl enable reboot-to-windows.timer`.
