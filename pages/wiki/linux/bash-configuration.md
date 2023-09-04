---
title: Bash Configuration
---

This page is a collection of miscellaneous recommended configuration for Bash
users, with explanations!

# History

## Where did my history go?

If you've ever wanted to check how Bash behaves in the absence of your
personal configs, you may have run a command like `bash --noprofile --norc`.
Unfortunately, when you did this, you probably mysteriously lost a bunch of your
command history. To avoid this, set `HISTFILE` to a nonstandard path (i.e., not
the default `~/.bash_history`) in your `.bashrc` file:

```bash
# Use a nonstandard history file to avoid accidentally losing history
HISTFILE=~/.bash_history_actual
```

**Explanation:** Bash's default behavior is to keep only 500 entries in the
history file. If you run Bash without loading your personal configs, Bash will
truncate the history file to 500 entries when it exits. Using a nonstandard
history file ensures that Bash will only touch *your* history file when it has
also loaded your other history settings.

# Readline (inputrc)

## Improving readability

```inputrc
set blink-matching-paren on
set colored-completion-prefix on
```

## Reducing keystrokes

```inputrc
set completion-ignore-case on
set completion-map-case on
set show-all-if-unmodified on
```
