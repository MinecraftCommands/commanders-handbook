---
title: Selector Argument Order
category: Selectors
tags: commands selectors optimization
permalink: selector-argument-order
author: vdvman1
---

Different selector arguments have different performance impacts, and so it is important to order the selectors to eliminate unnecessary processing.
> Note that this ordering is currently speculative, real tests of performance will be performed and this order may be updated if the empirical testing shows otherwise
> 
> This ordering is also not guaranteed to remain the same between versions. This document will be updated whenever a change in the ordering is noticed, but we will not be checking every version. If you have any information on changes between versions please make an issue or a pull request so that this document may be updated.

## TL;DR
Selector arguments should be in this order:
1. type
2. In any order:
  * gamemode
  * team
3. tag
4. name
5. scores
6. advancements
7. nbt

These selector arguments have predefined order, and as such the order does not matter:
* level
* x_rotation/y_rotation
* distance
* x/y/z
* dx/dy/dz
* sort
* limit

## In code ordering
MrPingouin has analyzed the decompiled code for selectors, and determined the following.

These selector arguments are processed in whatever order you put them in your selector:
* name
* gamemode
* team
* type
* tag
* nbt
* score
* advancement

After the above selector arguments are processed the following are processed in order:
1. level
2. x_rotation
3. y_rotation

The following selector arguments perform tasks both before and after all other selector arguments:
* distance
* x/y/z
* dx/dy/dz
* sort
* limit

## Custom Ordering Explanation
### 1. `type`
`type` is known to drastically reduce the number of entities processed. For a full explanation see [When to use `type` in selectors]({{ site.baseurl }}{% post_url 2018-08-22-when-to-use-type-in-selectors %})

### 2. `gamemode` and `team`
`gamemode` and `team` are able to discard a very large number of entities at very little cost.
> TODO: explain in detail why these selector arguments can discard a large number of entities

e.g. Using `gamemode=creative` limits the selector to only creative players, which on a survival server would result in discarding all survival players, which very likely is a large number of players.

### 3. `tag`
`tag` is a very cheap selector, entity tags are stored as a hashset and therefore tag lookup is very fast. Specifically, lookup is `O(k)`, where `k` is the length of the tag name.

### 4. `name`
`name` is slower than `tag` because the name of an entity is a JSON text component, and is converted to a plain text string any time the `name` selector argument is used.

### 5. `score`
`score` has a slightly more complicated lookup process. The score name and the entity's UUID are both used as keys to find the associated score value, and then that value is compared with the range specified.

### 6. `advancement`
`advancement` has a very similar lookup to `score`, but has a slightly more complicated value test. It either checks if the player has the advancement, or checks the criteria to see if they have the specified criteria

### 7. `nbt`
`nbt` is the slowest selector. In memory the game doesn't use NBT, instead every block/entity stores it in its own structure. This means that in order to test, or manipulate NBT in any way, the game first needs to convert these custom structures back into NBT, which is does by serializing to NBT then deserializing back into some internal structure that is used for comparing the NBT. This process is intensive, and so `nbt` selector arguments should be last, and avoided whenever possible.