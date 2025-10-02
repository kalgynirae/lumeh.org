# lumeh.org

[**lumeh.org**] is Colin Chan’s personal website. It is built using
**Websleydale**, a custom static site generator designed specifically
for this website.

[**lumeh.org**]: https://www.lumeh.org/

The text you’re reading right now comes from [README.md in the lumeh.org
Git repo]. If you’re reading this on GitHub, this explanation probably
seems inane. But this file also appears as a [page on lumeh.org], so if
you’re reading it there, I hope the explanation is helpful!

[README.md in the lumeh.org Git repo]: https://github.com/kalgynirae/lumeh.org/blob/main/README.md
[page on lumeh.org]: https://www.lumeh.org/projects/lumeh.org/

## Reporting problems

There are two ways to report a problem with lumeh.org:

* <a href=https://github.com/kalgynirae/lumeh.org/issues/new rel=external target=_blank>File an issue on GitHub</a> (preferred, requires a GitHub account)
* <a href=https://airtable.com/appopNVjvtXgt5gQQ/pagwo1PQB92bHio2c/form rel=external target=_blank>Complete a form on Airtable</a> (no account needed)

## Contributing

You’re very welcome to suggest changes and edits to the site, but since it is my personal website,
there’s no guarantee that I will accept or use your suggestions. Feel free to open an issue for
discussion before spending time making a pull request that might not be accepted.

### Building the site

The build process requires <a href=https://docs.astral.sh/uv/ rel=external target=_blank>uv</a>
(Python package manager) and Bash. Theoretically it could work in macOS, but I only test it in Linux
and (occasionally) WSL.

1. **Clone the repo** and `cd` into it.
2. **Init submodules** with `git submodule update --init`. (Note that the *assets* repo will fail to
   clone because it is private.)
3. **Check out submodule branches** with `git submodule foreach 'if ! git symbolic-ref -q HEAD >/dev/null; then git checkout main || git checkout master; fi'`.
4. **Build** with `./build.sh`.

To view the result, run `./test.sh` and visit the displayed address in
your browser.

<aside class=important>

**Note:** The test site has a few limitations. First, because certain files are kept in a separate
*assets* repo (which is private), some files are expected to be missing, including the file that
provides the monospaced font. Second, the test server doesn’t handle redirects—you’ll get 404 errors
instead of being redirected.

</aside>

## Data & privacy

### Cookies

I **despise** cookie banners; therefore lumeh.org avoids using any cookies.

I like cookies, though, and I highly recommend making your own! I recommend either my [classic
chocolate-chip recipe](https://www.lumeh.org/recipes/cookies/) known for its use of maple flavoring
or [Chonklate Chip Cookies](https://www.lumeh.org/recipes/chonklate-chip-cookies/) which imitate
Levain Bakery’s famous cookies.

### Site usage

I use Plausible to collect <a href=https://plausible.io/lumeh.org rel=external target=_blank>site
usage data</a>. Plausible does not collect any personally identifiable information—refer to their <a
href=https://plausible.io/data-policy rel=external target=_blank>data policy</a> for details.

### Uptime

lumeh.org’s <a href=https://stats.uptimerobot.com/2bTDg6gjOV rel=external target=_blank>uptime and
current status</a> are monitored by UptimeRobot.
