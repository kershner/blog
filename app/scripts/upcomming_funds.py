from datetime import datetime, timedelta
import calendar

total = int(raw_input('Current total: > '))
loan = 24041
income = 1080
two_week_expenses = 100 + 30 + 30 + 20
endofmonth_expenses = 400 + 29

today = datetime.now()
two_weeks = timedelta(days=14)

keep_going = True
paid_insurance = False
making_payment = False

print 'Today (%s) you have $%d.' % (today.strftime('%d %B'), total)

while keep_going:
    lastday = calendar.mdays[today.month]
    if today.month == 9 and not paid_insurance:
        total -= 450
        print 'You paid yearly car insurance this month (~$450).'
        paid_insurance = True
    if today.month == 10:
        paid_insurance = False
    if (lastday - 15) < today.day < lastday:
        total += (income - endofmonth_expenses)
        today += two_weeks
        if loan:
            loan -= 150
            total -= 280
            print 'Your loan is approximately $%d.' % loan
            print 'You paid rent, loan, and utilities this period.'
        else:
            print 'You paid your rent and utilities this period.'
        print 'On %s you will have roughly $%d.' % (today.strftime('%B %d \'%y'), total)
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
            print 'You\'re making a $%d payment on your student loan this month.' % amount
            print 'New total: %d\nApproximate Loan Size: %d.' % (total, loan)
        else:
            continue
    else:
        total += (income - two_week_expenses)
        today += two_weeks
        print 'On %s you will have roughly $%d.' % (today.strftime('%B %d \'%y'), total)
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
            print 'You\'re making a $%d payment on your student loan this month.' % amount
            print 'New total: %d\nApproximate Loan Size: %d.' % (total, loan)
        else:
            continue