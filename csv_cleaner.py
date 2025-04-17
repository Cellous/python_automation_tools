import csv

def clean_csv(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        for row in reader:
            if any(field.strip() for field in row):  # Skip empty rows
                writer.writerow(row)

if __name__ == "__main__":
    clean_csv('input.csv', 'output_clean.csv')
    print("CSV cleaned and saved as 'output_clean.csv'")
