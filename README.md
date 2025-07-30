<div class=compact-headings>

# lumeh.org

[**lumeh.org**] is Colin Chan’s personal website. It is built using
**Websleydale**, a custom static site generator designed specifically
for this website (more details below).

[**lumeh.org**]: https://www.lumeh.org/

The text you’re reading right now comes from [README.md in the lumeh.org
Git repo]. If you’re reading this on GitHub, this explanation probably
seems inane. But this file also appears as a [page on lumeh.org], so if
you’re reading it there, I hope the explanation is useful!

[README.md in the lumeh.org Git repo]: https://github.com/kalgynirae/lumeh.org/blob/main/README.md
[page on lumeh.org]: https://www.lumeh.org/projects/lumeh.org/

## Status page

lumeh.org has a
<a href=https://stats.uptimerobot.com/2bTDg6gjOV rel=external target=_blank>status page</a>
hosted by UptimeRobot.

## Analytics

lumeh.org uses Plausible for privacy-friendly analytics. You can read their
<a href=https://plausible.io/data-policy rel=external target=_blank>data policy</a>
for more information, and you can explore the collected data at
<a href=https://plausible.io/lumeh.org rel=external target=_blank>plausible.io/lumeh.org</a>.

## Building the site

1. **Clone the repo.**
2. **Init submodules** with `git submodule update --init`. (Note that
   this will fail to clone the private *assets* repo.)
3. **Build** with `./build.sh`.

To view the result, run `./test.sh` and visit the displayed address in
your browser.

<aside class=important>

**Note:** Because certain files are kept in a separate *assets* repo
(which is private), some files are expected to be missing, and the test
site will display with an incorrect monospaced font.

</aside>

## Contributing

You’re very welcome to suggest changes and edits to the site, but since
it is my *personal* website, there’s no guarantee that I will accept or
use your suggestions.

</div>
