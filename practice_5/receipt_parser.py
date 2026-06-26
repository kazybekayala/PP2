import re
import json

#reading receipt file
with open("raw.txt", "r", encoding="utf-8") as file:
    receipt = file.read()

#extract product names
products = re.findall(
    r"\d+\.\n(.+)",
    receipt
)

#extract prices
prices = re.findall(
    r"\n([\d ]+,\d{2})\nСтоимость",
    receipt
)

#convert prices from string to numbers
clean_prices = []

for price in prices:
    price = price.replace(" ", "")
    price = price.replace(",", ".")
    clean_prices.append(float(price))

#calculate total amount
total = sum(clean_prices)

#extract date and time
date_time = re.search(
    r"Время:\s*(\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2})",
    receipt
)

#extract payment method
payment = re.search(
    r"(Банковская карта):",
    receipt
)

#create structured output
data = {
    "products": products,
    "prices": clean_prices,
    "total_amount": total,
    "date_time": date_time.group(1) if date_time else None,
    "payment_method": payment.group(1) if payment else None
}

#print json output
print(json.dumps(
    data,
    ensure_ascii=False,
    indent=4
))