# Sales Report Generator

This project generates sales reports, including charts for the top 5 best-selling products, the number of orders each month, and the sales amount each month. Use postgres DB

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

## Introduction

The main purpose of this project is to provide insights into sales data by generating reports and charts. When given the `-r` or `--report` argument, the system will produce charts for the top 5 best-selling products, the number of orders each month, and the sales amount each month.

## Installation

To install and run the project, follow these steps:

Start the postgres server and set the valuse in db_settings.py

```bash
cd your-repository
pip install -r requirements.txt
python main.py -r
# or
python main.py --report
```

## Usage
1. Execute the project using the provided instructions in the Installation section.
2. Enter the customer code when prompted.
3. The system will generate charts displaying the number of purchases, purchase amounts, and the number of purchases for each product made by the specified customer in each month.


<!-- CONTACT -->
## Contact

Hasan Sadeghi - sadeghihasi@gmail.com

Project Link: [https://github.com/sadeghihasi](https://github.com/sadeghihasi)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
[github-url]: https://github.com/sadeghihasi
[linkedin-url]: https://linkedin.com/in/sadeghihasi
