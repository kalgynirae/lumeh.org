---
title: Git Thesaurus
---

Because Git is relatively simple under the hood but its commands tend to have a
lot of convenient flags and shortcuts, there are usually several ways to
accomplish the same thing. This page attempts to document many of those ways.

NOTE: This is very much a work-in-progress.

# Equivalent ways to do the same thing

## Reset a branch to a specific location

```sh
# Reset foo to the new location
git branch -f foo <branch|commit>
git checkout foo
```

```sh
git checkout foo
# Reset foo to the new location
git reset --hard <branch|commit>
```

```sh
# Move to the new location
git checkout <branch|commit>
# Reset foo to here
git checkout -B foo
```

```sh
# Move to the new location
git checkout <branch|commit>
# Delete foo
git branch -D foo
# Create foo here
git checkout -b foo
```
