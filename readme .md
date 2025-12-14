# Bahire Hasab - Ethiopian Calendar Calculator

## Table of Contents
- [Introduction](#introduction)
- [About the Ethiopian Calendar](#about-the-ethiopian-calendar)
- [What is Bahire Hasab?](#what-is-bahire-hasab)
- [Calendar Structure](#calendar-structure)
- [Key Concepts](#key-concepts)
- [Calculation Methods](#calculation-methods)
- [Conversion Formulas](#conversion-formulas)
- [Important Dates and Feasts](#important-dates-and-feasts)
- [Usage Examples](#usage-examples)
- [References](#references)

---

## Introduction

**Bahire Hasab** (ባሕረ ሃሳብ) is the traditional Ethiopian system of chronology and calendar calculation. The term literally means "Sea of Thought" or "Ocean of Knowledge" in Ge'ez, reflecting the depth and complexity of the calculations involved.

This system has been used for centuries by the Ethiopian Orthodox Tewahedo Church and the general population to determine:
- Religious feast days and fasting periods
- Easter (Fasika) dates
- Beginning of the year (Enkutatash)
- Conversion between Ethiopian and Gregorian calendars
- Agricultural seasons and planning

---

## About the Ethiopian Calendar

The Ethiopian Calendar (የኢትዮጵያ ዘመን አቆጣጠር) is the principal calendar used in Ethiopia and Eritrea. It is approximately **7-8 years behind** the Gregorian calendar.

### Key Characteristics:
- **13 months**: 12 months of 30 days each + 1 short month (Pagume) of 5-6 days
- **Year structure**: 365 days (366 in leap years)
- **New Year**: Meskerem 1 (September 11 or 12 in Gregorian calendar)
- **Leap year cycle**: Every 4 years (similar to Gregorian)

---

## What is Bahire Hasab?

Bahire Hasab is a complex computational system that includes:

1. **Abakte** (ዐባቅተ) - The Four Evangelists cycle
2. **Metke** (መትቅዕ) - The date of creation
3. **Wengelawi** (ወንጌላዊ) - The gospel reading cycle
4. **Tewsak** (ተዋሳክ) - The lunar cycle calculations
5. **Nenewe** (ነነዌ) - Calculation of Lent beginning
6. **Fasika** (ፋሲካ) - Easter calculation (most important)

---

## Calendar Structure

### The 13 Months

| # | Ethiopian Name | Days | Gregorian Equivalent |
|---|----------------|------|---------------------|
| 1 | Meskerem (መስከረም) | 30 | Sep 11 - Oct 10 |
| 2 | Tikimt (ጥቅምት) | 30 | Oct 11 - Nov 9 |
| 3 | Hidar (ኅዳር) | 30 | Nov 10 - Dec 9 |
| 4 | Tahsas (ታኅሣሥ) | 30 | Dec 10 - Jan 8 |
| 5 | Tir (ጥር) | 30 | Jan 9 - Feb 7 |
| 6 | Yekatit (የካቲት) | 30 | Feb 8 - Mar 9 |
| 7 | Megabit (መጋቢት) | 30 | Mar 10 - Apr 8 |
| 8 | Miazia (ሚያዝያ) | 30 | Apr 9 - May 8 |
| 9 | Ginbot (ግንቦት) | 30 | May 9 - Jun 7 |
| 10 | Sene (ሰኔ) | 30 | Jun 8 - Jul 7 |
| 11 | Hamle (ሐምሌ) | 30 | Jul 8 - Aug 6 |
| 12 | Nehase (ነሐሴ) | 30 | Aug 7 - Sep 5 |
| 13 | Pagume (ጳጉሜ) | 5/6* | Sep 6 - Sep 10/11 |

*6 days in leap years

---

## Key Concepts

### 1. Leap Year (Rub'e Amet - ርዑብ ዓመት)

The Ethiopian calendar leap year follows this rule:
- Every 4th year has 366 days (Pagume has 6 days)
- Leap years: when (Ethiopian Year + 1) ÷ 4 = whole number

**Example**: 
- 2015 EC: (2015 + 1) ÷ 4 = 504 → Leap Year ✓
- 2016 EC: (2016 + 1) ÷ 4 = 504.25 → Not Leap Year

### 2. Evangelists (Wengelawian - ወንጌላውያን)

Each year is associated with one of the Four Evangelists in rotation:
1. **Matthew** (ማቴዎስ) - Matewos
2. **Mark** (ማርቆስ) - Marqos
3. **Luke** (ሉቃስ) - Luqas
4. **John** (ዮሐንስ) - Yohannes

**Calculation**: (Ethiopian Year + 1) mod 4
- Remainder 0 = John (Leap Year)
- Remainder 1 = Matthew
- Remainder 2 = Mark
- Remainder 3 = Luke

### 3. Metke (መትቅዕ) - Era Calculation

Metke represents the year since the creation of the world according to Ethiopian Orthodox tradition.

**Formula**: Metke = Ethiopian Year + 5500

### 4. Tewsak (ተዋሳክ) - Lunar Calculations

Used to calculate the date of Easter and other moveable feasts.

**Tewsak Formula**:
```
Tewsak = (Metke × 19) mod 30
```

### 5. Abakte (ዐባቅተ)

The number used in Easter calculations, representing cycles of the moon.

**Abakte Formula**:
```
Abakte = (Metke × 11) mod 30
```

---

## Calculation Methods

### Easter (Fasika) Calculation

The most important calculation in Bahire Hasab. Easter always falls on a Sunday between Megabit 26 and Miyazya 30.

**Steps**:

1. **Calculate Metke**: Ethiopian Year + 5500
2. **Calculate Tewsak**: (Metke × 19) mod 30
3. **Calculate Abakte**: (Metke × 11) mod 30
4. **Determine Easter Month and Day** using complex tables

**Simplified Formula**:
```python
def calculate_easter(ethiopian_year):
    metke = ethiopian_year + 5500
    
    # Golden Number
    golden = (metke % 19) + 1
    
    # Tewsak
    tewsak = (metke * 19) % 30
    
    # Abakte
    abakte = (metke * 11) % 30
    
    # Easter calculation (simplified)
    # Full calculation requires additional tables
    # Easter falls between Megabit 26 - Miyazya 30
    
    return easter_month, easter_day
```

### Nenewe (ነነዌ) - Beginning of Lent

Nenewe (Jonah's Fast) begins exactly 70 days before Easter.

**Formula**: Easter Date - 70 days

### Hudade/Abiy Tsom (ሁዳዴ/ዐቢይ ጾም) - Great Lent

The Great Lent begins 55 days before Easter.

**Formula**: Easter Date - 55 days

### Debre Zeit (ደብረ ዘይት) - Mount of Olives

Begins 14 days before Easter (Palm Sunday week).

**Formula**: Easter Date - 14 days

---

## Conversion Formulas

### Ethiopian to Gregorian Conversion

```python
def ethiopian_to_gregorian(eth_year, eth_month, eth_day):
    # Ethiopian year in Gregorian calendar starts on Sep 11 (or Sep 12 in Gregorian leap year)
    
    # Calculate JDN (Julian Day Number)
    jdn = (
        (eth_year + 5500) // 4 +
        (eth_year * 1461 - 1) // 4 +
        (eth_month - 1) * 30 +
        eth_day +
        1723856 +
        2  # Adjustment for calendar difference
    )
    
    # Convert JDN to Gregorian
    # (Complex calculation involving Julian calendar transitions)
    
    return gregorian_year, gregorian_month, gregorian_day
```

### Gregorian to Ethiopian Conversion

```python
def gregorian_to_ethiopian(greg_year, greg_month, greg_day):
    # Calculate Julian Day Number for Gregorian date
    # Then convert to Ethiopian calendar
    
    # Simplified approach:
    # Ethiopian year is approximately Gregorian year - 7 or - 8
    
    if greg_month < 9 or (greg_month == 9 and greg_day <= 10):
        eth_year = greg_year - 8
    else:
        eth_year = greg_year - 7
    
    # Calculate day and month based on offset from Sep 11
    
    return eth_year, eth_month, eth_day
```

---

## Important Dates and Feasts

### Fixed Feasts (በዓላት)

| Feast | Ethiopian Date | Gregorian Equivalent |
|-------|----------------|---------------------|
| Enkutatash (New Year) | Meskerem 1 | Sep 11 |
| Meskel (Finding of True Cross) | Meskerem 17 | Sep 27 |
| Gena (Christmas) | Tahsas 29 | Jan 7 |
| Timket (Epiphany) | Tir 11 | Jan 19 |
| Kidus Yohannes (St. John) | Ginbot 2 | May 10 |
| Ledeta (Nativity) | Tahsas 29 | Jan 7 |

### Moveable Feasts (Dependent on Easter)

| Feast | Offset from Easter | Duration |
|-------|-------------------|----------|
| Nenewe (Jonah's Fast) | -70 days | 3 days |
| Hudade (Great Lent) | -55 days | 55 days |
| Debre Zeit (Palm Sunday) | -7 days | 1 week |
| Siklet (Crucifixion) | -3 days | Good Friday |
| Fasika (Easter) | 0 days | Sunday |
| Erget (Pentecost) | +50 days | Sunday |
| Tsome Hawaryat (Apostles' Fast) | +50 days | Variable |

---

## Usage Examples

### Example 1: Current Ethiopian Date

**Question**: What is today's Ethiopian date if today is December 14, 2025 (Gregorian)?

**Calculation**:
- December is before the Ethiopian new year transition
- Ethiopian Year = 2025 - 8 = 2017 EC
- Days from Sep 11, 2025 to Dec 14, 2025 = 94 days
- 94 days = 3 months (90 days) + 4 days
- Result: **Tahsas 4, 2017 EC**

### Example 2: Is 2016 EC a Leap Year?

**Calculation**:
- (2016 + 1) ÷ 4 = 2017 ÷ 4 = 504.25
- Not a whole number → **Not a Leap Year**
- Pagume will have 5 days

### Example 3: Which Evangelist for 2017 EC?

**Calculation**:
- (2017 + 1) mod 4 = 2018 mod 4 = 2
- Remainder 2 = **Mark (Marqos)**

### Example 4: Calculate Metke for 2017 EC

**Calculation**:
- Metke = 2017 + 5500 = **7517**

---

## Fasting Periods (ጾማት)

The Ethiopian Orthodox Church observes numerous fasting periods:

### Major Fasts:

1. **Tsome Hudade** (Great Lent) - 55 days before Easter
2. **Tsome Filseta** (Assumption Fast) - 1-16 Nehase (Aug 7-22)
3. **Tsome Hawaryat** (Apostles' Fast) - Variable length, ends Hamle 5
4. **Tsome Nenewe** (Jonah's Fast) - 3 days, 70 days before Easter
5. **Tsome Gena** (Advent Fast) - 40 days before Christmas

### Weekly Fasts:
- **Wednesday and Friday** - Throughout the year (except Easter season)

---

## Technical Implementation Notes

### Data Structures Needed:

```python
# Month names
ETHIOPIAN_MONTHS = [
    "Meskerem", "Tikimt", "Hidar", "Tahsas", "Tir", "Yekatit",
    "Megabit", "Miazia", "Ginbot", "Sene", "Hamle", "Nehase", "Pagume"
]

# Days in each month
DAYS_IN_MONTH = [30] * 12 + [5]  # Pagume has 5 (6 in leap year)

# Evangelists
EVANGELISTS = ["Yohannes", "Matewos", "Marqos", "Luqas"]
```

### Key Functions to Implement:

```python
1. is_leap_year(ethiopian_year)
2. get_evangelist(ethiopian_year)
3. calculate_metke(ethiopian_year)
4. calculate_tewsak(ethiopian_year)
5. calculate_abakte(ethiopian_year)
6. calculate_easter(ethiopian_year)
7. ethiopian_to_gregorian(year, month, day)
8. gregorian_to_ethiopian(year, month, day)
9. get_feast_days(ethiopian_year)
10. calculate_fasting_periods(ethiopian_year)
```

---

## References and Resources

### Historical Sources:
- Traditional Bahire Hasab manuscripts from Ethiopian Orthodox monasteries
- Ge'ez astronomical texts
- Church calculation tables (Metsehafe Bahire Hasab)

### Academic References:
- Otto Neugebauer - "Ethiopic Easter Computus"
- Ethiopian Orthodox Tewahedo Church Calendar Publications
- Institute of Ethiopian Studies archives

### Online Resources:
- Ethiopian Calendar Research Institute
- Ethiopian Orthodox Tewahedo Church Official Calendar
- Academic papers on Ethiopian chronology

---

## Cultural Significance

Bahire Hasab represents:
- **Religious devotion**: Ensuring proper observance of feasts and fasts
- **Cultural identity**: Maintaining Ethiopian chronological independence
- **Scientific knowledge**: Ancient astronomical and mathematical understanding
- **Agricultural planning**: Aligning farming with seasonal cycles
- **Community coordination**: Synchronizing celebrations across Ethiopia

---

## Notes for Developers

### Challenges in Implementation:

1. **Easter Calculation Complexity**: Full Bahire Hasab Easter calculation requires extensive lookup tables
2. **Leap Year Alignment**: Ethiopian and Gregorian leap years don't always align
3. **Date Conversion Edge Cases**: Transitions between calendars require careful handling
4. **Time Zone Considerations**: Ethiopia uses a different time system (12-hour shift)
5. **Localization**: Proper display of Ge'ez numerals and Amharic text

### Best Practices:

- Use well-tested libraries for date conversions
- Validate all inputs (year, month, day ranges)
- Handle Pagume month specially (5 or 6 days)
- Cache Easter calculations (they're computationally expensive)
- Provide both Amharic and English interfaces
- Include cultural context and explanations

---

## Version History

- **v1.0** - Initial documentation
- Comprehensive coverage of Bahire Hasab principles
- Conversion formulas and examples
- Implementation guidance

---

## License

This documentation is provided for educational and cultural preservation purposes.

---

## Contributing

Contributions to improve the accuracy and completeness of this documentation are welcome. Please ensure all information aligns with traditional Ethiopian Orthodox Tewahedo Church teachings and established historical sources.

---

## Contact

For questions, corrections, or additional information about Bahire Hasab and the Ethiopian Calendar system, please consult with Ethiopian Orthodox Church scholars and cultural institutions.

---

**ባሕረ ሃሳብ - የእውቀት ባሕር**  
*"The Ocean of Knowledge lives on in the digital age"*

