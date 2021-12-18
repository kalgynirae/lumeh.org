---
title: i3 + Firefox Context Menu Alignment Issue
---

For a long time, I have experienced an issue when running Firefox in the [i3
window manager]. Although I still don’t know why the issue occurs, I finally
have a good solution.

# The Issue

When I press the right mouse button, the context menu appears
such that the mouse cursor is already highlighting the first item in the menu.
Releasing the mouse button then immediately selects that item. This means that a
simple right-click on a page takes me back to the previous page—the menu appears
for just a moment, and the release of the mouse button selects the first item in
the menu (the Back item).

# A Good Solution

I realized I can use *userChrome.css* to shift the context menu a few pixels
away from the mouse cursor. Here’s the relevant excerpt from [my
*userChrome.css* file]:

```css
/* Offset right-click menus a bit so they don’t appear
   with the first item already highlighted */
#contentAreaContextMenu {
  margin-top: 5px !important;
}
```

This shifts the menu down by 5px, which is plenty to avoid the issue.

## userChrome.css

If you’re not familiar with *userChrome.css*, it’s a file you can create and add
to your [Firefox profile] that tweaks the appearance of Firefox itself. It is
frequently used to do things like change the location of the tab bar or hide
unneeded menu items. If you want to learn more about this, there are a bunch of
good resources at [/r/FirefoxCSS].

## Drawbacks

Since *userChrome.css* relies on the internal names of browser components
(`#contentAreaContextMenu` in this case), it's fairly likely to stop working in
future Firefox versions. If that happens, it shouldn't be too hard to find the
new name of the component used for the context menu.

[i3 window manager]: https://i3wm.org/
[my *userChrome.css* file]: https://github.com/kalgynirae/dotfiles/blob/00b7b7d62f9066d48120979108cf3c0d01356878/userChrome.css.mustache#L23-L26
[Firefox profile]: https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data
[/r/FirefoxCss]: https://www.reddit.com/r/FirefoxCSS/
