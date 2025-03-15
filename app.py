from flask import Flask, render_template, send_from_directory
import pandas as pd
import folium
import os
from flask import Flask, request, jsonify
from Paretofronts import find_top_n_dominant_3d, find_top_n_dominant
import datetime  
import matplotlib.pyplot as plt
from flask import Flask, request, send_file, jsonify
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)

# Folder to store the map HTML file
MAPS_DIR = 'static/maps'
os.makedirs(MAPS_DIR, exist_ok=True)  # Ensure the directory exists


result = None
markers = None

# Define the static maps directory
MAPS_DIR = os.path.join('static', 'maps')
os.makedirs(MAPS_DIR, exist_ok=True)  # Ensure the directory exists



# Load CSV into memory (on app startup)
df = pd.read_csv(r'data\hardbrake.csv')

# Convert date and time columns to datetime for fast filtering
df['date'] = pd.to_datetime(df.iloc[:, 2], format='%m/%d/%Y').dt.date
df['time'] = pd.to_datetime(df.iloc[:, 3], format='%H:%M:%S').dt.hour  # Extract hour only




@app.route('/')
def default():
    # Define map centered on San Antonio, Texas
    map_center = [29.4241, -98.4936]
    m = folium.Map(location=map_center, zoom_start=12)

    # Save the map in the static/maps directory
    map_filename = os.path.join(MAPS_DIR, 'map.html')
    m.save(map_filename)

    return render_template('index.html', map_url='/static/maps/map.html')


# @app.route('/map')
# def show_map():
#     global result

#     # Define map centered on San Antonio, Texas
#     map_center = [29.4241, -98.4936]
#     m = folium.Map(location=map_center, zoom_start=12)


#     # If result has data, add markers
#     if result:
#         for data in result:
#             lat, lon = data[3], data[4]  # Extract latitude and longitude
#             folium.Marker(
#                 location=[lat, lon],
#                 popup=f"Value: {data[0]}, Score: {data[1]:.4f}, Distance: {data[2]:.2f}",
#                 icon=folium.Icon(color="blue", icon="info-sign")
#             ).add_to(m)

#     # Save the map
#     map_html = os.path.join(MAPS_DIR, 'map.html')
#     m.save(map_html)

#     return render_template('index.html', map_url='/static/maps/marker_map.html')

# @app.route('/map')
# def show_map():
#     global result

#     if not result:
#         return jsonify({"status": "error", "message": "No data available"})

#     markers = [{"lat": data[3], "lon": data[4], "info": f"Value: {data[0]}, Score: {data[1]:.4f}, Distance: {data[2]:.2f}"} for data in result]

#     return jsonify({"status": "success", "markers": markers})



