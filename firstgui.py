import tkinter as tk
import serial
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque

# Create the main window
root = tk.Tk()
root.title("Tkinter with Matplotlib Plot and Circle")

# Set the size of the Tkinter window
root.geometry("1000x1000")

# Create a Tkinter canvas
canvas = tk.Canvas(root, width=1000, height=1000, bg="lightsteelblue")
canvas.pack()

# Create a Matplotlib figure with a specified size
fig = plt.figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)

# Initialize lists to store time and voltage data
time_data = []  # Store the last 100 time values
voltage_data = []  # Store the last 100 value readings
average_voltage = []
averages = []
average_time = []

line, = ax.plot(time_data, voltage_data)
avg_line, = ax.plot(average_time, averages)

ser = serial.Serial('COM5', 9600)
font = {'family': 'Georgia', 'size': 12}

def update_plot():
    try:
        # Read data from serial port
        count = 0
        data_parts = []
        data_count = 0
        average_count = 0
        while count < 2:
            value = ser.readline().decode().strip()
            data_parts.append(value)
            count += 1
            average_count += 1
        if len(data_parts) == 2:
            data_count += 1
            time_value = float(data_parts[1]) / 1000
            voltage_value = float(data_parts[0])
            time_data.append(time_value)
            voltage_data.append(voltage_value)
            if len(time_data) == len(voltage_data):
                # Calculate the average every 10 data points
                if len(voltage_data) % 10 == 0:
                    average_val = sum(voltage_data[-10:]) / 10
                    averages.append(average_val)
                    average_time.append(time_value)

            if data_count <= 1:
                average_voltage.append(float(data_parts[0]))
            else:
                length = len(average_voltage)
                old_average = float(average_voltage[length - 1]) * (data_count - 1)
                new_average = float((old_average + data_parts[0])/(data_count))
                average_voltage.append(new_average)

            # Update plot with new data
            line.set_xdata(time_data)
            line.set_ydata(voltage_data)
            # avg_line.set_xdata(average_time)
            # avg_line.set_ydata(averages)
            # ax.plot(average_time, average_voltage, color='red')
            ax.set_xlabel('Time (s)', fontdict=font)
            ax.set_ylabel('Voltage (V)', fontdict=font)
            ax.set_title('Real-Time Voltage Plot', fontdict=font)
            ax.set_ylim(1, 2.5)

            # Update plot limits if needed
            ax.relim()
            ax.autoscale_view()

            # Redraw canvas
            fig_canvas.draw()

    except Exception as e:
        print(f"Error reading serial data: {e}")

    # Call update_plot function again after a delay
    root.after(1, update_plot)  # Update every 1 ms

# Function to handle slider movements
def slider_move(value):
    global x_left_1, x_right_1, x_left_2, x_right_2, difference, colors, new_coords  # Declare variables as global
    change = int(value) / 2
    x_left_1 = 650 - change / 2
    x_right_1 = 700 + change / 2
    x_left_2 = 700 - change / 2
    x_right_2 = 750 + change / 2
    difference = (x_right_1 - x_left_1)/2
    pressure = (1)/(4 * 3.14 * (difference * difference))
    pressure_rounded = "{:.6f}".format(pressure)
    print(pressure_rounded)
    label.config(text=f"Radius: {difference}")
    label_2.config(text=f"{pressure_rounded}")
    add = int(value)*10
    # Redraw arcs with updated coordinates
    canvas.delete("arc")  # Clear previous arcs
    canvas.create_arc(x_left_1, y_top, x_right_1, y_bottom, start=90, extent=180, outline='blue', width=3, style=tk.ARC, tags="arc")
    canvas.create_arc(x_left_2, y_top, x_right_2, y_bottom, start=270, extent=180, outline='blue', width=3, style=tk.ARC, tags="arc")
    new_coords = (825, 50+add, 925, 50+add)
    print(new_coords)
    canvas.coords(pressure_line, new_coords)


# Create a FigureCanvasTkAgg object to embed the Matplotlib plot into the Tkinter canvas
fig_canvas = FigureCanvasTkAgg(fig, master=root)
fig_canvas_widget = fig_canvas.get_tk_widget()

# Create a window within the canvas to hold the Matplotlib plot
canvas.create_window(300, 300, window=fig_canvas_widget)  # Position at (400, 300)
canvas.create_rectangle(625, 25, 950, 750, fill="white")
# Draw lines
canvas.create_line(675, 50, 675, 150, fill="blue", width=3)
canvas.create_line(725, 50, 725, 150, fill="blue", width=3)
canvas.create_line(675, 450, 675, 550, fill="blue", width=3)
canvas.create_line(725, 450, 725, 550, fill="blue", width=3)
canvas.create_rectangle(825, 50, 925, 150, fill="green")
canvas.create_rectangle(825,150, 925, 250, fill="yellowgreen")
canvas.create_rectangle(825, 250, 925, 350, fill="yellow")
canvas.create_rectangle(825, 350, 925, 450, fill="orange")
canvas.create_rectangle(825, 450, 925, 550, fill="red")
pressure_line = canvas.create_line(825, 50, 925, 50, fill="blue", width=3)

# Define the initial bounding box parameters for the arcs
x_left_1 = 650
x_right_1 = 700
x_left_2 = 700
x_right_2 = 750
y_top = 150
y_bottom = 450
difference = (x_right_1 - x_left_1)/2
# Draw the arcs
canvas.create_arc(x_left_1, y_top, x_right_1, y_bottom, start=90, extent=180, outline='blue', width=3, style=tk.ARC, tags="arc")
canvas.create_arc(x_left_2, y_top, x_right_2, y_bottom, start=270, extent=180, outline='blue', width=3, style=tk.ARC, tags="arc")

# Create a label
label = tk.Label(root, text = f"Radius: {difference}", font=("Georgia", 25), bg="white", fg="darkblue")
label.place(x = 700, y=675)
pressure = (1.0)/(4 * 3.14 * (difference * difference))
pressure_rounded = "{:.2f}".format(pressure)
label_pressure = tk.Label(root, text="Pressure", font=("Georgia", 25), bg="white", fg="darkblue")
label_pressure.place(x=805, y=565)
label_2 = tk.Label(root, text = f"{pressure_rounded}", font=("Georgia", 25), bg="white", anchor="center", fg="darkblue")
label_2.place(x = 840, y=600)
# Create a Scale widget (horizontal slider)
slider = tk.Scale(root, from_=0, to=50, orient=tk.HORIZONTAL, command=slider_move)
slider.place(x=650, y=550)
title = tk.Label(root, text='Catheter Interface', font=('Georgia', 30),bg="lightsteelblue", anchor='center', fg="darkblue")
title.place(x=200, y=30)
# Start updating the plot
update_plot()

# Run the Tkinter main loop
root.mainloop()