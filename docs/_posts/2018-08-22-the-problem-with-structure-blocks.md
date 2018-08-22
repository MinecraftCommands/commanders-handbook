---
title: The problem with structure blocks
category: Structures
tags: structures structure-blocks
permalink: the-problem-with-structure-blocks
author: Arcensoth
---

Structure blocks are an amazing tool and one of the many milestones in mapmaking history. Almost every time I suggest implementing a structure command, I get the argument that you can just use structure blocks and redstone blocks to achieve the same result. This is true in many cases, but obviously much less convenient. It's also entirely false and becomes a huge problem in certain edge cases, like the one I'm about to explain.

Imagine we want to generate our own homemade chunk of randomized ore. We'll start with pure stone, throw in a generous amount of iron, sprinkle in a bit of gold, and then a drop of diamonds.

Now, there are several ways of achieving this but I'm going to cover one of the most common that utilizes several "layered" structures with different integrity ratios to achieve a sort of "scattered" distribution. Not the best way of randomizing ore, I know, but it helps get the idea across.

One important note to make is that *structure blocks activate the instant they are powered*. One common mistake is to place all of the structure blocks and then power them all at the same time. This will often result in only one of the structure blocks activating, because the structure will load and overwrite the remaining structure blocks before they even realize they were powered.

Luckily we can use this behaviour to our advantage: place each pair of structure block and redstone block, one after another, in alternating positions. We only need two blocks of space to do this for any number of layered structures, and we can do it right outside the cube to avoid tainting the randomized cube.

Neat, right?

**But here's the problem.** What if we only have our original chunk of space to work with? What if we can't touch anything outside of this space for a good reason? (For example, we want to randomize an entire chunk but can't be sure whether the neighbouring chunks have already been populated.)

In this case, we have no choice but to sacrifice two blocks of "random space" within the chunk. If you do some thinking, you'll realize that this problem exists for any layered structure method. It is an unfortunate result of the fact that we need to use "physical" blocks in world space to load a structure.

The best solution to this problem that I've come up with is to simply replace any remaining structure and/or redstone blocks in the 2-block area with some static block - in this case, probably stone. Regardless of our decision, we've effectively lost 2 blocks of randomness and also require additional work to cover our tracks.

So yes, a dedicated command for loading structures would indeed allow us to do more than we currently can with structure blocks.
