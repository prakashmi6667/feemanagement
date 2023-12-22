from django import template
from django.utils.html import format_html

register = template.Library()


def course(crs, franchise_id):
    try:
        if crs:
            for dt in crs:
                
                if dt.franchise_id == franchise_id:
                    # print(dt.course, dt.franchise_id)
                    return dt.fee
        else:
            return 0.00
        # print(crs, franchise_id)
        return 0.00
    except Exception as ex:
        print(ex)
        return "---"

register.filter('course', course)
