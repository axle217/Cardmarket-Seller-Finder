# Cardmarket Seller Finder

When you go to [Cardmarket](https://www.cardmarket.com/en/YuGiOh) and wonder:

> **Which seller has the most cards I'm looking for, and what would they cost?**

These scripts help you find out.

Compared to "Shopping Wizard" and "Sellers with the Most Cards" features,
Pros: unlimited run, you have more control to prioritize cards to buy over large wanted list, and compare prices directly over multiple cards
Cons: open pages and copy paste manually, and lookup to seller profile again (Tips: filter the country to your desired shipping cost in CM and copy up to your price limit)

## Installation

* Install **Python 3.8+**
* Clone/download this repository
* No external Python packages are required

Check Python:

```bash
python3 --version
```

## 1. Parse Cardmarket listings

Copy the listings for a card from Cardmarket into a text file, e.g.:

```text
hamon.txt
```

Then run:

```bash
python3 parse_listings.py hamon.txt hamon.csv CORI
```

Format:

```text
python3 parse_listings.py INPUT OUTPUT SET_CODE
```

Multiple set codes can be provided:

```bash
python3 parse_listings.py cards.txt cards.csv CORI LOB MRD
```

The result is a CSV containing:

```text
seller,condition,price,quantity
```

Repeat this for each card you're interested in.

## 2. Find sellers shared between cards

Once you have multiple CSVs:

```bash
python3 search_occurrence.py seller hamon.csv ravielli.csv blueeyes.csv
```

This finds sellers appearing in **two or more files** and shows their corresponding listings.

Example:

```text
seller: seller_alpha

  [hamon.csv]
    price: 0.05
    quantity: 3

  [ravielli.csv]
    price: 0.15
    quantity: 2
```

This lets you identify sellers who can provide multiple cards from your wanted list and compare their prices.

## Save the results

```bash
python3 search_occurrence.py seller hamon.csv ravielli.csv blueeyes.csv > results.txt
```

Or display and save at the same time:

```bash
python3 search_occurrence.py seller hamon.csv ravielli.csv blueeyes.csv 2>&1 | tee results.txt
```

## In short

```text
Cardmarket
    ↓
Copy listings
    ↓
parse_listings.py
    ↓
CSV per card
    ↓
search_occurrence.py
    ↓
Find sellers carrying multiple wanted cards
    ↓
Compare prices
```

No Cardmarket scraping is involved — you simply copy the listing text from the pages you are interested in.
