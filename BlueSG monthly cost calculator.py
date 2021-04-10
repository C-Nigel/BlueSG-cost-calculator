import pandas as pandas

file = pandas.read_excel(r"C:\Users\home\Desktop\history-2021-03-15-13-24-24.xlsx")
datesOfRental = pandas.to_datetime(file["Date"], dayfirst=True)
listOfCost = file["Amount invoiced"].astype(float)
month = datesOfRental[0].month
year = datesOfRental[0].year
totalCostForTheMonth = 0.00
costPerMonth = {}
counter = 0


def append_total_cost(totalCostForTheMonth, month, year):
    costPerMonth[str(month) + "/" + str(year)] = round(totalCostForTheMonth, 2)


while counter < len(datesOfRental):
    selectedDate = datesOfRental[counter]
    # Check if transaction falls within the same month and year
    if selectedDate.month == month and selectedDate.year == year:
        totalCostForTheMonth += listOfCost[counter]
        # Check if entry currently selected is the last entry
        if counter == len(datesOfRental):
            append_total_cost(totalCostForTheMonth, month, year)
    else:
        # Save the month and year with the cost associated with it,
        # reset the total cost for the month,
        # update month and year variable to the next record
        append_total_cost(totalCostForTheMonth, month, year)
        totalCostForTheMonth = 0.00
        month = datesOfRental[counter].month
        year = datesOfRental[counter].year
        counter -= 1
    counter += 1

# Print out the cost for every month
for k,v in costPerMonth.items():
    print(k, ": $", v)