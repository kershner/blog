from datetime import datetime, timedelta
import calendar

total = int(raw_input('Current total: > '))
loan = 23896
income = 1060
two_week_expenses = 100 + 45 + 50  # Food, Gas, Misc
endofmonth_expenses = 400 + 29  # Rent, internet

today = datetime.now()
two_weeks = timedelta(days=14)

keep_going = True
paid_insurance = False
making_payment = False

print '\nToday (%s) you have $%d.' % (today.strftime('%d %B'), total)

while keep_going:
    lastday = calendar.mdays[today.month]
    if today.month == 9 and not paid_insurance:
        total -= 450
        print '\nYou paid yearly car insurance this month (~$450).'
        paid_insurance = True
    if today.month == 10:
        paid_insurance = False
    if (lastday - 15) < today.day < lastday:
        total += (income - endofmonth_expenses)
        today += two_weeks
        if loan:
            loan -= 150
            total -= 280
            print '\nYour loan is approximately $%d.' % loan
            print '\nYou paid rent, loan, and utilities this period.'
        else:
            print '\nYou paid your rent and utilities this period.'
        print '\nOn %s you will have roughly $%d.' % (today.strftime('%B %d \'%y'), total)
        if loan:
            prompt = raw_input('Continue? [Yes] [No] [Make] Loan Payment > ').lower()
        else:
            prompt = raw_input('Continue? [Yes] [No] > ').lower()
        if prompt == 'no':
            keep_going = False
        elif prompt == 'make':
            amount = int(raw_input('Amount to pay: > '))
            total -= amount
            loan -= amount
            print '\nYou\'re making a $%d payment on your student loan this month.' % amount
            print '\nNew total: $%d\nApproximate Loan Size: %d.' % (total, loan)
        else:
            continue
    else:
        total += (income - two_week_expenses)
        today += two_weeks
        print '\nOn %s you will have roughly $%d.' % (today.strftime('%B %d \'%y'), total)
        if loan:
            prompt = raw_input('Continue? [Yes] [No] [Make] Loan Payment > ').lower()
        else:
            prompt = raw_input('Continue? [Yes] [No] > ').lower()
        if prompt == 'no':
            keep_going = False
        elif prompt == 'make':
            amount = int(raw_input('Amount to pay: > '))
            total -= amount
            loan -= amount
            print '\nYou\'re making a $%d payment on your student loan this month.' % amount
            print 'New total: $%d\nApproximate Loan Size: %d.' % (total, loan)
        else:
            continue