@app.route('/get_data', methods=['GET', 'POST'])
def get_data():
    global result 


    if request.method == 'POST':
        data = request.get_json()
        print("Received Data:", data)
        

        # Extract date from user input
        selected_date = data.get('date')  # Expected format: 'MM/DD/YY'
        selected_tab = str(data.get('selectedTab')) 
        slider_value = int(data.get('sliderValue'))
        selected_options = data.get('selectedCheckboxes')

        # Load data from CSV
        df = pd.read_csv(r'data\Data.csv')  # Read as string to avoid auto-parsing issues


        if selected_tab == '2D':
            dominant_points, nondominant_points = find_top_n_dominant(df, slider_value, selected_date, selected_options)

            # Check if the result contains data
            if not dominant_points and not nondominant_points:
                # If both are empty, return a message indicating no data
                return jsonify({"error": "No data available for the selected parameters."}), 400  # or 404 if not found


            else:
                result  = dominant_points
                # print(dominant_points)
                # print("hhahahaahahahhhhhhhhhhhhhhhhhhhhhhhhhh")
                # print(nondominant_points)

                ID_index, lat_index, lon_index = 0, 3, 4

                graph_file = ''

                if 'hardBrakes' in selected_options and 'emission' in selected_options:
                    Hardbrake_index, CO2_index = 1, 2
                    markers = [{"ID": row[ID_index],
                                "lat": row[lat_index],
                                "lon": row[lon_index],
                                "Average_Hardbrake": row[Hardbrake_index],
                                "Average_CO2": row[CO2_index]
                                } for row in result if len(row) > lon_index]
                    
                        
                    fig = plt.figure()
                    ax = fig.add_subplot()

                    plt.scatter([point[1] for point in dominant_points], 
                                [point[2] for point in dominant_points], 
                                c='red', label=f'Top {slider_value} Dominant Points')

                    plt.scatter([point[1] for point in nondominant_points], 
                                [point[2] for point in nondominant_points], 
                                c='blue', label='Non-Dominant Points')

                    plt.xlabel('Average Hard Brakes per Mile', fontsize=10)
                    plt.ylabel('Average CO2 per Mile', fontsize=10)
                    plt.title('Saftey Vs Energy', fontsize=10)
                    plt.legend()
                    plt.grid(True, color='black', linestyle='--', linewidth=0.5)
                    plt.xlim(left=0)

                    # Save the plot to the static/images directory
                    graph_file = 'static/images/Saftey_Vs_Energy.png'
                    plt.savefig(graph_file)
                    plt.close()

                    

                elif 'emission' in selected_options and 'numStops' in selected_options:
                    CO2_index, Stops_index = 1, 2
                    markers = [{"ID": row[ID_index],
                                "lat": row[lat_index],
                                "lon": row[lon_index],
                                "Average_CO2": row[CO2_index],
                                "Average_Stops": row[Stops_index]
                                } for row in result if len(row) > lon_index]
                    
                    fig = plt.figure()
                    ax = fig.add_subplot()

                    plt.scatter([point[1] for point in dominant_points], 
                                [point[2] for point in dominant_points], 
                                c='red', label=f'Top {slider_value} Dominant Points')

                    plt.scatter([point[1] for point in nondominant_points], 
                                [point[2] for point in nondominant_points], 
                                c='blue', label='Non-Dominant Points')

                    plt.xlabel('Average CO2 per Mile', fontsize=10)
                    plt.ylabel('Average Stops per Mile', fontsize=10)
                    plt.title('Energy Vs Mobility', fontsize=10)
                    plt.legend()
                    plt.grid(True, color='black', linestyle='--', linewidth=0.5)
                    plt.xlim(left=0)

                    # Set graph file path
                    graph_file = 'static/images/Energy_Vs_Mobility.png'
                    plt.savefig(graph_file)
                    plt.close()

                elif 'numStops' in selected_options and 'hardBrakes' in selected_options:
                    Stops_index, Hardbrake_index = 1, 2
                    markers = [{"ID": row[ID_index],
                                "lat": row[lat_index],
                                "lon": row[lon_index],
                                "Average_Stops": row[Stops_index],
                                "Average_Hardbrake": row[Hardbrake_index]
                                } for row in result if len(row) > lon_index]
                    
                    fig = plt.figure()
                    ax = fig.add_subplot()

                    plt.scatter([point[1] for point in dominant_points], 
                                [point[2] for point in dominant_points], 
                                c='red', label=f'Top {slider_value} Dominant Points')

                    plt.scatter([point[1] for point in nondominant_points], 
                                [point[2] for point in nondominant_points], 
                                c='blue', label='Non-Dominant Points')

                    plt.xlabel('Average Stops per Mile', fontsize=10)
                    plt.ylabel('Average Hard Brakes per Mile', fontsize=10)
                    plt.title('Mobility Vs Saftey', fontsize=10)
                    plt.legend()
                    plt.grid(True, color='black', linestyle='--', linewidth=0.5)
                    plt.xlim(left=0)

                    # Set graph file path
                    graph_file = 'static/images/Mobility_Vs_Saftey.png'
                    plt.savefig(graph_file)
                    plt.close()
                    

        if selected_tab == '3D':
            dominant_points, nondominant_points = find_top_n_dominant_3d(df, slider_value, selected_date, selected_options)

            # Check if the result contains data
            if not dominant_points and not nondominant_points:
                # If both are empty, return a message indicating no data
                return jsonify({"error": "No data available for the selected parameters."}), 400  # or 404 if not found

            else:
                result = dominant_points

                ID_index, Hardbrake_index, CO2_index, Stops_index, lat_index, lon_index = 0, 1, 2, 3, 4, 5 

                graph_file = ''
                
                
                # Extract lat/lon (3rd and 4th index in each row)
                markers = [{"ID": row[ID_index],
                        "lat": row[lat_index],
                        "lon": row[lon_index],
                        "Average_Hardbrake": row[Hardbrake_index],
                        "Average_CO2": row[CO2_index],
                        "Average_Stops": row[Stops_index]
                        } for row in result if len(row) > lon_index]
                

                # Create a figure and 3D axis
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')

                # Scatter plot for dominant points
                ax.scatter([point[1] for point in dominant_points], 
                        [point[2] for point in dominant_points], 
                        [point[3] for point in dominant_points], 
                        c='red', marker='^', label=f'Top {slider_value} Dominant Points')

                # Scatter plot for non-dominant points
                ax.scatter([point[1] for point in nondominant_points], 
                        [point[2] for point in nondominant_points], 
                        [point[3] for point in nondominant_points], 
                        c='blue', label='Non-Dominant Points')

                # Set axis labels with font properties
                ax.set_xlabel('Average Number of Hard Brakes per mile', family='serif', fontsize=11, weight='bold', fontname='Times New Roman')
                ax.set_ylabel('Average CO2 per mile', family='serif', fontsize=11, weight='bold', fontname='Times New Roman')
                ax.set_zlabel('Average Number of Stops per mile', family='serif', fontsize=11, weight='bold', fontname='Times New Roman')

                # Set the title
                ax.set_title("3D Dominant Points", family='serif', fontsize=14, weight='bold', fontname='Times New Roman')

                # Set the legend
                ax.legend()

                # Grid settings
                ax.grid(True, color='black', linestyle='--', linewidth=0.5)

                # Set x-axis limits
                ax.set_xlim(left=0)

                # Save the graph
                graph_file = 'static/images/3D_Pareto_Front_Graph.png'
                plt.savefig(graph_file)
                plt.close()

                        
        return jsonify({
            "message": "Data received successfully", 
            "data": result,
            "markers": markers,
            'graph_file': graph_file 
        })


        # return jsonify({"message": "Data received successfully", "data":result})
    
    elif request.method == 'GET':

        if result:
            return jsonify({
                "status": "success",
                "message": "GET request received. Showing last POST data and dominant_output.",
                "output data": result
            })
        else:
            return jsonify({
                "status": "error",
                "message": "No POST data or dominant_output available"
            })
        




