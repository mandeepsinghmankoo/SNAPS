import numpy as np
import os
import qrcode

def park_car(parking_lot, car_info, car_number, rows, cols):
    for i in range(rows):
        for j in range(cols):
            if parking_lot[i][j] == 0:
                parking_lot[i][j] = 1
                car_info[car_number] = (i, j, 0)  # (row, col, entry_time)
                print(f"Car {car_number} parked at spot P{3 * i + j}")
                return
    print("Parking lot is full!")
    return True  # Indicate that the parking lot is full

def calculate_fare(car_info, car_number, exit_time):
    if car_number not in car_info:
        print("Car not found in parking lot!")
        return
    entry_time = car_info[car_number][2]
    parked_time = exit_time - entry_time
    rate_per_hour = 5  # Example rate
    fare = parked_time * rate_per_hour
    print(f"Car {car_number} parked for {parked_time} hours. Fare: ₹{fare}")

    # Generate QR code for fare amount
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(f"The amount you have to pay:₹{fare}")
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img.save(f"qr{car_number}_fare_qr.png")
    
    return fare

def remove_car(parking_lot, car_info, car_number):
    if car_number not in car_info:
        print("Car not found in parking lot!")
        return
    i, j, _ = car_info[car_number]
    parking_lot[i][j] = 0
    del car_info[car_number]
    print(f"Car {car_number} removed from parking lot.")

def delete_car_from_file(file_name, car_number):
    try:
        with open(file_name, "r") as file:
            lines = file.readlines()
        with open(file_name, "w") as file:
            for line in lines:
                if line.strip() != car_number:
                    file.write(line)
        print(f"Car {car_number} deleted from file.")
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")

# Initialize parking lot
rows = 3
cols = 3
parking_lot = np.zeros((rows, cols), dtype=int)
car_info = {}

# Park cars
with open("car_numbers.txt", "r") as file:
    car_numbers = file.readlines()
    for car_number in car_numbers:
        car_number = car_number.strip()
        if park_car(parking_lot, car_info, car_number, rows, cols):
            break  # Stop parking cars if the parking lot is full

# Simulate cars leaving
while True:
    car_number = input("Enter car number leaving the parking lot (or 'exit' to quit): ")
    if car_number == "exit":
        break
    exit_time = float(input("Enter exit time: "))
    fare = calculate_fare(car_info, car_number, exit_time)
    remove_car(parking_lot, car_info, car_number)
    delete_car_from_file("car_numbers.txt", car_number)  # Delete car from file