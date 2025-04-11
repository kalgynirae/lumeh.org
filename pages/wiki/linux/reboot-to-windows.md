---
title: Reboot to Windows
---

My PC dual-boots Windows and Linux, but I use Linux ~95% of the time. Since I like my PC to boot as quickly as possible, I’ve settled on the following setup:

* The PC always boots into Linux first. There is no boot selection screen.
* In Linux, I’ve added a *Reboot to Windows* option to both my login manager and my
  desktop environment.
* To allow Windows’s *Update and shut down* process to work unattended, I’ve set up a systemd timer
  to reboot into Windows if nobody has logged into the machine after 90 seconds.

This page documents the details of my setup.

## EFI boot entries

The main prerequisite is a system that boots using [UEFI] with boot entries for both Linux and Windows. For this setup to be effective, the Linux boot entry should always boot into Linux. If it instead shows a fancy boot menu (such as [GRUB]) that remembers your previous selection, that won’t play well. (You can likely configure your boot menu to select Linux automatically, but that’s out of the scope of this page.)

[UEFI]: https://wiki.archlinux.org/title/Unified_Extensible_Firmware_Interface
[GRUB]: https://wiki.archlinux.org/title/GRUB

`efibootmgr` lists the existing boot entries:
```
$ efibootmgr
BootCurrent: 0000
Timeout: 0 seconds
BootOrder: 0000,0002,0001,0003,0004,0005,0006
Boot0000* Arch Linux	HD(2,GPT,47be9262-66d7-7743-be45-99e62dee1724,0x76c00800,0x100000)/\vmlinuz-linux69006e0069007400720064003d005c0069006e0069007400720061006d00660073002d006c0069006e00750078002e0069006d006700200072006f006f0074003d004c004100420045004c003d00610072006300680072006f006f0074002000720077002000610075006400690074003d003000
Boot0001* UEFI OS	HD(1,GPT,dd9ddf9f-afcd-4776-9d72-db7cc812b6d2,0x800,0xa00000)/\EFI\BOOT\BOOTX64.EFI0000424f
Boot0002* Windows Boot Manager	HD(2,GPT,7dd2e191-7af4-4540-a427-32f1d99adb12,0xa00800,0x32000)/\EFI\MICROSOFT\BOOT\BOOTMGFW.EFI57494e444f5753000100000088000000780000004200430044004f0042004a004500430054003d007b00390064006500610038003600320063002d0035006300640064002d0034006500370030002d0061006300630031002d006600330032006200330034003400640034003700390035007d0000004d000100000010000000040000007fff0400
Boot0003* UEFI: ScarlettWelcome Disk, Partition 1	PciRoot(0x0)/Pci(0x1,0x2)/Pci(0x0,0x0)/Pci(0x8,0x0)/Pci(0x0,0x1)/USB(2,0)/USB(1,4)/HD(1,MBR,0x2d82c634,0x3f,0x141)0000424f
Boot0004* UEFI:CD/DVD Drive	BBS(129,,0x0)
Boot0005* UEFI:Removable Device	BBS(130,,0x0)
Boot0006* UEFI:Network Device	BBS(131,,0x0)
```

You can see that, for my machine, `0000` is Linux and `0002` is Windows, and `0000` is the one that will be booted first.

### BootNext

UEFI supports overriding the boot order for the next boot only. For my machine, to boot into Windows next, I would run:
```
$ sudo efibootmgr --bootnext 0002
```

## reboot-to-windows script

I didn’t want to hard-code my machine’s boot ID for Windows (which could change if I re-install in the future), so I wrote a script to find it.

<span class=path>/home/colin/bin/reboot-to-windows</span>
```bash
#!/bin/bash

set-next-boot() {
  local output
  if output=$(efibootmgr | grep "$1") && [[ $output =~ Boot([[:xdigit:]]{4}) ]]; then
    sudo efibootmgr --bootnext "${BASH_REMATCH[1]}"
  else
    echo >&2 "No EFI boot entry found matching ${1@Q}"
    return 1
  fi
}

if ! set-next-boot Windows; then
  echo >&2 "Failed to set next boot; aborting"
  exit 1
fi

systemctl --quiet --no-block reboot
```

The script first defines `set-next-boot()`, which searches the boot entries for a given string and, if
one is found, runs `efibootmgr` to set the next boot. Then, the script calls
that function with the hard-coded string *Windows* and initiates a reboot.

### sudo configuration

`efibootmgr` needs elevated privileges to modify EFI variables. To avoid being prompted
for a password, I added the following to <span class=path>/etc/sudoers</span>.

```sudoers
%wheel ALL=(ALL:ALL) NOPASSWD: /usr/bin/efibootmgr --bootnext ^[[\:xdigit\:]]+$
```

This allows any member of the [*wheel* group] to run this specific command without providing a
password. In case you’re not familiar with configuring sudo, note that you should always [use the `visudo` command] to do so.

[*wheel* group]: https://en.wikipedia.org/wiki/Wheel_(computing)#Wheel_group
[use the `visudo` command]: https://wiki.archlinux.org/title/Sudo#Using_visudo

## greetd configuration

(TODO)

## Automatic reboot after a delay

(TODO)

<span class=path>/etc/systemd/system/reboot-to-windows.service</span>
```systemd
[Service]
Type=oneshot
ExecCondition=bash -c "! loginctl list-sessions --json=short | jq -e '.[]|select(.seat != null and .user != \"greeter\")'"
ExecStart=/home/colin/bin/reboot-to-windows
```

The interesting part of this service is the condition:
```bash
! loginctl list-sessions --json=short \
  | jq -e '.[] | select( .seat != null and .user != "greeter" )'
```
The human-readable output of `loginctl list-sessions`:
```
$ loginctl list-sessions
SESSION  UID USER  SEAT  LEADER CLASS   TTY  IDLE SINCE
      1 1000 colin -     809    manager -    no   -
      4 1000 colin seat0 1110   user    tty1 no   -
```
Then I’m selecting only sessions for which `seat` is populated and `user` is not *greeter*.

<span class=path>/etc/systemd/system/reboot-to-windows.timer</span>
```systemd
[Timer]
OnActiveSec=90s

[Install]
WantedBy=multi-user.target
```
