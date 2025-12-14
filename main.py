from bahire_hasab import get_bahire_hasab
from constants import MONTH_NAMES, FIXED_HOLIDAYS, HOLIDAY_INFO
from conversions import to_gc
from exceptions import InvalidEthiopianDateError


def main():
    try:
        # 1. የዓመት እና የወር ግቤት መቀበል
        year = int(input("Enter Ethiopian Year: "))
        month = int(input("Enter Ethiopian Month Number (1=Meskerem to 13=Pagume): "))
        
        # የወር ቁጥሩን ማረጋገጥ
        if not 1 <= month <= 13:
            raise InvalidEthiopianDateError(year, month, 1)

        selected_month_amharic = MONTH_NAMES['amharic'][month - 1]
        
        print(f"\n--- በዓላት በ{selected_month_amharic} {year} ዓ.ም ---")
        print("--------------------------------------------------")

        all_holidays = []
        
        # 2. ተንቀሳቃሽ በዓላትን ማግኘት (ከባሕረ ሃሳብ ስሌት)
        # get_bahire_hasab ስሌቱን ያከናውናል
        result = get_bahire_hasab(year)
        
        for feast_key, feast_data in result['movableFeasts'].items():
            if feast_data['ethiopian']['month'] == month:
                # በዓሉን ለህትመት ማዘጋጀት
                holiday_name = HOLIDAY_INFO.get(feast_key, {}).get('name', {}).get('amharic', feast_key)
                
                all_holidays.append({
                    'name': holiday_name,
                    'ethiopian': feast_data['ethiopian'],
                    'gregorian': feast_data['gregorian'],
                    'type': 'ተንቀሳቃሽ'
                })

        # 3. ቋሚ በዓላትን ማግኘት (ከconstants.py ዝርዝር)
        for key, info in FIXED_HOLIDAYS.items():
            fixed_month = info['month']
            
            if fixed_month == month:
                eth_date = {'year': year, 'month': fixed_month, 'day': info['day']}
                
                # የዓሉን የአማርኛ ስም ከHOLIDAY_INFO መውሰድ
                holiday_name = HOLIDAY_INFO.get(key, {}).get('name', {}).get('amharic', key)
                
                all_holidays.append({
                    'name': holiday_name,
                    'ethiopian': eth_date,
                    'gregorian': to_gc(year, fixed_month, info['day']),
                    'type': 'ቋሚ'
                })
                
        # 4. በዓላትን በቀን ተራ ማተም
        all_holidays.sort(key=lambda x: x['ethiopian']['day'])
        
        if not all_holidays:
            print(f"በ{selected_month_amharic} ወር ውስጥ በዓል አልተገኘም።")
            
        for holiday in all_holidays:
            eth_date = holiday['ethiopian']
            gc_date = holiday['gregorian']
            
            # ቀለል ያለና ግልጽ የሆነ ውፅዓት
            print(f"  {holiday['name']} ({holiday['type']}):")
            print(f"    - የኢትዮጵያ ቀን: {selected_month_amharic} {eth_date['day']}, {eth_date['year']}")
            print(f"    - የጎርጎርያን ቀን: {gc_date}")
            print()
                
    except InvalidEthiopianDateError as e:
        print(f"\nError: {e}")
    except ValueError:
        print("\nInvalid input. Please enter a valid number for both the year and the month.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()