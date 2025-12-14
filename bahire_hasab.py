from utils import validate_numeric_inputs, get_weekday
from day_arithmetic import add_days
from conversions import to_gc
from exceptions import UnknownHolidayError
from constants import (
    DAYS_OF_WEEK,
    EVANGELIST_NAMES,
    TEWSAK_MAP,
    MOVABLE_HOLIDAY_TEWSAK,
    KEY_TO_TEWSAK_MAP,
    HOLIDAY_INFO,
    MOVABLE_HOLIDAYS
)


def _calculate_bahire_hasab_base(ethiopian_year):
    """
    Calculates and returns all base values for the Bahire Hasab system. 
    This internal helper is the single source of truth for the core computational logic. 
    """
    
    # 1. Fixed Calculations
    amete_alem = 5500 + ethiopian_year  
    metene_rabiet = amete_alem // 4  
    
    # Evangelist (Matthew, Mark, Luke, John)
    evangelist_remainder = amete_alem % 4
    
    # 2. Medeb, Wenber, Abektie, Metqi (The 19-Year Cycle)
    medeb = amete_alem % 19  
    wenber = 18 if medeb == 0 else medeb - 1  
    abektie = (wenber * 11) % 30  
    metqi = (wenber * 19) % 30  

    # 3. New Year Day of the Week (Tinte Qemer)
    # The sum of Amete Alem and Metene Rabiet modulo 7 gives the weekday index (0=Sunday)
    tinte_qemer = (amete_alem + metene_rabiet) % 7
    # Convert index (0-6) to Amharic day name
    new_year_weekday = DAYS_OF_WEEK['amharic'][tinte_qemer]

    # 4. Beale Metqi Date and Weekday
    beale_metqi_month = 1 if metqi > 14 else 2  
    beale_metqi_day = metqi  
    beale_metqi_date = {'year': ethiopian_year, 'month': beale_metqi_month, 'day': beale_metqi_day}
    
    # Get the day name of the Beale Metqi date
    # NOTE: You need to ensure get_weekday returns the English day name for the TEWSAK_MAP to work!
    beale_metqi_weekday = get_weekday(beale_metqi_date['year'], beale_metqi_date['month'], beale_metqi_date['day'])

    # 5. Tewsak Calculation (The correction factor)
    # Tewsak is the number of days to add to Metqi to move its weekday to a Saturday
    # Note: Tewsak Map uses English names, assuming get_weekday returns English names.
    tewsak = TEWSAK_MAP.get(beale_metqi_weekday, 0)
    
    # 6. Fasika Base Calculation (The key final step)
    # The day index (0 to 30) for Fasika based on the lunar cycle
    fasika_day_index = (beale_metqi_day + tewsak) % 30
    if fasika_day_index == 0:
        fasika_day_index = 30 # Adjust 0 to 30 for the final day of the cycle

    # Tinte Fasika: The day of the month for Fasika on the Tinte Qemer cycle
    # (fasika_day_index + 15) adjusts for the fixed offset to get the correct day.
    tinte_fasika = (fasika_day_index + 15) % 7
    
    # 7. Final Base Values Result
    return {
        'ethiopian_year': ethiopian_year,
        'amete_alem': amete_alem,
        'metene_rabiet': metene_rabiet,
        'evangelist_remainder': evangelist_remainder,
        'tinte_qemer': tinte_qemer,
        'new_year_weekday': new_year_weekday,
        'medeb': medeb,
        'wenber': wenber,
        'abektie': abektie,
        'metqi': metqi,
        'beale_metqi_date': beale_metqi_date,
        'beale_metqi_weekday': beale_metqi_weekday,
        'tewsak': tewsak,
        'fasika_day_index': fasika_day_index,
        'tinte_fasika': tinte_fasika, # The numerical key to the Fasika date
    }
def get_bahire_hasab(ethiopian_year, lang='amharic'):
    
    """
    Calculates the full Bahire Hasab result for a given Ethiopian year.

    Args:
        ethiopian_year (int): The Ethiopian year (e.g., 2017).

    Returns:
        dict: A comprehensive dictionary containing all Bahire Hasab constants 
              and the dates of all movable feasts.
    """
    validate_numeric_inputs('get_bahire_hasab', ethiopian_year=ethiopian_year)
    
    # 1. Calculate Base Values
    base = _calculate_bahire_hasab_base(ethiopian_year)
    
    # 2. Calculate Fasika (Easter) - The main anchor
    fasika_date = _calculate_fasika_date(base)
    
    # 3. Calculate Movable Feasts (anchored to Fasika)
    movable_feasts = _calculate_movable_feasts(base, fasika_date)
    
    # 4. Prepare Evangelist name
    evangelist_name = EVANGELIST_NAMES[base['evangelist_remainder']]
    
    # 5. Format Movable Feasts for output (including Gregorian conversion)
    formatted_movable_feasts = {}
    for key, date in movable_feasts.items():
        formatted_movable_feasts[key] = {
            'ethiopian': date, 
            'gregorian': to_gc(date['year'], date['month'], date['day'])
        }

    return {
        'ameteAlem': base['amete_alem'],
        'meteneRabiet': base['metene_rabiet'],
        'evangelist': {'name': evangelist_name, 'remainder': base['evangelist_remainder']},
        'newYear': {'dayName': base['new_year_weekday'], 'tinteQemer': base['tinte_qemer']},
        'medeb': base['medeb'],
        'wenber': base['wenber'],
        'abektie': base['abektie'],
        'metqi': base['metqi'],
        'bealeMetqi': {'date': base['beale_metqi_date'], 'weekday': base['beale_metqi_weekday']},
        'tewsak': base['tewsak'],
        'fasikaDayIndex': base['fasika_day_index'],
        'tinteFasika': base['tinte_fasika'],
        'movableFeasts': formatted_movable_feasts
    }
 
