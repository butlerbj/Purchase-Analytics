import csv
from operator import itemgetter
from collections import defaultdict

# read in 'order_products.csv' to a list of lists
with open('./input/order_products.csv') as f:
    reader = csv.reader(f)
    header = next(reader)
    order_products = [header] + [[int(number) for number in row] for row in reader]
orders = order_products[1:]
orders.sort(key=lambda x: x[1])

# read in 'order_products.csv' to a list of lists
with open('./input/products.csv') as f:
    reader = csv.reader(f)
    header = next(reader)
    products = [row for row in reader]
    for row in products:
        del row[1:3]  # delete rows that are unused

# create two lists containing the products and its respective department
# and combine them into one dictionary for easy indexing
product_list = [row[0] for row in products]
department = [row[1] for row in products]
dept_prod_dict = dict(zip(product_list, department))


def build_product_freq_table(data, kind):
    """Builds a frequency table from the data by product_id.

    Parameters
    ----------
        data : two-dimensional array
            List of lists read in from the CSV.

        kind : 'total' or 'first_orders'
            Type of frequency table to construct.
    Returns
    -------
        frequency_table : dictionary
            Dictionary containing `product_id` as keys and
            the sums as values.

    """

    kinds = {'total': 1, 'first_orders': 3}
    freq_table = dict()
    var = kinds[kind]

    if kind == 'total':
        for row in data:
            key = str(row[1])
            if key in freq_table:
                freq_table[key] += 1
            else:
                freq_table[key] = 1

    if kind == 'first_orders':
        for row in data:
            key = str(row[1])
            if row[var] == 0:
                if key in freq_table:
                    freq_table[key] += 1
                else:
                    freq_table[key] = 1

    return freq_table


def build_dept_freq_table(dept_map, prod_freq_table):
    """Builds a frequency table from the data by department_id.

    Parameters
    ----------

        dept_map : dictionary
            Dictionary containing products as keys and
            their respective department as values.

        prod_freq_table : dictionary
            Existing product id frequency table corresponding
            to the kind of output table desired.
            e.g., if a 'totals_by_department' frequency table
            is desired, then the input 'freq_table' should be
            a 'build_product_freq_table' dictionary.

    Returns
    -------
        frequency_table : dictionary
            Dictionary containing `department_id` as keys and
            the sums as values.

    """

    freq_table = dict()

    for key, value in dept_map.items():
        if key in prod_freq_table:
            if value in freq_table:
                freq_table[value] += prod_freq_table[key]
            else:
                freq_table[value] = prod_freq_table[key]
        else:
            continue

    return freq_table


def build_final_dict(totals, first_orders):
    """Builds final dictionary containing necessary values.

    Parameters
    ----------
        totals : dictionary
            Totals dictionary built using build_dept_freq_table

        first_orders : dictionary
            First orders dictionary built using build_dept_freq_table
    Returns
    -------
        final_dict : defaultdictionary
            Dictionary containing department_id as keys
            and total purchases, number of first orders,
            and the ratio as keys (list)

    """
    final_dict = defaultdict(list)

    for key, value in totals.items():
        final_dict[key].append(value)
        if key in first_orders:
            final_dict[key].append(first_orders[key])
            final_dict[key].append(round(first_orders[key]/value, 2))
        if key not in first_orders:
            final_dict[key].append(0)
            final_dict[key].append(round(0 / value, 2))

    return final_dict


def convert_for_writing(final_dict):
    """Converts final dictionary to list for easier writing to csv.

    Parameters
    ----------
        final_dict : defaultdictionary
            Dictionary containing department_id as keys
            and total purchases, number of first orders,
            and the ratio as keys (list).
    Returns
    -------
        output_list : two-dimensional array
            final_dict converted to a list of lists.

    """

    output_list = list()
    for key, value in final_dict.items():
        final_dict[key].insert(0, int(key))
        output_list.append(value)
    output_list = sorted(output_list, key=itemgetter(0))
    for row in output_list:
        row[-1] = "{:.2f}".format(row[-1])

    return output_list


# build two frequency tables containing the total purchases
# and total first orders, by product_id
purchase_totals = build_product_freq_table(orders, kind='total')
first_order = build_product_freq_table(orders, kind='first_orders')

# build two frequency tables containing the total purchases
# and total first orders, by department_id
totals_by_dept = build_dept_freq_table(dept_prod_dict, purchase_totals)
first_by_dept = build_dept_freq_table(dept_prod_dict, first_order)

# build the final dictionary containing the desired values:
# number_of_orders, number_of_first_orders, and percentage
final_dict = build_final_dict(totals_by_dept, first_by_dept)

# convert the final dictionary to a list for easy writing to csv in desired
# output format
output_list = convert_for_writing(final_dict)

# write the output_list to csv, done!
csv_header = [['department_id', 'number_of_orders',
           'number_of_first_orders', 'percentage']]
csv_data = list()
csv_data.append(csv_header)
csv_data.append(output_list)
with open('./output/report.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_header)
    writer.writerows(output_list)
csv_file.close()
