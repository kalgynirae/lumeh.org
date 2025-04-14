---
title: Bash Configuration
---

# Bash Configuration

This page is a collection of miscellaneous recommended configuration for Bash
users, with full rationale given so you can decide whether they are appropriate
for you.

## History

### Use a custom HISTFILE

If you’ve ever wanted to check how Bash behaves in the absence of your
personal configs, you may have run a command like `bash --noprofile --norc`.
Unfortunately, when you did this, you probably mysteriously lost a bunch of your
command history. To avoid this, set `HISTFILE` to a nonstandard path in your
`.bashrc` file:

<figure class=fullwidth>
<figcaption><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-minus-fill" viewBox="0 0 16 16">
  <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1M6 8.5h4a.5.5 0 0 1 0 1H6a.5.5 0 0 1 0-1"/>
</svg>~/.bashrc <span class=excerpt>(excerpt)</span></figcaption>
<pre><code><span class=comment># Use a nonstandard history file to avoid accidentally losing history</span>
HISTFILE=~/.bash_history_actual
</code></pre>
</figure>

**Explanation:** Bash’s default behavior is to keep only 500 entries in the
history file. If you run Bash without loading your personal configs, Bash will
truncate the history file to 500 entries when it starts. Putting your history
file at a nonstandard path ensures that Bash can touch your history file only if
it has also loaded your other history settings.

### Save more history

Bash’s default is to store only 500 lines of history, which is tiny. In recent
versions, both `HISTSIZE` and `HISTFILESIZE` can accept a negative value to
indicate that their size should be unbounded. My strategy is to make these
unbounded and revisit this decision if I start to notice performance problems
later.

<figure class=fullwidth>
<figcaption><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-minus-fill" viewBox="0 0 16 16">
  <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1M6 8.5h4a.5.5 0 0 1 0 1H6a.5.5 0 0 1 0-1"/>
</svg>~/.bashrc <span class=excerpt>(excerpt)</span></figcaption>
<pre><code><span class=comment># Don't limit the size of the history file</span>
HISTFILESIZE=-1
<span class=comment># Don't limit the size of the in-memory history list</span>
HISTSIZE=-1
</code></pre>
</figure>

In older versions of Bash (I’m not sure how old), setting at least one of
these variables to a negative value caused problems. I suggest checking `man
bash` on your system to ensure that your version explicitly supports such values
(search for the phrase “*values less than zero*”).

If you don’t want to make these values unbounded, I suggest setting
`HISTFILESIZE` to 500,000. Based on my personal experience, that should be
enough to store several years of history even for a heavy terminal user.

## Readline

Readline is the library used by Bash (and some other programs) to provide
command-line editing and completion features.

### Improving readability

<figure class=fullwidth>
<figcaption><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-minus-fill" viewBox="0 0 16 16">
  <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1M6 8.5h4a.5.5 0 0 1 0 1H6a.5.5 0 0 1 0-1"/>
</svg>~/.inputrc <span class=excerpt>(excerpt)</span></figcaption>
<pre><code><span class=comment># Briefly highlight the corresponding opening symbol when entering a closing symbol</span>
set blink-matching-paren on
<span class=comment># When listing possible completions, color the part that is already typed</span>
set colored-completion-prefix on
</code></pre>
</figure>

### Reducing keystrokes

Readline has two options that make tab completion more flexible. The first
treats uppercase and lowercase as interchangeable for completion purposes, and
the second treats underscores and hyphens as interchangeable. For example, with
both options enabled, you can type <kbd>a-b<kbd>Tab</kbd></kbd> to complete a
file that is actually named <span class=path>A_BASKETBALL</span>.

<figure class=fullwidth>
<figcaption><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-minus-fill" viewBox="0 0 16 16">
  <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1M6 8.5h4a.5.5 0 0 1 0 1H6a.5.5 0 0 1 0-1"/>
</svg>~/.inputrc <span class=excerpt>(excerpt)</span></figcaption>
<pre><code>set completion-ignore-case on
set completion-map-case on
</code></pre>
</figure>

You can also have Readline *immediately* print the possible completions when
there are several options (instead of requiring a second <kbd><kbd>Tab</kbd></kbd> to print
them).

<figure class=fullwidth>
<figcaption><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-minus-fill" viewBox="0 0 16 16">
  <path d="M9.293 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V4.707A1 1 0 0 0 13.707 4L10 .293A1 1 0 0 0 9.293 0M9.5 3.5v-2l3 3h-2a1 1 0 0 1-1-1M6 8.5h4a.5.5 0 0 1 0 1H6a.5.5 0 0 1 0-1"/>
</svg>~/.inputrc <span class=excerpt>(excerpt)</span></figcaption>
<pre><code>set show-all-if-unmodified on
</code></pre>
</figure>
