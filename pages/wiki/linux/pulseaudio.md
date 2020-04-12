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

  * **sink-input**: a stream going to a sink (e.g., the sound output by an
    application, going to speakers)

  * **source-output**: a stream coming from a source (e.g., the sound input to
    an application, coming from a microphone)

  These terms are confusing because they seem to be named from *PulseAudio’s
  perspective* (a sink-input is the sound *coming into a sink* from an
  application). I find it helpful to mentally flip the order of the two words
  and think of them as “input (to a) sink” and “output (from a) source”.

* And there’s one more concept that I couldn’t fit into a better category:

  * **monitor**: a hidden source that automatically exists for each sink and
    allows accessing the audio that is being sent to that sink

## pavucontrol

**pavucontrol** (PulseAudio Volume Control) is the best way to interact with
PulseAudio because it doesn’t try to simplify or hide these concepts from you
(like the volume widgets of many desktop environments do). 

<figure>

The first two tabs of pavucontrol let you adjust the connections and volumes of
sink-inputs and source-outputs.

![screenshot of pavucontrol’s Playback tab](/media/pulseaudio/pavucontrol.svg)

Note that the sink-inputs and source-outputs correspond to applications, and
pavucontrol lets you choose which sinks and sources they are attached to.

</figure>


# Device Naming

Each device has a name used internally by PulseAudio as well as a *description*
which is meant to be human-readable.

<figure>

pavucontrol shows the description, not the internal name.

![pavucontrol showing a sink called “Sound Core3D [Sound Blaster Recon3D / Z-Series] (SB1570 SB Audigy Fx) Analog Stereo”](/media/pulseaudio/pavucontrol-long-name.png)

Sometimes the “human-readability” of the description is questionable.

</figure>

## Finding Device Names

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

<aside class=tip>

**Tip:** Save the device name(s) in shell variables to save typing in future commands.

```bash
$ speakers=alsa_output.pci-0000_00_1f.3.analog-stereo
$ headphones=bluez_sink.38_18_4C_7D_5C_08.a2dp_sink
```

</aside>

## Changing Device Descriptions

Use the `update-sink-proplist` or `update-source-proplist` commands to change
the `device.description` property.

```bash
$ pacmd update-sink-proplist $speakers 'device.description="Laptop Speakers"'
```

<figure>

![pavucontrol showing a sink called “Laptop Speakers”](/media/pulseaudio/pavucontrol-short-name.png)

Now that’s what I call “human-readable”!

</figure>


# Useful Modules

## Null Sink

A **null sink** is a virtual sink that discards audio sent to it. That’s not
very useful by itself, but the **monitor** that comes with it can be very
useful.

Use `load-module module-null-sink` to create a new null sink.

```bash
$ pacmd load-module module-null-sink \
    sink_name=null \
    sink_properties=\'device.description=\"Null Output\"\'
```

You can omit the `sink_name` and `sink_properties` arguments if you don’t care
about the name and description (you’ll get the defaults, “null” and “Null
Output”). But if this is part of a more complex setup, it’s worth it to set
descriptive names from the beginning (see [Application to
Application](#application-to-application) for a practical example).

<aside class=important>

**Important:** The value given to `sink_properties` must be quoted, or
PulseAudio will silently fail to load the module. (It’s not actually silent; the
errors are logged by the PulseAudio daemon, so you can find them in `journalctl
--user -u pulseaudio`.) In this example, we escaped all the quotes with
backslashes so that the shell does not interpret them and they make it through
to PulseAudio.

</aside>

Use pavucontrol to route application audio to the null sink as desired.

## Combined Sink

A **combined sink** is a virtual sink that forwards audio to multiple other
sinks.

First, [find the names](#finding-device-names) of the sinks you want to combine,
then use `load-module module-combine-sink` to create a new combined sink.

```bash
$ pacmd load-module module-combine-sink slaves=$speakers,$headphones
```

The combined sink will automatically have a readable description.

<aside class=note>

**Note:** Although the combined sink *appears* in pavucontrol (as sink-inputs
attached to the sinks being combined), it is not possible to *change* which
sinks are being combined except by unloading the module and loading it again.

</aside>

## Loopback

A **loopback** forwards audio from a source to a sink.

Use `load-module module-loopback` to create a new loopback.

```bash
$ pacmd load-module module-loopback
```

Then use pavucontrol to choose which source and sink the loopback should use.

<aside class=note>

**Note:** The sink-input and source-output created by the loopback have
dynamically-updated descriptions. These will likely be confusing until you have
set the correct source and sink for the loopback; then they will make sense.

</aside>


# Routing Audio

## Application to Application

Use a [null sink](#null-sink) to receive the audio from the source application,
and configure the other application to read from the monitor of the null sink.

<figure>

Let’s set things up to route the audio from Firefox to a Discord voice channel.
First, create a null sink called “Discord Input”.

```bash
$ pacmd load-module module-null-sink \
    sink_name=discord \
    sink_properties=\'device.description=\"Discord Input\"\'
```

In pavucontrol’s Playback tab, route the audio from Firefox there.

![selecting “Discord Input” in pavucontrol](/media/pulseaudio/pavucontrol-discord-input.png)

In pavucontrol’s Recording tab, route the audio from the monitor to Discord.

<p><img id=monitor-img class=secret-border alt="selecting “Monitor of Discord Input” in pavucontrol" src="/media/pulseaudio/pavucontrol-monitor-of-discord-input.png"></p>

Voilà!

</figure>

## Application to Application+Speakers

Follow the previous instructions, then add a [combined sink](#combined-sink)
that forwards to the null sink and the speakers.

<figure>

After following the previous example, set up the combined sink.

```bash
$ pacmd load-module module-combine-sink slaves=discord,$speakers
```

![selecting “Simultaneous output to Discord Input, Laptop Speakers” in pavucontrol](/media/pulseaudio/pavucontrol-simultaneous-output.png)

</figure>

## Application to Application+Speakers *and* Microphone to Application

Follow the previous instructions, then add a [loopback](#loopback) that forwards
the microphone to the null sink.

<figure>

After following the previous example, set up the loopback.

```bash
$ pacmd load-module module-loopback
```

In pavucontrol’s Recording tab, route the audio from the microphone to the
loopback.

![selecting “...” in pavucontrol](/media/pulseaudio/pavucontrol-loopback-recording.png)

In pavucontrol’s Playback tab, route the audio from the loopback to the null
sink.

![selecting “...” in pavucontrol](/media/pulseaudio/pavucontrol-loopback-playback.png)

</figure>


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
