# lumeh.org

[**lumeh.org**] is Colin Chan’s personal website. It is built using
**Websleydale**, a custom static site generator designed specifically
for this website (more details below).

[**lumeh.org**]: https://www.lumeh.org/

The text you’re reading right now comes from [README.md in the lumeh.org
Git repo]. If you’re reading this on GitHub, this explanation probably
seems inane. But this file also appears as a [page on lumeh.org], so if
you’re reading it there, I hope the explanation is useful!

[README.md in the lumeh.org Git repo]: https://github.com/kalgynirae/lumeh.org/blob/master/README.md
[page on lumeh.org]: https://www.lumeh.org/projects/lumeh.org/

## Building the site

1. **Clone the repo.**
2. **Init submodules** with `git submodule update --init`. Note that
   this will fail to clone the *assets* repo (because it is private).
3. **Build** with `uv run -s build.py`. Note that this will report many
   missing files due to the absence of the *assets* repo.

To view the result, run `./test.sh` and visit the displayed address in
your browser. Note that this preview will use the wrong monospace font
(since the correct one is only available via the *assets* repo).

## Contributing

You’re very welcome to suggest changes and edits to the site, but since
it is my *personal* website, there’s no guarantee that I will accept or
use your suggestions.
