from datetime import date, timedelta

URL = "https://www.easyfuture.pt/artigos"
DATA_ID_HEADER = 'pgi'
MONTHS = {
    'jan.': 1,
    'fev.': 2,
    'mar.': 3,
    'abr.': 4,
    'mai.': 5,
    'jun.': 6,
    'jul.': 7,
    'ago.': 8,
    'set.': 9,
    'out.': 10,
    'nov.': 11,
    'dez.': 12
}

def parse_date(post_date):
    #current_date = 
    post_date = post_date.split()
    parsed_date = date.today()

    # Check if date includes year
    if (len(post_date) == 3):
        # Check if it is in format 'há dd dias' or in 'dd de mmm.'
        if (post_date[0].isdigit()):
            day = int(post_date[0])
            month = MONTHS[post_date[2]]
            year = parsed_date.year
            parsed_date = date(day=day, month=month, year=year)
        else:
            days = int(post_date[1])
            parsed_date = parsed_date - timedelta(days=days)
    else:
        day = int(post_date[0])
        month = MONTHS[post_date[2]]
        year = int(post_date[4])
        parsed_date = date(day=day, month=month, year=year)

    return parsed_date