---
title: Random number generation (RNG) with UUIDs
category: Commands
tags: commands randomizers rng math
permalink: random-number-generation-with-uuids
author: Arcensoth
---

We can easily and effectively generate large random numbers by (ab)using entity UUIDs.

## Give me commands
Set things up once:
```
scoreboard objectives add temp dummy
scoreboard objectives setdisplay sidebar temp
```

Generate a new random number:
```
summon minecraft:area_effect_cloud ~ ~ ~ {Duration:1200,Tags:["rngcloud"]}
execute store result score $rng temp run data get entity @e[type=minecraft:area_effect_cloud,tag=rngcloud,limit=1] UUIDMost 0.0000000002328306436538696289
kill @e[type=minecraft:area_effect_cloud,tag=rngcloud]
```

You can use `Duration:0` and drop the `kill` altogether if you're not doing this by hand.

## How it works
When we summon an entity, it is instantaneously assigned a [random-type UUID](#but-are-uuids-random). The resulting number is large enough that it needs to be stored in two separate NBT longs: `UUIDMost` and `UUIDLeast`.

Now comes the question: do we use `UUIDMost` or `UUIDLeast`? It's easy to flip a coin, but with a bit of digging you'll find out that `UUIDMost` [is the better option](#uuidmost-vs-uuidleast).

In any case, we still need to deal with the fact that scoreboard values can only hold integers. It's a good thing `data get` comes with a `<scale>` factor. We use `0.0000000002328306436538696289` because math:

1. `UUIDMost` is a signed long and can hold from `-(2^63)` to `2^63 - 1`
2. Scoreboard values are signed integers and can only hold from `-(2^31)` to `2^31 - 1`
3. We need to crunch-down `UUIDMost` to fit it into the scoreboard: `(2^63) / (2^31) = (2^32)`
4. Using the reciprocal `1 / (2^32)` and rounding-down we get the aforementioned scale

And we've got a freshly-generated random number ready to go. Keep in mind the results fall in the range `-2147483648..2147483647` and this is the part where you do modulo.

Be aware that Minecraft 1.13.1 [altered various scoreboard operations](https://bugs.mojang.com/browse/MC-135431), meaning results may not be consistent even within the same major version.

### `UUIDMost` vs `UUIDLeast`
Just by [spamming some commands](https://i.imgur.com/iuzMGJQ.png) you might notice that `UUIDMost` seems more random than `UUIDLeast`.

It turns out this holds up on a technical level, too. Under the hood `UUIDMost` gives us 32 bits of full random goodness, whereas `UUIDLeast` comes in short at a measly 30. The reason for this is twofold:

1. The most-significant half (`UUIDMost`) of a random-type UUID contains 60 bits of entropy, where bits 49 through 52 define a static `version` field. The least-significant half (`UUIDLeast`) contains 62 bits of entropy, but this time bits 0 and 1 define a static `variant` field. The remaining 122 bits are set "to randomly (or pseudo-randomly) chosen values." [^3]
2. We can only access the 32 most-signifcant bits of a long due to scoreboard scaling. With `UUIDMost` we're left with 32 bits of entropy for the taking, but `UUIDLeast` leaves its 2 most-significant bits to be desired.

You might also notice that `UUIDLeast` is always negative, which is exactly what happened to those 2 bits. This is due to the way UUIDs record their format, wherein the `variant` field "contains a value which identifies the layout of the UUID" [^1] and hence remains static for every UUID of the same format. Moreover, the `variant` consists of "a variable number of the most significant bits of octet 8 of the UUID" [^3] i.e. the most-significant bits of `UUIDLeast`. Suffice it to say that the `variant` is solely responsible for determining the sign of every `UUIDLeast` we see.

## Questions and criticisms
### How do you seed this thing?
You can't. The most obvious fallback to this approach is that it cannot be seeded. If you do need seeded PRNG, then you'll have to look elsewhere. If you don't need seeded PRNG, or don't know what this means in the first place, then this limitation isn't going to make a difference.

### But are UUIDs random?
While UUIDs can be generated with variable amounts of randomness, it's important to realize that they are generally designed to be *unique* and not necessarily random. They are often composed of values such as system clock time, clock sequence, and hardware MAC address, to help ensure that they are indeed unique.

Lucky for us, Minecraft uses the kind of UUID that is "generated using a cryptographically strong pseudo random number generator" [^2] so we can be confident that this method will give us sufficiently random results. (You can verify that Minecraft does indeed use random-type UUIDs by decoding a few and checking their `version` field.)

## Resources and further reading
- Read over [Java's UUID class](https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html) and [RFC 4122](http://www.ietf.org/rfc/rfc4122.txt) if you want to know more about how UUIDs are generated.

---

[^1]: [Java's UUID Class](https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html)
[^2]: [Java's UUID Class, method `randomUUID()`](https://docs.oracle.com/javase/7/docs/api/java/util/UUID.html#randomUUID())
[^3]: [RFC 4122](http://www.ietf.org/rfc/rfc4122.txt)
