---
title: When to use `type` in selectors
category: Selectors
tags: commands selectors optimization
permalink: when-to-use-type-in-selectors
author: Arcensoth
---

In 1.12? Always. In 1.13? Very always.

(This is assuming you're only dealing with one type of entity.)

In 1.12, the reason isn't much more than how quick it is to compare entity types versus other arguments.

In 1.13, the reason is a bit more involved. In this version, the game will - in certain cases - use `type` to bypass all other types of entities in the search. These "certain cases" occur when when `type` is used alongside volumetric arguments `dx/dy/dz` and/or `distance`, so that the game may consult colliding chunks for their entities instead of the global list.

This works based on two factors:

1. each chunk stores its own collection of indexed entity lists, one for each type of entity, and
2. selectors consult colliding chunks for these lists, instead of the global non-indexed list, when provided with volumetric arguments.

The moral of the story is that providing `type` is good, and in some cases *very* good.

Throwing in a volumetric argument (`dx/dy/dz` and/or `distance`) where possible will help to reduce the overhead of selector processing, such as when there are many entities in the world of varying types. Consider the common case where only several area effect clouds are being used as markers. Here, something like `@e[type=minecraft:area_effect_cloud,distance=..1]` would allow the game to bypass all other entities in all non-colliding chunks. Huge savings!

Big thanks to @Skylinerw for digging into the source and verifying the behaviour directly. Also thanks to @Adrodoc on the testfor[dev] Discord server for sparking my interest in the topic in the first place.

I'll end this article with some informative excerpts from a chat with @Skylinerw on the /r/MinecraftCommands Discord server:

> In 1.12 the "indexed by type" in chunks is not relevant to `type` for selectors. The method `Chunk.getEntitiesOfTypeWithinAAAB()` takes in an entity class, but that's not based on the selector. Instead, it's based on what the *command itself* is "allowed" to target. For example, a large number of commands can select all entities (like `/execute`), thus it's searching for the `Entity` class (so whatever the selector is attempting to target is irrelevant and the indexing won't help). A command like `/effect` can only target `EntityLivingBase` entities, and `/give` can only target `EntityPlayer`.

> Aaaand just to follow up on the `type` thing overriding the default of `Entity`: I made a jar mod for 1.13 and can confirm that it *does* use `type` for accessing the indexed class types in chunk files. ~~I haven't checked if the global list of entities is indexed though.~~ Aaand that is also the same as 1.12: the global list is not indexed by class type.
