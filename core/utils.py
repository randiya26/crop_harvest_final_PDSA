from datetime import date, datetime

def status_label(harvest_date):
    # convert to date if datetime
    if isinstance(harvest_date, datetime):
        harvest_date = harvest_date.date()
    today = date.today()
    diff = (harvest_date - today).days
    if diff <= 2:
        return "URGENT"
    elif diff <= 7:
        return "READY"
    else:
        return "NORMAL"