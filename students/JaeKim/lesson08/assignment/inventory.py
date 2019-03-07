def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    with open(invoice_file, 'a') as file:
        file.write("\n{},{},{},{}".format(customer_name, item_code, item_description, item_monthly_price))

def single_customer(customer_name, invoice_file):
    def another_function(target_csv):
        #print("add everything from {} to {} with name {}".format(target_csv, invoice_file.csv, customer_name))
        with open(invoice_file) as source_csv:
            original_entries = [line.split(",") for line in source_csv]

        with open(target_csv, 'a') as new_csv:
            for item in original_entries:
                new_csv.write("{},{},{},{}".format(customer_name, item[1], item[2], item[3]))
    return another_function

if __name__ == "__main__":
    create_invoice = single_customer("Susan Wong", "invoice_file.csv")
    create_invoice("test_items.csv")