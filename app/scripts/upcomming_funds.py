from datetime import datetime, timedelta
import calendar

total = int(raw_input('Current total: > '))
loan = 24041
income = 1045
two_week_expenses = 100 + 30 + 30 + 20
endofmonth_expenses = 400 + 280 + 29

today = datetime.now()
two_weeks = timedelta(days=14)

keep_going = True
paid_insurance = False
making_payment = False

print 'Today (%s) you have %d' % (today.strftime('%d %B'), total)

while keep_going:
    lastday = calendar.mdays[today.month]
    if today.month == 9 and not paid_insurance:
        total -= 450
        print 'You paid yearly car insurance this month (~$450).'
        paid_insurance = True
    if (lastday - 15) < today.day < lastday:
        total += (income - endofmonth_expenses)
        today += two_weeks
        loan -= 150
        print '\nOn %s you will have roughly $%d.' % (today.strftime('%B %d \'%y'), total)
        print '\nYour loan is approximately $%d.' % loan
        print 'You paid rent, loan, and utilities this period.'
        prompt = raw_input('\nContinue? [Yes] [No] [Make] Loan Payment > ').lower()
        if prompt == 'no':
            keep_going = False
        elif prompt == 'make':
            amount = int(raw_input('Amount to pay: > '))
            total -= amount
            loan -= amount
            print '\nYou\'re making a $%d payment on your student loan this month.' % amount
            print 'New total: %d\nApproximate Loan Size: %d.' % (total, loan)
        else:
            continue
    else:
        total += (income - two_week_expenses)
        today += two_weeks
        print '\nOn %s you will have roughly $%d.' % (today.strftime('%B %d \'%y'), total)
        prompt = raw_input('\nContinue? [Yes] [No] [Make] Loan Payment > ').lower()
        if prompt == 'no':
            keep_going = False
        elif prompt == 'make':
            amount = int(raw_input('Amount to pay: > '))
            total -= amount
            loan -= amount
            print '\nYou\'re making a $%d payment on your student loan this month.' % amount
            print 'New total: %d\nApproximate Loan Size: %d.' % (total, loan)
        else:
            continue
