import requests
import database
# url = "https://latest-mutual-fund-nav.p.rapidapi.com/latest"

# querystring = {"Scheme_Type":"Open"}

# headers = {
# 	"x-rapidapi-key": "f6711bb0d1msh75232968387d53fp10f9f9jsne6ef58618152",
# 	"x-rapidapi-host": "latest-mutual-fund-nav.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# response=response.json()




# fund_family=set()
# for scheme in response:
#     fund_family.add(scheme['Mutual_Fund_Family'])
# print(fund_family)



# open_ended_schemes=[]
# for scheme in response:
#     if scheme['Scheme_Type']=='Open Ended Schemes':
#         open_ended_schemes.append(scheme)
# print(len(open_ended_schemes))

from test1 import mock_response
respone=mock_response
print(respone)
for scheme in respone:
    database.insert_fund_family_details(str(scheme['Scheme_Code']),scheme['Scheme_Name'],scheme['Net_Asset_Value'],scheme['Scheme_Type'],scheme['Mutual_Fund_Family'])
    

