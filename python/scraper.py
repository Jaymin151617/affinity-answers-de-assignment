"""
MDComputers Product Scraper

This script takes a product search term from the user, retrieves all
matching products from the MDComputers website, and extracts product
details including:

- Product ID
- Product name
- Current price
- Original price
- Discount percentage
- Product link
- Product image URL

The results are deduplicated using the product ID and saved in a
readable JSON file along with the search URL, expected item count,
and number of products successfully scraped.

Usage:
    1. Run the script:
           python scraper.py

    2. Enter the product search term when prompted:
           Enter search term: external hard disk

    3. The scraped data will be saved to:
           products.json
       
       The file is created in the same directory as the script.

Design Choices:
    - BeautifulSoup is used to parse the HTML because the website
      returns HTML product listings and it provides simple CSS
      selectors for extracting the required fields.

    - URL parameters are passed through the requests `params`
      argument instead of manually constructing the URL. This
      ensures that spaces and special characters in search terms
      are encoded correctly.

    - Pagination is handled by reading the total number of pages
      from the search results and requesting each page.

    - Products are stored in a dictionary using the product ID as
      the key. This prevents duplicate products from appearing in
      the final output.

    - The scraped results are written to a JSON file instead of being
      printed to the terminal. This makes the complete output easier to
      read, review, store, and reuse for further processing without
      cluttering the terminal.

    - JSON is used as the output format because it supports both
      metadata and structured product records while remaining
      human-readable and easy to process programmatically.

    - Prices and discount percentages are converted to numeric
      values so they can be easily used for further analysis.

    - The scraper compares the number of unique products collected
      with the number reported by the website and displays a warning
      if the counts do not match.
"""


# Import required libraries
import json
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Path to the output JSON file in the same directory as the script
OUTPUT_FILE = Path(__file__).resolve().parent / "products.json"

# Base URL of the website
BASE_URL = "https://mdcomputers.in"

# Headers used to mimic a regular web browser request
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def get_page(url, params=None) -> str:
    """
    Fetch the webpage and return its HTML content.

    Returns:
        str: The HTML content of the webpage.
    """
    response = requests.get(
        url,
        params=params,
        headers=HEADERS,
        timeout=30
    )

    # Raise an error if the request was unsuccessful
    response.raise_for_status()

    return response.text


def parse_price(price_tag) -> int | None:
    """
    Convert price text such as '₹2,799' into 2799.

    Returns:
        int | None: The numeric price, or None if no price is found.
    """
    if price_tag is None:
        return None

    price_text = price_tag.get_text(strip=True)

    # Remove everything except digits.
    # Example: '₹2,799' -> '2799'
    price_text = re.sub(r"[^\d]", "", price_text)

    return int(price_text) if price_text else None


def parse_discount(discount_tag) -> int | None:
    """
    Convert discount text such as '-20%' into 20.

    Returns:
        int | None: The discount percentage, or None if no discount is found.
    """
    if discount_tag is None:
        return None

    discount_text = discount_tag.get_text(strip=True)

    # Find one or more consecutive digits.
    # Example: '-20%' -> '20'
    match = re.search(r"(\d+)", discount_text)

    return int(match.group(1)) if match else None


def parse_product_id(cart_button) -> str | None:
    """
    Extract the product ID from an add-to-cart button.

    Example:
        cart.add('13274') -> 13274

    Returns:
        str | None: The product ID, or None if it cannot be found.
    """
    if cart_button is None:
        return None

    onclick = cart_button.get("onclick", "")

    # Match the number inside cart.add('...').
    # Example: "cart.add('13274')" -> "13274"
    match = re.search(r"cart\.add\('(\d+)'\)", onclick)

    return match.group(1) if match else None


