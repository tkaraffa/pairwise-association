# pairwise-association

One method to compute the confidence that, given a certain response, another reponse is present, is through pairwise association. This repo attempts to establish a repeatable, modular class to mine a dataset for those particular associative rules. By default, a threshold of `0.75` is given, meaning that a rule `P(B | A)` is only found if for at least 3/4 of instances, `A` is present when `B` is present, relative to all instances that contain `A`.


A rule `A implies B` is only valid if its confidence `conf(A => B)`, or `P(B | A)`, exceeds the given threshold `S`.

A valid rule is defined as:

![\Large P(B | A)\geqLarge S](https://latex.codecogs.com/svg.latex?\Large&space;P(B|A)\geq\Large&space;S) 

or

![\Large P(B \cup A)/P(A)\geqLarge S](https://latex.codecogs.com/svg.latex?\frac{&space;P(A&space;\cup&space;B)}{P(A)}\geq\Large&space;S) 

If this criteria is met, it can be reasonably said that 
![\Large A\implies B](https://latex.codecogs.com/svg.latex?&space;A\implies&space;B) or `A implies B`