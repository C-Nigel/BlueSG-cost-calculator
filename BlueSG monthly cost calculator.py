import pandas as pandas
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Location of excel file that contains all rental information
file = pandas.read_excel(
    r"C:\Users\Home\Desktop\python\BlueSG-cost-calculator\history-2021-07-10-11-51-36.xlsx"
)

# Input the start of your subscription date
startOfSubscriptionDate = "03/10/2020"

# Empty variables
# costPerMonth stores period of billing cycle as key, and totalInvoicedForTheMonth as value
totalInvoicedForTheMonth = 0.00
costPerMonth = {}
counter = 0

# List of rental dates and invoiced amount
datesOfRental = pandas.to_datetime(file["Date"], dayfirst=True)
invoicedCost = file["Amount invoiced"].astype(float)

# Get the next billing date
def nextBillingDate(subscriptionStartDate):
    subscriptionDate = datetime.strptime(subscriptionStartDate, "%d/%m/%Y")
    if datetime.now().day >= subscriptionDate.day:
        date = (
            str(subscriptionDate.day)
            + "/"
            + str(datetime.now().month)
            + "/"
            + str(datetime.now().year)
        )
        constructedDate = datetime.strptime(date, "%d/%m/%Y") + relativedelta(months=1)
        return constructedDate
    else:
        date = (
            str(subscriptionDate.day)
            + "/"
            + str(datetime.now().month)
            + "/"
            + str(datetime.now().year)
        )
        constructedDate = datetime.strptime(date, "%d/%m/%Y")
        return constructedDate


# Get the next previous billing date
def previousBillingDate(date):
    return date - relativedelta(months=1)


# Add billing period and total amount invoiced into costPerMonth list
def appendTotalCost(totalInvoicedForTheMonth, billingDate):
    costPerMonth[
        previousBillingDate(billingDate).date().strftime("%d/%m/%Y")
        + " - "
        + (billingDate.date() - relativedelta(days=1)).strftime("%d/%m/%Y")
    ] = round(totalInvoicedForTheMonth, 2)


# Main program

# Adds all invoiced amount that is within the selected billing cycle
billingDate = nextBillingDate(startOfSubscriptionDate)
while counter < len(datesOfRental):
    if billingDate > datesOfRental[counter] and datesOfRental[
        counter
    ] >= previousBillingDate(billingDate):
        totalInvoicedForTheMonth += invoicedCost[counter]
        if counter == len(datesOfRental) - 1:
            appendTotalCost(totalInvoicedForTheMonth, billingDate)
    else:
        appendTotalCost(totalInvoicedForTheMonth, billingDate)
        totalInvoicedForTheMonth = 0.00
        billingDate = previousBillingDate(billingDate)
        counter -= 1
    counter += 1

# Print out the cost for every month
for k, v in costPerMonth.items():
    print(k, ": $", v)
