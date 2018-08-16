---
title: Random number generation (RNG) with UUIDs
category: Commands
tags: commands randomizers rng math
permalink: random-number-generation-with-uuids
author: Arcensoth
---

We can easily and effectively generate large random numbers by (ab)using entity UUIDs:
```
summon minecraft:area_effect_cloud ~ ~ ~ {Duration:1200,Tags:["rngcloud"]}
execute store result score $rng temp run data get entity @e[type=minecraft:area_effect_cloud,tag=rngcloud,limit=1] UUIDMost 0.0000000002328306436538696289
kill @e[type=minecraft:area_effect_cloud,tag=rngcloud]
```

Here's a quick way to see the results:
```
scoreboard objectives add temp dummy
scoreboard objectives setdisplay sidebar temp
```

## How it works
When we summon an entity, it is instantaneously assigned a [universally unique identifier (UUID)](https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html). The resulting number is large enough that it needs to be stored in two separate NBT longs: `UUIDMost` and `UUIDLeast`. Both of these longs are meant to be random, in theory, but in practice `UUIDMost` [seems to be the better option](#uuidmost-vs-uuidleast).

We still need to deal with the fact that scoreboard values can only hold integers, so it's a good thing `data get` comes with a `<scale>` factor. We use `0.0000000002328306436538696289` because math:

1. `UUIDMost` is a signed long and can hold from `-(2^63)` to `2^63 - 1`
2. Scoreboard values are signed integers and can only hold from `-(2^31)` to `2^31 - 1`
3. We need to crunch-down `UUIDMost` to fit it into the scoreboard: `(2^63) / (2^31) = (2^32)`
4. Using the reciprocal `1 / (2^32)` and rounding-down we get the aforementioned scale

And we've got a freshly-generated random number ready to go. Keep in mind the results fall in the range `-2147483648..2147483647` so you may need to cap the value according to your needs.

Be aware that Minecraft 1.13.1 altered the way various scoreboard operations work with negative numbers, meaning results may not be consistent even within the same major version. [^2]

### `UUIDMost` vs `UUIDLeast`
Some empirical results show that `UUIDMost` is actually "more random" than `UUIDLeast`. [^3]

Notice how `UUIDLeast` is always negative. This may due to [the way UUIDs record their format](https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html), wherein the `variant` field "contains a value which identifies the layout of the UUID" [^1] and hence remains static for every UUID of the same format. Moreover, the `variant` consists of "a variable number of the most significant bits of octet 8 of the UUID" (AKA the most-significant bits of the least-significant half of the UUID). It's possible that the value of `variant` (i.e. whatever type of UUID Minecraft employs) is solely responsible for determining the sign of every `UUIDLeast` we see.

## Caveats and criticisms
### It cannot be seeded
The most obvious fallback to this approach is that it cannot be seeded. If you do need seeded PRNG, then you'll have to look elsewhere. If don't need seeded PRNG, or don't know what this means in the first place, then this limitation isn't going to make a difference.

### UUIDs aren't necessarily random
While UUIDs can be [generated randomly](https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html#randomUUID()), it's important to realize that they are generally designed to be *unique* and not necessarily random. They are often composed of values such as system clock time, clock sequence, and hardware MAC address, to help ensure that they are indeed unique.

Lucky or us, Minecraft uses a kind of UUID that is "generated using a cryptographically strong pseudo random number generator" [^4] so we can be confident that this method will give us sufficiently random results.

## Resources and further reading
- Check out [this datapack](#) for a more thorough implementation of UUID-based RNG.
- Read over [Java's UUID class](https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html) if you want to know more about how UUIDs are generated.

[^1]: https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html
[^2]: https://bugs.mojang.com/browse/MC-135431
[^3]: https://i.imgur.com/iuzMGJQ.png
[^4]: https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html#randomUUID()
[^5]: http://www.ietf.org/rfc/rfc4122.txt