def filter_data_by_date_and_time(selected_date, selected_hour):
    try:
        selected_date = datetime.datetime.strptime(selected_date, '%Y-%m-%d').date()
        filtered_df = df[(df['date'] == selected_date) & (df['time'] == selected_hour)]  # Use dynamic hour

        # Extract latitude, longitude, and intensity
        heat_data = filtered_df.iloc[:, [4, 5]].values.tolist()
        heat_data = [[lat, lon, 1] for lat, lon in heat_data]  # Add intensity
        
        return heat_data
    except Exception as e:
        print(f"Error filtering data: {e}")
        return []


@app.route('/api/filterHeatmapData', methods=['GET'])
def filter_heatmap_data():
    selected_date = request.args.get('date')  # Get selected date from query parameters
    selected_hour = request.args.get('hour')  # Get the selected hour
    print(selected_hour)
    print(selected_date)

    if not selected_date or selected_hour is None:
        return jsonify({"error": "No date or hour provided"}), 400

    try:
        selected_hour = int(selected_hour)  # Convert hour to integer
        heat_data = filter_data_by_date_and_time(selected_date, selected_hour)
        
        if not heat_data:
            return jsonify({"error": "No data found for the selected date and time"}), 404

        return jsonify(heat_data)
    except ValueError:
        return jsonify({"error": "Invalid hour format"}), 400




if __name__ == '__main__':
    app.run(debug=True)
