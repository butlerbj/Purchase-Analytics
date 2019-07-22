# Purchase-Analytics
Welcome to repo for the Insight Data Engineering coding challenge!

## Table of Contents
1. [Problem](README.md#problem)
1. [I/O](README.md#io)
1. [Approach](README.md#approach)
1. [Run instructions](README.md#run-instructions)
1. [Running the tests](README.md#running-the-tests)
1. [Limitations and future directions](README.md#instructions)
1. [Author](README.md#author)

## Problem

This challenge centered on an Instacart [dataset](https://www.instacart.com/datasets/grocery-shopping-2017) containing 3 million Instacart orders.

For this challenge, I was required to calculate, for each department, the number of times a product was requested, the number of times a product was requested for the first time, and a ratio of those two numbers.

## I/O

### Input datasets

For this challenge, we have two separate input data sources, `order_products.csv` and `products.csv`.

You can assume each line of the file `order_products.csv` holds data on one request. The file contains data of the form

```
order_id,product_id,add_to_cart_order,reordered
2,33120,1,1
2,28985,2,1
2,9327,3,0
2,45918,4,1
3,17668,1,1
3,46667,2,1
3,17461,4,1
3,32665,3,1
4,46842,1,0
```

where

* `order_id`: unique identifier of order
* `product_id`: unique identifier of product
* `add_to_cart_order`: sequence order in which each product was added to shopping cart
* `reordered`: flag indicating if the product has been ordered by this user at some point in the past. The field is `1` if the user has ordered it in the past and `0` if the user has not. While data engineers should validate their data, for the purposes of this challenge, you can take the `reordered` flag at face value and assume it accurately reflects whether the product has been ordered by the user before.

The file `products.csv` holds data on every product, and looks something like this:

```
product_id,product_name,aisle_id,department_id
9327,Garlic Powder,104,13
17461,Air Chilled Organic Boneless Skinless Chicken Breasts,35,12
17668,Unsweetened Chocolate Almond Breeze Almond Milk,91,16
28985,Michigan Organic Kale,83,4
32665,Organic Ezekiel 49 Bread Cinnamon Raisin,112,3
33120,Organic Egg Whites,86,16
45918,Coconut Butter,19,13
46667,Organic Ginger Root,83,4
46842,Plain Pre-Sliced Bagels,93,3
```
where

* `product_id`: unique identifier of the product
* `product_name`: name of the product
* `aisle_id`: identifier of aisle in which product is located
* `department_id`: identifier of department


### Expected output

Given the two input files in the input directory, the program will create an output file, `report.csv`, in the output directory that, for each department, surfaces the following statistics:

`number_of_orders`. How many times was a product requested from this department? (If the same product was ordered multiple times, we count it as multiple requests)

`number_of_first_orders`. How many of those requests contain products ordered for the first time?

`percentage`. What is the percentage of requests containing products ordered for the first time compared with the total number of requests for products from that department? (e.g., `number_of_first_orders` divided by `number_of_orders`)

For example, with the input files given above, the correct output file is

```
department_id,number_of_orders,number_of_first_orders,percentage
3,2,1,0.50
4,2,0,0.00
12,1,0,0.00
13,2,1,0.50
16,2,0,0.00
```

*The output file had to adhere to the following rules*

- It is listed in ascending order by `department_id`
- A `department_id` should be listed only if `number_of_orders` is greater than `0`
- `percentage` should be rounded to the second decimal

## Approach

I used Python 3.7.3 to complete this coding challenge, and opted for a straight-forward solution to the problem. As noted in the [problem](README.md#problem), I could not use any external packages or libraries
to complete the challenge. 

The source file `purchase_analytics.py` uses three modules from the [Python Standard Library](https://docs.python.org/3/library/index.html): `csv`, `operator`, and `collections`.

I read in the two input data sources, `order_products.csv` and `products.csv`, as lists of lists using the `csv` module. I constructed a series of dictionaries and iterated through them in order to map the product_id and department_id values to the their respective values (i.e., `number_of_orders`, `number_of_first_orders`, and `percentage`).

## Run instructions

You can run the test with the following command from within the `insight_testsuite` folder:

    insight_testsuite~$ ./run_tests.sh

On success, the output of `run_tests.sh` should look similar to

    [PASS]: test_1
    [Thu Mar 30 16:25:57 PDT 2017] 1 of 1 tests passed


On failure:

    [FAIL]: test_1
    [Thu Mar 30 16:28:01 PDT 2017] 0 of 1 tests passed
## Running the tests
## Limitations and future directions


Explain how to run the automated tests for this system

## Author

* [Brendon Jerome Butler](https://github.com/butlerbj)