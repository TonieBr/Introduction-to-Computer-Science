import math as m

annual_salary = int(input('Enter your annual salary: '))
portion_saved = float(input('Enter the percent of your salary to save, as a decimal: '))
total_cost = int(input('Enter the cost of your dream home: '))
semi_annual_raise = float(input('Enter the semi-annual raise, as a decimal: '))

savings = 0
portion_down_payment = 0.25
months = 0

downPayment = 0.25 * total_cost

while True:
    if savings > downPayment: break

    months = months + 1
    savings = savings + (portion_saved * (annual_salary / 12)) + (savings*0.04/12)

    if months % 6 == 0: annual_salary = annual_salary + (annual_salary*semi_annual_raise)

print('Number of months:', months)


