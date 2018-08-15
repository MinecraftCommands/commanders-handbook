---
layout: default
title: Table of Contents
---

## Authors
<ul>
  {% for author in site.authors %}
    <li>
      <a href="{{ site.baseurl }}{{ author.url }}">{{ author.title }}</a>
    </li>
  {% endfor %}
</ul>

## Articles
{% for category in site.categories %}
### {{ category }}
{% for post in site.posts %}
- [post.title]({{ site.baseurl }}{{ post.url }})
{% endfor %}
{% endfor %}
