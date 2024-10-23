from nepalicalender import get_nepali_details

details=get_nepali_details(2024,10,23)
for k,v in details.items():
    print(f"{k} : {v}")

details=get_nepali_details(2024,11,15)
for k,v in details.items():
    print(f"{k} : {v}")
    
details=get_nepali_details(2023,10,15)
for k,v in details.items():
    print(f"{k} : {v}")
    