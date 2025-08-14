---
title: Stop adjusting my microphone!
show_authors: true
---

# Stop adjusting my microphone!

How to prevent applications from **secretly adjusting the gain (input volume) of your microphone**
while you’re in a voice call.

## General solutions

The only general solution I’m aware of is for WirePlumber (the PipeWire session manager used in
recent Linux distributions). I’ll update this page if I become aware of general solutions for any
other environments.

### WirePlumber

On a Linux system using WirePlumber, it’s possible to prevent arbitrary applications from adjusting
levels by writing access rules:

<figure class=fullwidth>
<figcaption><l-icon name=file>~/.config/wireplumber/wireplumber.conf.d/90-prevent-adjusting.conf</l-icon></figcaption>
<pre><code>access.rules = [
  {
    matches = [
      {
        application.process.binary = "electron"
      }
    ]
    actions = {
      update-props = {
        default_permissions = "rx"
      }
    }
  }
]
</code></pre>
</figure>

<p>
You can find the relevant binary name by running <code>wpctl status | less</code>,
looking at the list of clients, and examining clients with
<code>wpctl inspect <span class=placeholder>ID</span> | less</code>.
You can also match on <strong>application.name</strong> or (presumably) other properties that
the inspect command shows. Based on brief testing, it seems that a rule will be applied if <em>any</em>
<code>{ … }</code> section within **matches** is a match for the client, and I’m guessing that
writing multiple conditions within one <code>{ … }</code> section means that <em>all</em> of the
conditions need to match. But this is all conjecture; I haven’t found any documentation about how
the matching works. If you are aware of any documentation, please
<a href="https://airtable.com/appopNVjvtXgt5gQQ/pagwo1PQB92bHio2c/form?prefill_URL=https%3A%2F%2Fwww.lumeh.org%2Fwiki%2Faudio%2Fstop-adjusting-my-microphone%2F&prefill_Description=Documentation+about+matching+in+WirePlumber+exists+here%3A%20&hide_Attachments=true" rel=external target=_blank
>let me know</a>.
</p>

## Application-specific solutions

### Google Chrome (and other Chromium-based browsers)

Chrome has a flag that can be used to disable this behavior: In a new tab, paste
`chrome://flags/#enable-webrtc-allow-input-volume-adjustment` into the address bar. This should
bring you to the flag titled “Allow WebRTC to adjust the input volume.” Use the drop-down to set it
to **Disabled**.

<p>
This flag exists at time of writing, but if you’re reading this in the future and the flag has been
removed, please
<a href="https://airtable.com/appopNVjvtXgt5gQQ/pagwo1PQB92bHio2c/form?prefill_URL=https%3A%2F%2Fwww.lumeh.org%2Fwiki%2Faudio%2Fstop-adjusting-my-microphone%2F&prefill_Description=The+Chrome+flag+doesn%27t+exist+for+me+on+Chrome+version%3A+%3CVERSION+%28get+from+chrome%3A%2F%2Fversion%29%3E&hide_Attachments=true" rel=external target=_blank
>let me know</a>.
</p>

### Discord

In Discord, open **User Settings** (gear icon), click on the **Voice & Video** tab, and scroll down to find the **Automatic Gain Control** setting. Turn this setting off.
