---
title: Which Selector Arguments Should I Include
category: Selectors
tags: commands selectors optimization
permalink: which-selector-arguments-should-i-include
author: vdvman1
---

## TL;DR
Whenever possible include these selector arguments:
* distance
* dx/dy/dz
* type

## Explanation
By including any selector arguments the limit the volume the game is able to use a more efficient algorithm for searching through entities. Rather than going through the list of all loaded entities the game instead uses the per-chunk entity lists, and only looks at the chunks that are at least partially inside the volume specified.
When combined with `type` this search becomes even more efficient, as explained in more detail in [When to use `type` in selectors]({{ site.baseurl }}{% post_url 2018-08-22-when-to-use-type-in-selectors %})