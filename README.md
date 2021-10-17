# pairwise-association

One method to compute the confidence that, given a certain response, another reponse is present, is through pairwise association. This repo attempts to establish a repeatable, modular class to mine a dataset for those particular associative rules. By default, a threshold of `0.75` is given, meaning that a rule `P(B | A)` is only found if for at least 3/4 of instances, `A` is present when `B` is present, relative to all instances that contain `A`.


A rule `A implies B` is only valid if its confidence `conf(A => B)`, or `P(B | A)`, exceeds the given threshold `S`.

A valid rule is defined as:

![\Large P(B | A)\geqLarge S](https://latex.codecogs.com/svg.latex?\Large&space;P(B|A)\geq\Large&space;S) 

or

![\Large P(B \cup A)/P(A)\geqLarge S](https://latex.codecogs.com/svg.latex?\frac{&space;P(A&space;\cup&space;B)}{P(A)}\geq\Large&space;S) 

If this criteria is met, it can be reasonably said that 
![\Large A\implies B](https://latex.codecogs.com/svg.latex?&space;A\implies&space;B) or `A implies B`

## Usage

```
usage: main.py [-h] [--threshold THRESHOLD] [--ignore IGNORE] file

Find pairwise association rules.

positional arguments:
  file                  The file with which to calculate pairwise associations

optional arguments:
  -h, --help            show this help message and exit
  --threshold THRESHOLD The value with which to filter pairwise probabilities (default=0.75).
  --ignore IGNORE       Column(s) to ignore and NOT calculate confidence rules for.
```

## Examples

The classic example of finding pairwise association rules is a grocery store receipt: given that a customer buys Product A (say, oat milk), how likely are they to buy *another* product (say, cookies). By examining a range of receipts, we can determine the probability that, given a purchase of oat milk, that same customer also purchased cookies.

With sample data like the following:
```
name,receipt
Wendy Jennings,bread;cheese;cookies;milk
Angela Cameron,bread;cheese;cookies;milk
Angela Carlson,milk
Kayla Knight,milk
Thomas Stokes,cheese;cookies;milk
Brenda Phelps,bread;cheese;cookies;milk
Toni Williams,bread;cheese;cookies;milk
Peggy Dorsey,bread;cheese;cookies;milk
Nicholas Smith,bread;cheese;cookies
...
```
we obtain the following rules
```
conf(receipt_milk => receipt_cookies) = 0.722
conf(receipt_cookies => receipt_milk) = 0.72
conf(receipt_bread => receipt_cookies) = 0.705
conf(receipt_bread => receipt_milk) = 0.695
conf(receipt_cheese => receipt_cookies) = 0.686
conf(receipt_bread => receipt_cheese) = 0.685
conf(receipt_cheese => receipt_milk) = 0.679
conf(receipt_cheese => receipt_bread) = 0.663
conf(receipt_cookies => receipt_cheese) = 0.652
conf(receipt_cookies => receipt_bread) = 0.649
conf(receipt_milk => receipt_cheese) = 0.648
conf(receipt_milk => receipt_bread) = 0.642
```
Note: each item is prefixed with `receipt` because the original file stores its values in a column named `receipt`. In a single-column use-case such as this, the prefix is unnecessary; in a multiple-column use-case, the prefix differentiates identical values obtained from different columns.