def parse_products(html) -> list:
    """
    Parse product information from the HTML page.

    Extracts the product ID, name, prices, discount, product link,
    and image URL for each product found.

    Returns:
        list: A list of dictionaries containing product details.
    """
    soup = BeautifulSoup(html, "html.parser")
    products = []

    # Find each product card on the page.
    for product in soup.select(".product-grid-item"):

        # Find the relevant elements within the product card.
        name_tag = product.select_one(".product-entities-title a")
        price_tag = product.select_one(".price .ins .amount")
        original_price_tag = product.select_one(".price .del .amount")
        discount_tag = product.select_one(".onsale.product-label")
        image_tag = product.select_one(".product-element-top img")
        cart_button = product.select_one(".add_to_cart_button")

        # Skip the product if its name or price is missing.
        if name_tag is None or price_tag is None:
            continue

        # Extract product name and product page URL.
        name = name_tag.get_text(strip=True)
        product_link = name_tag.get("href")

        # Convert price and discount values to numeric values.
        price = parse_price(price_tag)
        original_price = parse_price(original_price_tag)
        discount_percent = parse_discount(discount_tag)

        # Extract the product image URL if available.
        image_url = None
        if image_tag is not None:
            image_url = image_tag.get("src")

        # Extract product ID from the add-to-cart button.
        product_id = parse_product_id(cart_button)

        # Store the extracted information as a dictionary.
        products.append({
            "product_id": product_id,
            "name": name,
            "price": price,
            "original_price": original_price,
            "discount_percent": discount_percent,
            "product_link": product_link,
            "image_url": image_url
        })

    return products


def get_pagination_info(html) -> tuple[int | None, int]:
    """
    Extract the total number of items and pages from the pagination text.

    Example:
        'Showing 21 to 40 of 161 (9 Pages)'
        -> (161, 9)

    Returns:
        tuple: Total number of items and total number of pages.
               Returns (None, 1) if pagination information is not found.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Convert the page HTML into plain text.
    text = soup.get_text(" ", strip=True)

    # Extract the total items and pages from the pagination text.
    # Example:
    # 'Showing 21 to 40 of 161 (9 Pages)' -> 161 and 9
    match = re.search(
        r"Showing\s+\d+\s+to\s+\d+\s+of\s+(\d+)\s+\((\d+)\s+Pages?\)",
        text
    )

    if match:
        number_of_items = int(match.group(1))
        number_of_pages = int(match.group(2))

        return number_of_items, number_of_pages

    # Default values when pagination information is not found.
    return None, 1


def main():
    """
    Take a search term, scrape all matching products, and save the results
    to a JSON file.
    """
    search_term = input("Enter search term: ")

    # Build search parameters.
    # Requests will safely URL-encode special characters.
    search_params = {
        "route": "product/search",
        "search": search_term
    }

    # Store products using product ID as the key to avoid duplicates.
    all_products = {}

    # Fetch the first page.
    html = get_page(BASE_URL, params=search_params)

    print("Scraping page 1...")
    first_page_products = parse_products(html)

    # Stop if the search returned no products.
    if not first_page_products:
        print("No products found for this search term.")
        return

    # Get the total number of products and pages from the first page.
    number_of_items, number_of_pages = get_pagination_info(html)

    # Add products from the first page.
    for product in first_page_products:
        product_id = product["product_id"]

        if product_id is not None:
            all_products[product_id] = product

    # Fetch and process the remaining pages.
    for page in range(2, number_of_pages + 1):
        page_params = {
            **search_params,
            "page": page
        }

        print(f"Scraping page {page}/{number_of_pages}...")

        html = get_page(BASE_URL, params=page_params)

        for product in parse_products(html):
            product_id = product["product_id"]

            if product_id is not None:
                all_products[product_id] = product

    # Convert the dictionary of products into a list.
    all_products = list(all_products.values())
    scraped_items = len(all_products)

    # Build the complete search URL for the JSON output.
    search_url = requests.Request(
        "GET",
        BASE_URL,
        params=search_params
    ).prepare().url

    # Validate the number of scraped products.
    if number_of_items == scraped_items:
        print(
            f"\nValidation successful: "
            f"{scraped_items} of {number_of_items} products scraped."
        )
    else:
        print(
            "\nWARNING: Product count mismatch!"
            f"\nExpected: {number_of_items}"
            f"\nScraped:  {scraped_items}"
        )

    # Create the final JSON structure.
    output = {
        "search_url": search_url,
        "number_of_items": number_of_items,
        "scraped_items": scraped_items,
        "products": all_products
    }

    # Write the results to a readable JSON file.
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            output,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nScraping complete.")
    print(f"Output file: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
