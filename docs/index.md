---
layout: default
title: Index
---

## Table of Contents
<ol>
  <li><a href="#articles">Articles</a>
    <ol>
      {% for category in site.categories %}
        <li><a href="#category-{{ category | first }}">{{ category | first }}</a></li>
      {% endfor %}
    </ol>
  </li>
  <li><a href="#authors">Authors</a></li>
</ol>

## Articles
{% include article-list.html %}

## Authors
{% include author-list.html %}

<div style="height:2000px;"></div>
