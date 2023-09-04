NOTE: This page is very much a work-in-progress.

# The Building Blocks of Git

Some people learn best by understanding concepts from the ground up, while
others prefer to learn in more of a top-down way. For Git, I think it makes
sense to learn from the ground up even if that isn't the way you normally learn
best.  That's because Git actually has a *very small* number of core concepts,
so it's fairly easy to learn them, and once you do, you'll be able to work out
the solutions to almost any problems you encounter in Git.

## Commits are snapshots

Every commit in Git is a snapshot of all tracked files in the repo. That means,
if you can identify a specific commit (e.g., by its hash), you can use that to
retrieve the full contents of every tracked file as it was when the commit was
made.

This can be surprising because we often think of commits as *diffs*. For
example, we might talk about changing one file in the repo and then "committing
the change." Really, we are committing the new state of *all tracked files* --
it just so happens that all files but one are in the same state as they were in
the previous commit.

Adding to the confusion, there are many commands in Git itself that treat
commits as if they were diffs rather than snapshots. For example, `git show
<hash>` displays a commit as if it were a diff, but what it's really doing is
computing on-the-fly the differences between this commit and its parent commit.

## Commits have parents

Every* commit has one or more parent commits. If you have a specific commit, you
can find out its parent commit, and that commit's parent commit, and so on. So
Git can track down the whole history leading to a particular commit just from
the information stored in that commit, no branches involved.

*Not orphan commits (usually only the first commit made in a new repo).

* `git log <commit>`: Show all the history leading to `<commit>`

## Tags and branches are pointers to commits

Both tags and branches are little more than named pointers to specific commits.
The difference is that tags don't move, while branches move as you create new
commits.

We often think of branches as containing *sequences* of commits, but the reality
is that a branch only points to a single commit, and that commit has a parent
commit, which itself has a parent commit, and so on.

Many Git commands appear to treat a branch as if it contains many commits.  For
example, `git rebase` appears to move "the whole branch" to another base. Under
the hood, Git is computing on-the-fly the set of commits that are reachable from
the branch but not from the branch's configured upstream, and then rebasing
the computed set of commits. The branch does not actually *contain* that set of
commits, but we often think of it that way when performing operations.

Understanding that branches and tags are nothing more than pointers to specific
commits can be very powerful for resolving problems. For example, many problems
turn out to be some variant of "I want this branch to be over here." Well, since
the branch is just a pointer to a commit, you can just *change which commit it
points to*, either with a command that specifically does that (e.g., `git branch
-f <name> <hash>`) or by simply deleting the branch and creating a new one with
the same name at the desired commit.

Fast-forward merges are a safe way to move a branch forward.
TODO: explain more

## Committing moves the current branch

When you make a new commit, Git automatically moves the current branch to point
to the new commit.

If you `git checkout <hash>` to move to a specific commit, Git warns you that
you are in "detached HEAD" state. This simply means that you have no current
branch. If you commit in this state, no branch will be moved to point to the new
commit, so you risk losing track of the new commit unless you remember to create
a tag or branch there before you move somewhere else. However, this is really
not as risky as Git makes it sound. Even if you create new commits and then move
somewhere else without creating a branch or tag to get back, you can still use
`git reflog` to find the hashes of the commits you created.