def _calculate_fasika_date(base):
    """
    Calculates the exact Ethiopian date for Fasika (Easter) based on the base Bahire Hasab values.
    """
    # 1. Find Fasika Day of the Month (Miyazya or Ginbot)
    fasika_day = (base['fasika_day_index'] + base['tinte_qemer']) % 30
    if fasika_day == 0:
        fasika_day = 30
        
    # The final Fasika day is calculated by finding the Sunday after the full moon.
    # The Fasika formula results in a number that needs to be converted to a day of the week (Sunday)
    # The actual Fasika day is the next Sunday after the (fasika_day_index + tinte_qemer) offset.
    
    # We use the Tinte Fasika value (0-6) to find the day offset (0-6)
    fasika_weekday_offset = (base['tinte_fasika'] - base['tinte_qemer']) % 7
    if fasika_weekday_offset < 0:
        fasika_weekday_offset += 7
        
    # Now, find the actual Fasika date by adding the final offset to the Metqi date.
    # Fasika is always in Miazia (8) or Ginbot (9).
    # Since Beale Metqi is Meskerem/Tikimt, we can't just use add_days.
    
    # Correct Fasika Day Calculation:
    # Fasika always falls between Miazia 6 and Ginbot 5 (22nd of the 7th month to 5th of the 9th month)
    # The day is (Fasika_Day_Index + 15 + Tinte_Qemer) mod 30
    # Let's use the core calculation for the final Fasika Day in the 30-day lunar cycle:
    fasika_day_of_month = (base['fasika_day_index'] + 15 + base['tinte_qemer']) % 30
    if fasika_day_of_month == 0:
        fasika_day_of_month = 30

    # The result (fasika_day_of_month) is the day of the lunar cycle.
    # The final date is found by adjusting based on the Tinte Fasika index (0-6).
    
    # The total Fasika day number (from Meskerem 1) is:
    fasika_total_days = 202 + fasika_day_of_month + base['tinte_fasika']
    # The number 202 is the start of Miazia in a non-leap year (7 * 30 + 1)
    
    # Since your system has the 'add_days' utility, let's use it from a fixed starting point.
    
    # Fasika is always after Miazia 6. Let's start the count from Ginbot 5 (end of Fasika range)
    # The count (Yekut) is the number of days after Ginbot 5 (245th day of the year)
    # The fixed starting point for this system is Miyazya 1.
    
    # The core value of Fasika (Yekut) is:
    yekut = (base['fasika_day_index'] + base['tewsak']) % 30
    if yekut == 0:
        yekut = 30
        
    # Fasika Day in the Ethiopian Calendar is Miyazya 6 + yekut + (day_of_week_of_miyazya_6 - 1)
    # The fixed date for the start of the Fasika window (Miyazya 6) is the 216th day of the year (in a non-leap year)
    
    fasika_start_day = 216 # Miyazya 6
    
    # Calculate the number of days from Fasika_Start_Day to Fasika
    # The final day index is (yekut + tinte_fasika) mod 7
    # The number of days to add to Miyazya 6 is:
    
    fasika_days_to_add = (yekut + base['tinte_fasika'])
    
    # Convert this to an actual date using your existing add_days function
    start_date = {'year': base['ethiopian_year'], 'month': 8, 'day': 6} # Miyazya 6
    fasika_date = add_days(start_date, fasika_days_to_add)
    
    # Ensure the year is correct after the addition
    fasika_date['year'] = base['ethiopian_year']
    
    return fasika_date
def _calculate_movable_feasts(base, fasika_date):
    """
    Calculates all movable feasts by anchoring them to the Fasika date.
    
    Args:
        base (dict): The base Bahire Hasab values.
        fasika_date (dict): The calculated Ethiopian date for Fasika (Easter).

    Returns:
        dict: A dictionary of all movable feasts with their dates.
    """
    movable_feasts = {}
    
    # Fasika (Tinsaye) is the anchor
    movable_feasts['TINSAYE'] = fasika_date
    
    for key, days_offset in MOVABLE_HOLIDAY_TEWSAK.items():
        if key == 'TINSAYE':
            continue  # Already set
        
        # Use the add_days utility to calculate the new date
        date = add_days(fasika_date, days_offset)
        movable_feasts[key] = date
        
    return movable_feasts
bahire_hasab = get_bahire_hasab 