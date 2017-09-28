all: setup run

setup:
    pip3 install --user python-amazon-simple-product-api
    pip3 install --user boto3
    pip3 install --user tabulate

run:
    python3 amazon_checker.py

