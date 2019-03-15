import csv
import pandas

def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):

    with open(invoice_file, "a+", newline='') as f:
        writer = csv.writer(f)
        row = customer_name, item_code, item_description, item_monthly_price
        writer.writerow(row)

def single_customer(customer_name, invoice_file):
    def within_function(target_csv):
        with open(invoice_file) as source_csv:
            original_entries = [line.split(",") for line in source_csv if line]
            add_furniture(customer_name, item[1], item[2], item[3])

    return within_function

if __name__ == "__main__":
    add_furniture("invoice_file.csv", "Elisa Miles", "LR04", "Leather Sofa", "25.00")
    add_furniture("invoice_file.csv", "Edward Data", "KT78", "Kitchen Table", "10.00")
    add_furniture("invoice_file.csv", "Alex Gonzales", "BR02", "Queen Mattress", "17.00")

    create_invoice = single_customer("Susan Wong", "invoice_file.csv")
    create_invoice("test_items.csv")
