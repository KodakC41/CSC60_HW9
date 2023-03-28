# https://aqs.epa.gov/data/api/signup?email=myemail@example.com

import json
import requests
import pandas as pd
from matplotlib import pyplot as plt

stateIDs = ["26",  "36",  "12",  "24",  "06",  "25"]
countIDs = ["163", "001", "001", "005", "037", "025"]

# Wastes of time: 26, 15, 

# Ozone (code: 44201)
# PM10 Total 0-10µm STP (code: 81102)
# Lead PM10 LC FRM/FEM (code: 85129)
# PM2.5 - Local Conditions (code: 88101)

variables = ["44201", "81102", "85129", "88101"]  # Data Roulette

email     = "christopher.j.bruinsma@outlook.com"  # Email

password  = "coppercrane89" # private key

# Used for the monthly information collection
StartDate = "20210101" 
EndDate   = "20210228"

# Quartly Starts and Ends
# Quarter 1
Q1     = "20210101"
Q1_end = "20210331"
# Quarter 2
Q2     = "20210401"
Q2_end = "20210630"
# Quarter 3
Q3     = "20210701"
Q3_end = "20210730"
# Quarter 4
Q4     = "20211001"
Q4_end = "20211231"
# Arrays of quarterly starts and ends
starts = [Q1,Q2,Q3,Q4]
ends   = [Q1_end,Q2_end,Q3_end,Q4_end]

# Get all States and their associated codes. 
def GetStates():
    api_url = "https://aqs.epa.gov/data/api/list/states?email={email}&key={password}".format(
        email=email, password=password)
    response = requests.get(api_url)
    json_object = json.dumps(response.json(), indent=4)
    with open("AllStates.json", "w") as outfile:
        outfile.write(json_object)

# Get the info on each state, this is useful for finding county information and writing out a JSON file 
def getStateInfo():
    for state in stateIDs:
        api_url = "https://aqs.epa.gov/data/api/list/countiesByState?email={email}&key={password}&state={id}".format(
            email=email, password=password, id=state)
        response = requests.get(api_url)
        json_object = json.dumps(response.json(), indent=4)
        with open("stateID{i}.json".format(i=state), "w") as outfile:
            outfile.write(json_object)

# Get the needed data from each county per state over the monthly timeframe and write out a JSON file 
def getClimateInfo():
    for i in range(len(stateIDs)):
        for v in variables:
            api_url = "https://aqs.epa.gov/data/api/sampleData/byCounty?email={em}&key={password}&param={code1}&bdate={start}&edate={end}&state={id}&county={c_id}".format(
                id=stateIDs[i], c_id=countIDs[i], code1=v, start=StartDate, end=EndDate, password=password, em=email)
            response = requests.get(api_url)
            json_object = json.dumps(response.json(), indent=4)
            with open("ClimateData{i}_{v}.json".format(i=stateIDs[i],v=v), "w") as outfile:
                outfile.write(json_object)

# Get the quarterly environmental data and write out an associated data. 
def getQuarterlyInfo():
    for i in range(len(stateIDs)):
        for q in range(len(starts)):
             for v in variables:
                api_url = "https://aqs.epa.gov/data/api/sampleData/byCounty?email={em}&key={password}&param={code1}&bdate={start}&edate={end}&state={id}&county={c_id}".format(
                    id=stateIDs[i], c_id=countIDs[i], code1 = v, start=starts[q], end=ends[q], password=password, em=email)
                response = requests.get(api_url)
                json_object = json.dumps(response.json(), indent=4)
                with open("ClimateData{i}_Q{q}_{v}.json".format(i=stateIDs[i],q=q,v=v), "w") as outfile:
                    outfile.write(json_object)

# # Plotting stuff
# # Set the figure size
# plt.rcParams["figure.figsize"] = [7.00, 3.50]
# plt.rcParams["figure.autolayout"] = True

# # Make a list of columns
# columns = ['Data/date_local','Data/sample_measurement']
# # Read a CSV file
# df = pd.read_csv("/Users/chris/Documents/UR/SENIOR/FinalSemester/CSC260/HW9/ClimateData12_Month_Ozone.csv", usecols=columns)
# df1 = pd.read_csv("/Users/chris/Documents/UR/SENIOR/FinalSemester/CSC260/HW9/ClimateData12_Month.csv", usecols=columns)
# # Plot the lines
# plt.plot(df)
# plt.plot(df1)
# plt.show()

# GetStates()
# getStateInfo()
getClimateInfo()
getQuarterlyInfo()


