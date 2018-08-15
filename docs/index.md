---
layout: default
title: Table of Contents
---

<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ site.baseurl }}{% post_url 2010-07-21-name-of-post %}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
