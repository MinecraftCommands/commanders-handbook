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
1. type (when using `type=`)
2. gamemode
3. team
4. type (when using `type=!`)
5. tag
6. name
7. scores
8. advancements
9. nbt

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

### 2. `gamemode`
`gamemode` is similar to `type`, it discards all non-player entities immediately, leaving only player entities that need to be processed

### 3. `team`
`team` is also similar to type, it discards all non-living entities. This is still more entities that need to be processed than `gamemode`, hence why `team` is after `gamemode`

## 4. `type`
When using `type=!` the number of entities discarded is much lower than when using `type=`, and so it is suggested to put it after `gamemode` and `team` which throw out more entity types in this case

### 5. `tag`
`tag` is a very cheap selector, entity tags are stored as a hashset and therefore tag lookup is very fast. Specifically, lookup is `O(k)`, where `k` is the length of the tag name.

### 6. `name`
`name` is slower than `tag` because the name of an entity is a JSON text component, and is converted to a plain text string any time the `name` selector argument is used.

### 7. `score`
`score` has a slightly more complicated lookup process. The score name and the entity's UUID are both used as keys to find the associated score value, and then that value is compared with the range specified.

### 8. `advancement`
`advancement` has a very similar lookup to `score`, but has a slightly more complicated value test. It either checks if the player has the advancement, or checks the criteria to see if they have the specified criteria

### 9. `nbt`
`nbt` is the slowest selector. In memory the game doesn't use NBT, instead every block/entity stores it in its own structure. This means that in order to test, or manipulate NBT in any way, the game first needs to convert these custom structures back into NBT, which is does by serializing to NBT then deserializing back into some internal structure that is used for comparing the NBT. This process is intensive, and so `nbt` selector arguments should be last, and avoided whenever possible.