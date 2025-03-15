import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for server-side rendering





def find_top_n_dominant(df, slider_value, selected_date, selected_options):

    # Convert date format
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').dt.strftime('%Y-%d-%m')

    if isinstance(selected_date, list):  # If it's a list (weekly)
        df = df[df['date'].isin(selected_date)]

        df = df.groupby('int_id', as_index=False).agg({
            'date': 'first',
            'Number_of_Hard_Brakes': 'sum',
            'Total_CO2': 'sum',
            'Number_of_Stops': 'sum',
            'Number_of_Vehicles': 'sum',
            'Average_Number_of_Hard_Brakes': 'mean',
            'Average_CO2': 'mean',
            'Average_Number_of_Stops': 'mean',
            'Total_length': 'first',
            'Latitude': 'first',
            'Longitude': 'first'
        })


    else:  # If it's a single date (daily)
        df = df[df['date'] == str(selected_date)]


    df = pd.DataFrame(df)
    df1 = df


    # Check if the filtered dataframe is empty
    if df.empty:
        df = []
        df1 = []
        print("No data on this day")
        # return {"error": "No data available for the selected date."}  # Return an error message
        return df, df1
     
    else:
        # You can proceed with further operations if data is found
        print("Data found for the selected date")

    n = int(slider_value)

    # Initialize x and y
    x, y = [], []

    if 'hardBrakes' in selected_options and 'emission' in selected_options:
        x = df['Average_Number_of_Hard_Brakes'].tolist()
        y = df['Average_CO2'].tolist()

    elif 'emission' in selected_options and 'numStops' in selected_options:
        x = df['Average_CO2'].tolist()
        y = df['Average_Number_of_Stops'].tolist()

    elif 'numStops' in selected_options and 'hardBrakes' in selected_options:
        x = df['Average_Number_of_Stops'].tolist()
        y = df['Average_Number_of_Hard_Brakes'].tolist()
  
    else:
        print("Invalid selection or missing values")


    # Assuming 'int_id' exists in the dataset
    lat = df['Latitude'].tolist()
    lon = df["Longitude"].tolist()
    int_id = df['int_id'].tolist()  # Use the existing 'int_id' column from the dataset


    dominant_points = []
    nondominant_points = []
    remaining_indices = set(range(len(x)))

    while len(dominant_points) < n and remaining_indices:
        new_dominant_points = []
        for i in remaining_indices:
            is_dominant = True
            for j in remaining_indices:
                if i != j:
                    if x[i] <= x[j] and y[i] <= y[j]:
                        is_dominant = False
                        break
            if is_dominant:
                new_dominant_points.append(i)

        for idx in new_dominant_points:
            if len(dominant_points) < n:
                dominant_points.append((int(df["int_id"].iloc[idx]), x[idx], y[idx], lat[idx], lon[idx]))
                remaining_indices.remove(idx)

    for i in remaining_indices:
        nondominant_points.append((int(df["int_id"].iloc[i]), x[i], y[i], lat[i], lon[i]))

    dominant_points.sort(key=lambda x: (x[1], x[2]))
    nondominant_points.sort(key=lambda x: (x[1], x[2]))



    return dominant_points, nondominant_points




def find_top_n_dominant_3d(df, slider_value, selected_date, selected_options):


    # # Attempt to parse date correctly
    # try:
    #     selected_date = pd.to_datetime(selected_date, format='%m/%d/%y').date()  # First, try MM/DD/YY
    # except ValueError:
    #     selected_date= pd.to_datetime(selected_date, format='%m/%d/%Y').date()  # If fails, try MM/DD/YYYY

    # Convert date format
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d').dt.strftime('%Y-%d-%m')


    # # Filter DataFrame using string comparison
    # df = df[df['date'] == str(selected_date)]

    


    if isinstance(selected_date, list):  # If it's a list (weekly)
        df = df[df['date'].isin(selected_date)]
     


        df = df.groupby('int_id', as_index=False).agg({
            'date': 'first',
            'Number_of_Hard_Brakes': 'sum',
            'Total_CO2': 'sum',
            'Number_of_Stops': 'sum',
            'Number_of_Vehicles': 'sum',
            'Average_Number_of_Hard_Brakes': 'mean',
            'Average_CO2': 'mean',
            'Average_Number_of_Stops': 'mean',
            'Total_length': 'first',
            'Latitude': 'first',
            'Longitude': 'first'

              # Keep the first date
        })


    else:  # If it's a single date (daily)
        df = df[df['date'] == str(selected_date)]



    df = pd.DataFrame(df)  
    df1 = df  

    # Check if the filtered dataframe is empty
    if df.empty:
        df = []
        df1 = []
        print("No data on this day")
        return df, df1
    
    else:
        # You can proceed with further operations if data is found
        print("Data found for the selected date")

    n = int(slider_value)

    # Assuming 'int_id' exists in the dataset
    x = df['Average_Number_of_Hard_Brakes'].tolist()
    y = df['Average_CO2'].tolist()
    z = df['Average_Number_of_Stops'].tolist()
    lat = df['Latitude'].tolist()
    lon = df["Longitude"].tolist()
    int_id = df['int_id'].tolist()  # Use the existing 'int_id' column from the dataset


    dominant_points = []
    nondominant_points = []
    remaining_indices = set(range(len(x)))
 
    while len(dominant_points) < n and remaining_indices:
        new_dominant_points = []
        for i in remaining_indices:
            is_dominant = True
            for j in remaining_indices:
                if i != j:
                    if x[i] <= x[j] and y[i] <= y[j] and z[i] <= z[j]:
                        is_dominant = False
                        break
            if is_dominant:
                new_dominant_points.append(i)

        for idx in new_dominant_points:
            if len(dominant_points) < n:
                dominant_points.append((int(df["int_id"].iloc[idx]), x[idx], y[idx], z[idx], lat[idx], lon[idx]))
                remaining_indices.remove(idx)

    for i in remaining_indices:
        nondominant_points.append((int(df["int_id"].iloc[i]), x[i], y[i], z[i], lat[i], lon[i]))

    dominant_points.sort(key=lambda x: (x[1], x[2], x[3]))
    nondominant_points.sort(key=lambda x: (x[1], x[2], x[3]))



    return dominant_points, nondominant_points

