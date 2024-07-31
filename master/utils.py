import datetime

def date_hierarchy_drilldown(years_with_data, year_lookup=None, month_lookup=None):
    if year_lookup is None:
        unique_years = list({year['year_created'] for year in years_with_data})
        return [datetime.date(year, 1, 1) for year in unique_years]

    elif year_lookup is not None and month_lookup is None:
        months_with_data = {
            month['month_created']
            for month in years_with_data
            if month['year_created'] == year_lookup
        }
        return [datetime.date(year_lookup, month, 1) for month in months_with_data]

    return []
