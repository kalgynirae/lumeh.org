# lumeh.org

[**lumeh.org**] is Colin Chan’s personal website. It is built using a custom static site generator
called *Websleydale*. It uses neither [cookies](#cookies) nor [LLMs](#no-llms).

[**lumeh.org**]: https://www.lumeh.org/

The text you’re reading right now comes from [README.md in the lumeh.org
Git repo]. If you’re reading this on GitHub, this explanation probably
seems silly. But this file also appears as a [page on lumeh.org], so if
you’re reading it there, I hope the explanation is helpful!

[README.md in the lumeh.org Git repo]: https://github.com/kalgynirae/lumeh.org/blob/main/README.md
[page on lumeh.org]: https://www.lumeh.org/projects/lumeh.org/

## Reporting problems

There are two ways to report a problem with lumeh.org:

* <a href=https://airtable.com/appopNVjvtXgt5gQQ/pagwo1PQB92bHio2c/form rel=external target=_blank>Complete a form</a> (easier, no account needed)
* <a href=https://github.com/kalgynirae/lumeh.org/issues/new rel=external target=_blank>File an issue on GitHub</a> (requires a GitHub account)

## Contributing

You’re very welcome to suggest changes and edits to the site, but since it is my personal website,
there’s no guarantee that I will accept or use your suggestions. Feel free to open an issue for
discussion if you are unsure.

### Building the site

The build process requires <a href=https://docs.astral.sh/uv/ rel=external target=_blank>uv</a>
(Python package manager) and Bash. I only test the process in Linux, but in theory it should work
elsewhere.

1. **Clone the repo** and `cd` into it.
2. **Init submodules** with `./checkout-submodules.sh`. (Note that the *assets* repo will fail to
   clone because it is private.)
3. **Build** with `./build.sh`.
4. **Serve** with `./test.sh` and visit the displayed address in your browser.

Note that the test site has some limitations: First, because the *assets* repo is private, many
files will be missing in your copy (notably including the web font for [Berkeley Mono]). Second, the test server
doesn’t handle redirects, so a few links will lead to 404s.

[Berkeley Mono]: https://usgraphics.com/products/berkeley-mono

### No LLMs

All parts of lumeh.org—code, prose, audio, graphics, etc.—were created by humans without assistance from LLMs. Some of these humans (notably Colin) have a preexisting fondness for em dashes and will continue to use them despite their recent stigma.

## Data & privacy

### Cookies

lumeh.org does not use cookies.

If you *like* cookies, you can make some at home! I recommend either my
[classic chocolate-chip cookies](https://www.lumeh.org/recipes/cookies/) known for their use of maple
flavoring or [Chonklate Chip Cookies](https://www.lumeh.org/recipes/chonklate-chip-cookies/) which
imitate Levain Bakery’s famous cookies.

### Site usage

I use Plausible to collect <a href=https://plausible.io/lumeh.org rel=external target=_blank>site
usage data</a>. Plausible does not collect any personally identifiable information—refer to their <a
href=https://plausible.io/data-policy rel=external target=_blank>data policy</a> for details.

### Uptime

lumeh.org’s <a href=https://stats.uptimerobot.com/2bTDg6gjOV rel=external target=_blank>uptime and
current status</a> are monitored by UptimeRobot.
