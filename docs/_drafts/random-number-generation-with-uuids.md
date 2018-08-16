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
execute store result score $rng temp run data get entity @e[type=minecraft:area_effect_cloud,tag=rngcloud,limit=1] UUIDLeast 0.00000000023283
kill @e[type=minecraft:area_effect_cloud,tag=rngcloud]
```

Here's a quick way to see the results:
```
scoreboard objectives add temp dummy
scoreboard objectives setdisplay sidebar temp
```

## How it works

When we summon an entity, it is instantaneously assigned a [universally unique identifier (UUID)](https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html). The resulting number is large enough that it needs to be stored in two separate NBT longs: `UUIDMost` and `UUIDLeast`. Both of these longs are effectively random, but we go with `UUIDLeast` for no obvious reason.

We've still got to deal with the fact that the scoreboard can only hold integers, so it's a good thing `data get` comes with a `<scale>` factor. We use `0.00000000023283` because math:

1. `UUIDLeast` is a signed long and can hold from `-(2^63)` to `2^63 - 1`
2. Scoreboard values are signed integers and can only hold from `-(2^31)` to `2^31 - 1`
3. We need to crunch-down `UUIDLeast` to fit it into the scoreboard: `(2^63) / (2^31) = (2^32)`
4. Using the reciprocal `1 / (2^32)` and rounding-down we get our scale of `0.00000000023283`

And we've our freshly-generated random number is on the scoreboard:
```
scoreboard players get $rng temp
```

## Caveats and criticisms
### It cannot be seeded
The most obvious fallback to this approach is that it cannot be seeded. If you do need seeded PRNG, then you'll have to look elsewhere. If don't need seeded PRNG, or don't know what this means in the first place, then this limitation isn't going to make a difference.

### UUIDs aren't necessarily random
While UUIDs can be [generated randomly](https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html#randomUUID()), it's important to realize that they are generally designed to be *unique* and not necessarily random. They are often composed of values such as system clock time, clock sequence, and hardware MAC address, to help ensure that they are indeed unique.

Lucky or us, Minecraft uses a kind of UUID that is "generated using a cryptographically strong pseudo random number generator" [^1] so we can be confident that this method will give us sufficiently random results.

Fun fact: we went with `UUIDLeast` over `UUIDMost` simply because the most-significant bits of every UUID contain a static `version` field, denoting which format the UUID takes on. Presumably this reduces the overall entropy of `UUIDMost`, making `UUIDLeast` the ever-so-slightly more random half. Whether such a small difference is worth considering (or even entirely correct) is up for argument.

## Resources and further reading
- Check out [the uuidrng datapack]() for a more thorough implementation of UUID-based RNG.
- Read over [Java's UUID class](https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html) if you want to know more about how UUIDs are generated.

[^1]: https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html#randomUUID()
