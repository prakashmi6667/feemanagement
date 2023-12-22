from django import template
from django.utils.html import format_html
from calendar import monthrange

register = template.Library()


def days(month, year):
    try:
        print(monthrange(year, month)[1])
        td = ''
        total = monthrange(year, month)[1]+1
        for i in range(1, total):
            td += '<th>'+str(i)+'</th>'

        return td
    except Exception as ex:
        print(ex)
        return ""


def Studentdays(month, year):
    try:
        total = monthrange(year, month)[1]+1
        return total
    except Exception as ex:
        print(ex)
        return ""


def Studentdays_to_td(total, st):
    try:
        td = ''
        for i in range(1, total):
            if i <= 9:
                day = '0'+str(i)
            else:
                day = str(i)
            td += '<td data-id="'+str(st)+'" data-day="'+day+'" ></td>'

        return td
    except Exception as ex:
        print(ex)
        return ""


def is_ttMatched(id, id1):
    try:
        if int(id) == int(id1):
            print(id, id1)
            return True
        else:
            return False
    except Exception as ex:
        print(ex)
        return ""


register.filter('days', days)
register.filter('Studentdays', Studentdays)
register.filter('Studentdays_to_td', Studentdays_to_td)
register.filter('is_ttMatched', is_ttMatched)
