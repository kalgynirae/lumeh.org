---
title: PulseAudio
---

PulseAudio is the sound system used by most desktop Linux distributions. It’s
mostly straightforward, but there are a few helpful things that are worth
documenting here.

# Important Concepts

* There are two types of devices:

  * **sink**: a device that an application can send audio to (e.g., a set of
    speakers)

  * **source**: a device that an application can get audio from (e.g., a
    microphone)

  These terms are straightforward if you remember that they are named from an
  *application’s perspective*.

* There are two types of application streams:

  * **sink-input**: a stream going to a **sink** (e.g., the sound output by an
    application, going to speakers)

  * **source-output**: a stream coming from a **source** (e.g., the sound input to
    an application, coming from a microphone)

  These terms are confusing because they seem to be named from *PulseAudio’s
  perspective* (a **sink-input** is the sound *coming into a sink* from an
  application). I find it helpful to mentally flip the order of the two words
  and think of them as “input (to a) sink” and “output (from a) source”.

* And there’s one more concept that I couldn’t fit into a better category:

  * **monitor**: a hidden **source** that automatically exists for each **sink**
    and allows accessing the audio that is being sent to that sink

## pavucontrol

**pavucontrol** (PulseAudio Volume Control) is the best way to interact with
PulseAudio because it doesn’t try to simplify or hide these concepts from you
(like the volume widgets of many desktop environments do). 

<figure>

The first two tabs of pavucontrol let you adjust the connections and volumes of
**sink-inputs** (Playback) and **source-outputs** (Recording).

![screenshot of pavucontrol’s Playback tab](/media/pulseaudio/pavucontrol.svg)

Note that the **sink-inputs** and **source-outputs** are defined by the
applications, and pavucontrol lets you choose which **sinks** and **sources**
they are attached to.

</figure>

# Device Naming

Each device has a name used internally by PulseAudio as well as a *description*
which is meant to be human-readable.

<figure>

pavucontrol shows the description, not the internal name.

![pavucontrol showing a sink called "Sound Core3D [Sound Blaster Recon3D /
Z-Series] (SB1570 SB Audigy Fx) Analog Stereo"](/media/pulseaudio/pavucontrol-long-name.png)

Sometimes the “human-readability” of the description is questionable.

</figure>

## Finding a Device’s Name

Use the `list-sinks` or `list-sources`
commands and search for the lines that contain `name:` or `device.description
=`. Then find the name that matches the description.

```bash
$ pacmd list-sinks | grep -E 'name:|device\.description'
        name: <alsa_output.pci-0000_00_1f.3.analog-stereo>
                device.description = "Sound Core3D [Sound Blaster Recon3D / Z-Series] (SB1570 SB Audigy Fx) Analog Stereo"
        name: <bluez_sink.38_18_4C_7D_5C_08.a2dp_sink>
                device.description = "Headphones"
```

The name is the part between the `<>` brackets (i.e., the brackets are not part
of the name).

Save the device name in a shell variable to save typing in future commands.

```bash
$ device=alsa_output.pci-0000_00_1f.3.analog-stereo
```

## Changing a Device’s Description

Use the `update-sink-proplist` or `update-source-proplist` commands to change
the `device.description` property.

```bash
$ pacmd update-sink-proplist "$device" 'device.description="Laptop Speakers"'
```

<figure>

![pavucontrol showing a sink called "Laptop Speakers"](/media/pulseaudio/pavucontrol-short-name.png)

Now that’s what I call “human-readable”!

</figure>

# Useful Modules

## Null Sink

A **null sink** is a virtual sink that you can send audio to. The sink itself
isn’t so useful, but its **monitor** is very useful.

Use `load-module module-null-sink` to create a new null sink.

```bash
$ pacmd load-module module-null-sink
```

This creates the sink with the description “Null Sink”. If you want a more
descriptive description, you can specify it using `sink_properties`.

```bash
$ pacmd load-module module-null-sink "sink_properties='device.description=\"Helpfully-Named Output\"'"
```

**Important:** If you forget the quoting around the entire `sink_properties` value, PulseAudio
will fail to parse the arguments and will silently fail to load the module. (The
errors are actually logged by the PulseAudio daemon, so you can find them in
`journalctl --user -u pulseaudio`.)

## Loopback

...

# Routing Audio

## Application to Application

Use a **null sink** to receive the audio from the source application, and
configure the other application to read from the **monitor** of the **null
sink**.

<figure>

Let’s set things up to send the audio from Firefox over Discord voice channel.
First, create a **null sink** called “Discord Input”.

```bash
$ pacmd load-module module-null-sink "sink_properties='device.description=\"Discord Input\"'"
```

In pavucontrol’s **Playback** tab, route the audio from Firefox there.

![selecting “Discord Input” in pavucontrol](/media/pulseaudio/pavucontrol-discord-input.png)

In pavucontrol’s **Recording** tab, route the audio from the monitor to Discord.

<p><img id=monitor-img class=secret-border alt="selecting “Monitor of Discord Input” in pavucontrol" src="/media/pulseaudio/pavucontrol-monitor-of-discord-input.png"></p>

Voilà!

</figure>

## Application+Microphone to Application

Use a **null sink** to receive the audio from the source application, configure
the other application to read from the **monitor** of the **null sink**, and use
a **loopback** to route the microphone to the **null sink** also.

<figure>

...

</figure>

## Application to Application+Speakers

...

## Application to Application+Speakers *and* Microphone to Application

...


<style>
#monitor-img:hover {border-color: ;}
</style>
<script>
function monitorImageToggle() {
  const image = document.getElementById("monitor-img");
  if (image.src.includes("pavucontrol")) {
    image.src = "/media/pulseaudio/monitor-of-discord-input.jpg";
  } else {
    image.src = "/media/pulseaudio/pavucontrol-monitor-of-discord-input.png";
  }
}
document.getElementById("monitor-img").addEventListener("click", monitorImageToggle);
</script>
