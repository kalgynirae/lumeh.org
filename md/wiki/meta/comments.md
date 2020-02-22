---
title: Comments
comments:
  - author: Colin
    date: 2020-01-30
    content: >
      This is a great page. It shows how to write comments without actually
      explaining how to write comments!
  - author: Bolin
    date: 2020-01-30
    content: >
      I'm not sure I agree—an actual explanation would be helpful.
  - author: Colin
    date: 2020-01-30
    content: >
      Fair. Here's how it works:

       1. Click the **Add a comment** link above. This brings you to an editor
          on GitHub where you can modify the source of the page.

       2. Add your comment to the YAML block at the top of the source in the
          following format:

          ```yaml
          comments:
            - author: <name>
              date: <date>
              content: >
                <content (Markdown supported)>
          ```

       3. Use GitHub's interface to submit a pull request with your changes.

      That's all there is to it! You can check this page's source (the link is
      above) to see some examples of real comments.
---

**{{ site.title }}** is a static site powered by GitHub Pages. Comments can be added
to a page by submitting a *pull request* that modifies the page's content.

This page demonstrates how the comment system works.

# See also

* [This page's source](https://raw.githubusercontent.com/{{ site.github.repository_nwo }}/{{ site.github.build_revision }}/{{ page.path }})
