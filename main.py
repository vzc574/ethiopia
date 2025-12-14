from bahire_hasab import get_bahire_hasab, to_gc
from constants import HOLIDAY_INFO, FIXED_HOLIDAYS

def main():
    print("Ethiopian Calendar & Bahire Hasab Console\n")
    
    # Ask user for Ethiopian year input
    while True:
        year_input = input("Enter Ethiopian year: ")
        if year_input.isdigit():
            year = int(year_input)
            break
        else:
            print("Invalid input! Please enter a number.")

    # Calculate Bahire Hasab
    bh = get_bahire_hasab(year)
    
    print(f"\nBahire Hasab for Ethiopian year {year}:")
    print(f"Metqi: {bh['metqi']}")
    print(f"Beale Metqi date: {bh['bealeMetqi']['date']} ({bh['bealeMetqi']['weekday']})")
    print(f"Nineveh date: {bh['nineveh']}")
    
    # Convert Nineveh date to Gregorian
    nineveh = bh['nineveh']
    gc = to_gc(nineveh['year'], nineveh['month'], nineveh['day'])
    print(f"Nineveh in Gregorian calendar: {gc}")

    # Show all holidays
    print(f"\n=== ALL HOLIDAYS FOR ETHIOPIAN YEAR {year} ===")
    
    # Fixed holidays
    print("\n--- FIXED HOLIDAYS ---")
    for key, info in FIXED_HOLIDAYS.items():
        holiday_info = HOLIDAY_INFO.get(key, {})
        name_amharic = holiday_info.get('name', {}).get('amharic', key)
        name_english = holiday_info.get('name', {}).get('english', key)
        description = holiday_info.get('description', {}).get('english', 'No description available')
        
        eth_date = {'year': year, 'month': info['month'], 'day': info['day']}
        gc_date = to_gc(year, info['month'], info['day'])
        
        print(f"{name_amharic} ({name_english})")
        print(f"  Ethiopian: {eth_date['month']}/{eth_date['day']}/{eth_date['year']}")
        print(f"  Gregorian: {gc_date.month}/{gc_date.day}/{gc_date.year}")
        print(f"  Description: {description}")
        print()

    # Movable holidays
    print("--- MOVABLE HOLIDAYS ---")
    for feast_key, feast_data in bh['movableFeasts'].items():
        name = feast_data.get('name', feast_key)
        eth_date = feast_data['ethiopian']
        gc_date = feast_data['gregorian']
        
        holiday_info = HOLIDAY_INFO.get(feast_key, {})
        description = holiday_info.get('description', {}).get('english', 'No description available')
        
        print(f"{name}")
        print(f"  Ethiopian: {eth_date['month']}/{eth_date['day']}/{eth_date['year']}")
        print(f"  Gregorian: {gc_date.month}/{gc_date.day}/{gc_date.year}")
        print(f"  Description: {description}")
        print()

if __name__ == "__main__":
    main()