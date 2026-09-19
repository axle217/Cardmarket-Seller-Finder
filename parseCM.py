import argparse
import csv
import re


CONDITIONS = {
    "M", "NM", "EX", "GD", "LP", "PL", "PO"
}


def clean_price(line):
    match = re.search(r"([\d.,]+)\s*€", line)

    if not match:
        return None

    price = match.group(1).replace(".", "").replace(",", ".")

    return f"{float(price):.2f}"


def is_quantity(line):
    return bool(re.fullmatch(r"\d+", line.strip()))


def parse_listings(text, set_codes):
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    listings = []
    i = 0

    while i < len(lines):

        # Look for one of the supplied set codes
        if lines[i].upper() in set_codes:

            if i == 0:
                i += 1
                continue

            # Seller is immediately before the set code
            seller = lines[i - 1]

            # Condition follows the set code
            condition = None

            if i + 1 < len(lines):
                possible_condition = lines[i + 1].upper()

                if possible_condition in CONDITIONS:
                    condition = possible_condition

            if not condition:
                i += 1
                continue

            # Search for the price after the condition
            price_index = None
            price = None

            j = i + 2

            while j < len(lines):

                if "€" in lines[j]:
                    price = clean_price(lines[j])
                    price_index = j
                    break

                # Another set code means we've reached another listing
                if lines[j].upper() in set_codes:
                    break

                j += 1

            if price is None:
                i += 1
                continue

            # Quantity immediately follows price
            quantity = None

            if price_index + 1 < len(lines):
                if is_quantity(lines[price_index + 1]):
                    quantity = int(lines[price_index + 1])

            listings.append({
                "seller": seller,
                "condition": condition,
                "price": price,
                "quantity": quantity
            })

            i = price_index + 2
            continue

        i += 1

    return listings


def save_csv(listings, output_file):
    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "seller",
                "condition",
                "price",
                "quantity"
            ]
        )

        writer.writeheader()
        writer.writerows(listings)


def main():
    parser = argparse.ArgumentParser(
        description="Parse copied Cardmarket listings into CSV."
    )

    parser.add_argument(
        "input",
        help="Input text file containing copied listings"
    )

    parser.add_argument(
        "output",
        help="Output CSV filename"
    )

    parser.add_argument(
        "set_codes",
        nargs="+",
        help="One or more set codes, e.g. CORI LOB MRD"
    )

    args = parser.parse_args()

    # Normalize set codes to uppercase
    set_codes = {
        code.upper()
        for code in args.set_codes
    }

    with open(args.input, "r", encoding="utf-8") as file:
        text = file.read()

    listings = parse_listings(text, set_codes)

    save_csv(listings, args.output)

    print(f"Parsed {len(listings)} listings.")
    print(f"Set codes: {', '.join(sorted(set_codes))}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()

# ### Usage

# One set:

# ```bash
# python3 parse_listings.py listings.txt hamon.csv CORI
# ```

# Multiple sets:

# ```bash
# python3 parse_listings.py listings.txt cards.csv CORI LOB MRD
# ```

# The argument order is now:

# ```text
# python3 parse_listings.py INPUT OUTPUT SET_CODE [SET_CODE ...]
# ```

# So there's no set-specific configuration left inside the script. You can reuse the same parser for different Cardmarket copies simply by changing the command-line arguments.
