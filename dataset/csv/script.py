import os
import csv

def calculate_average(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header if there is one
        total = 0
        count = 0
        for row in csv_reader:
            if len(row) >= 3:
                total += float(row[2])
                count += 1
        return total / count if count > 0 else 0

def calculate_min(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header if there is one
        min = float('inf')
        for row in csv_reader:
            if len(row) >= 3:
                value = float(row[2])
                if value < min:
                    min = value
        return min

def calculate_max(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header if there is one
        max = float('-inf')
        for row in csv_reader:
            if len(row) >= 3:
                value = float(row[2])
                if value > max:
                    max = value
        return max

def calculate_std(file_path):
    with open(file_path, mode='r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header if there is one
        total = 0
        count = 0
        for row in csv_reader:
            if len(row) >= 3:
                total += float(row[2])
                count += 1
        average = total / count if count > 0 else 0
        file.seek(0)
        next(csv_reader)  # Skip header if there is one
        total = 0
        for row in csv_reader:
            if len(row) >= 3:
                total += (float(row[2]) - average) ** 2
        return (total / count) ** 0.5

def iterate_folders(base_path):
    for root, dirs, files in os.walk(base_path):
        if 'land' in root:
            continue  # Salta le directory che contengono 'land'

        year_list = []
        min_list = []
        max_list = []
        mean_list = []
        std_list = []

        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)

                min_value = calculate_min(file_path)
                max_value = calculate_max(file_path)
                avg_value = calculate_average(file_path)
                std_value = calculate_std(file_path)
                # save in year file with only numbers
                # Se c'è un modo per ottenere l'anno, aggiungilo a year_list
                year_list.append(int(file.split('.')[0]))  # Esempio statico

                min_list.append(int(min_value))
                max_list.append(int(max_value))
                mean_list.append(int(avg_value))
                std_list.append(int(std_value))

        sorted_data = sorted(zip(year_list, min_list, max_list, mean_list, std_list))
        if sorted_data:  # Ensure data exists before unpacking
            year_list, min_list, max_list, mean_list, std_list = zip(*sorted_data)
        else:
            year_list, min_list, max_list, mean_list, std_list = [], [], [], [], []
        print(f"""
            <datatype>
            name: {root}
            year: {year_list}
            min: {min_list}
            max: {max_list}
            mean: {mean_list}
            std: {std_list}
            </datatype>
        """)

if __name__ == "__main__":
    base_path = '.'
    iterate_folders(base_path)