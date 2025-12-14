from bahire_hasab import bahire_hasab

year = int(input("Enter Ethiopian Year: "))
result = bahire_hasab(year)

for k, v in result.items():
    print(f"{k}: {v}")
