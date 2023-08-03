import math as m
import sys

semi_annual_raise = 0.07
returnInterest = 0.04
downPayment = 0.25 * 1000000
totalMonths = 36

lowerBound = 0
higherBound = 10000

steps = 0

annual_salary = int(input('Enter the starting salary: '))

if 3 * annual_salary < downPayment:
        print('It is not possible to pay the down payment in three years.')
        sys.exit()

while True:
    steps = steps + 1
    pick = lowerBound + ((higherBound - lowerBound) / 2)
    pickFlt = pick / 10000

    savings = 0
    months = 0
    annual_salarytmp = annual_salary

    while True:
            if savings > downPayment: break
            months = months + 1
            savings = savings + (pickFlt * (annual_salarytmp / 12)) + (savings*returnInterest/12)
            if months % 6 == 0: annual_salarytmp = annual_salarytmp + (annual_salarytmp*semi_annual_raise)

    if months == totalMonths:
          print('Best savings rate:', pick / 10000)
          print('Steps in bisection search:', steps)
          break
    
    elif months > totalMonths: lowerBound = pick
    elif months < totalMonths: higherBound = pick

