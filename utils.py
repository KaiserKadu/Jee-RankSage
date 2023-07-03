import pandas as pd
import numpy as np
import plotly.express as px



def get_df(year,exam):
    if(year == 2016 and exam == "Jee Mains"):
        df = pd.read_csv('data/2016/Mains.csv')
        return df            
    elif(year == 2016 and exam == "Jee Advanced"):
        df = pd.read_csv('data/2016/Adv.csv')
        return df
    elif(year == 2017 and exam == "Jee Mains"):
        df = pd.read_csv('data/2017/Mains.csv')
        return df  
    elif(year == 2017 and exam == "Jee Advanced"):
        df = pd.read_csv('data/2017/Adv.csv')
        return df  
    elif(year == 2018 and exam == "Jee Mains"):
        df = pd.read_csv('data/2018/Mains.csv')
        return df  
    elif(year == 2018 and exam == "Jee Advanced"):
        df = pd.read_csv('data/2018/Adv.csv')
        return df  
    elif(year == 2019 and exam == "Jee Mains"):
        df = pd.read_csv('data/2019/Mains.csv')
        return df  
    elif(year == 2019 and exam == "Jee Advanced"):
        df = pd.read_csv('data/2019/Adv.csv')
        return df  
    elif(year == 2020 and exam == "Jee Mains"):
        df = pd.read_csv('data/2020/Mains.csv')
        return df  
    elif(year == 2020 and exam == "Jee Advanced"):
        df = pd.read_csv('data/2020/Adv.csv')
        return df  
    elif(year == 2021 and exam == "Jee Mains"):
        df = pd.read_csv('data/2021/Mains.csv')
        return df  
    elif(year == 2021 and exam == "Jee Advanced"):
        df = pd.read_csv('data/2021/Adv.csv')
        return df  
    elif(year == 2022 and exam == "Jee Mains"):
        df = pd.read_csv('data/2022/Mains.csv')
        return df  
    elif(year == 2022 and exam == "Jee Advanced"):
        df = pd.read_csv('data/2022/Adv.csv')
        return df  
    
  
def get_institutes(df,all = False):
    list =  df["Institute"].unique().tolist()
    if all:
        list.insert(0   , "All")
    return list

def get_programs(df,all = False):
    list =  df["Academic Program Name"].unique().tolist()
    if all:
        list.insert(0   , "All")
    return list

def get_quota(df,all = False):
    list =  df["Quota"].unique().tolist()
    if all:
        list.insert(0   , "All")
    return list
    

def get_seatType(df,all = False):
    list = df["Seat Type"].unique().tolist()
    if all:
        list.insert(0   , "All")
    return list


def get_gender(df,all = False):
    list =  df["Gender"].unique().tolist()
    if all:
        list.insert(0   , "All")
    return list

def check_string_present(string, string_list):
    if string in string_list:
        return False
    else:
        return True

def apply_filters( df,institutes, academic_programs, quota, seatType, gender, rank):
    data = df
    # Filter by institutes
    if check_string_present('All', institutes):
        data = data[data['Institute'].isin(institutes)]

    # Filter by academic programs
    if check_string_present('All', academic_programs):
        data = data[data['Academic Program Name'].isin(academic_programs)]

    # Filter by quota
    if quota != "All":
        data = data[data['Quota'] == quota]

    # Filter by seat type
    if seatType != "All":
        data = data[data['Seat Type'] == seatType]

    # Filter by gender
    if gender != "All":
        data = data[data['Gender'] == gender]

    # Filter by rank
    if rank != 0:
        data = data[data['Closing Rank'] >= rank]

    return data

def plotter_program(df):
    selected_row = df.iloc[0]

    # Extract the years and closing ranks
    years = ['2016', '2017', '2018', '2019', '2020', '2022']
    closing_ranks = selected_row[['CR2016', 'CR2017', 'CR2018', 'CR2019', 'CR2020', 'CR2022']].values
    #title = 'Closing Ranks from 2016 to 2022'title +" for \n" 
    title =  selected_row['Institute'] + ' - ' + selected_row['Academic Program Name']+'('+selected_row['Seat Type']+' - '+ selected_row['Gender'] +	')'
    

    # Create a Plotly line plot
    fig = px.line(x=years, y=closing_ranks, color=px.Constant("Trend"),title = title, markers = True,
             labels=dict(x="Year", y="Closing Rank", color="Legend"))
    fig.update_traces(line_color='#7f2ccb')
    fig.update_traces(marker_color='#F0EB8D')
    return fig

def plotter_institute(df,title = None):
    result = df.iloc[:,6:]
    result =pd.DataFrame(result)
    years = ['2016', '2017', '2018', '2019', '2020', '2022']
    fig = px.line(x=years, y=result.iloc[0].values,markers = True,color=px.Constant(df.iloc[0,2]),labels=dict(x="Year", y="Closing Rank", color="Programs"),title=title)
    for i in range(1,len(result)):
        arr = result.iloc[i]
        fig.add_scatter(x=years, y=arr ,name = df.iloc[i,2][:60])
    return fig