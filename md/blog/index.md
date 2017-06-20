---
title: index
---

So, this is the index, eh?

### Posts

{% for post in site.posts %}
* [[{{ post.date | date: "%Y-%m-%d" }}] {{ post.title }}]({{ post.url }})
{% endfor %}
