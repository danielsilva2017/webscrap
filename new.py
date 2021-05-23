from csv import writer
import csv
import sys

import ast

from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

def main(): 
    
    url = sys.argv[1]
    driver.get(url)
    soup = BeautifulSoup(driver.page_source,'html.parser')
    price = soup.find('span',{'id': 'priceblock_ourprice'}).text.replace("\xa0€","")
    title = soup.find('span',{'id': 'productTitle'}).text.strip()

    save('prices.csv',title,price)
    priceIsLower('prices.csv',title)




def save(file,title,price):
    with open('prices.csv', 'a+', newline='') as csvfile:
        row =[title,price]
        writers = writer(csvfile)
        writers.writerow(row)

def priceIsLower(file,title):
    with open('prices.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_counter=0
        line_lower=0
        lower_price=0
        for row in csv_reader:
            row_price=float(row[1].replace(",","."))
            if row[0] == title:
                print("here")
                if lower_price==0:
                    lower_price=row_price
                    line_lower=line_counter
                if(row_price<float(lower_price)):
                    lower_price=row_price
                    line_lower=line_counter
            line_counter=line_counter+1
        print("The lower price is in line {line}".format(line=line_lower))


#Run

main()