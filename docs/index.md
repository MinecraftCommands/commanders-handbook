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

## Posts
<ul>
  {% for post in site.posts %}
    <li>
      <a href="{{ site.baseurl }}{{ post.url }}">{{ post.title }}</a>
    </li>
  {% endfor %}
</ul>
