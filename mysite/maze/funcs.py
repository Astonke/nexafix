from encron.tools import find_file

db_file=find_file('verif_code.csv')

def verify_code(submitted_code,db_file=db_file):
        import csv
     # Read the codes from the CSV file
        with open(db_file, 'r') as file:
            reader = csv.reader(file)
            codes = [row[0] for row in reader]

        # Check if the submitted code is in the list
        if submitted_code in codes:
            # Remove the used code
            codes.remove(submitted_code)

            # Rewrite the updated codes list back to the CSV file
            with open(db_file, 'w', newline='') as file:
                writer = csv.writer(file)
                for code in codes:
                    writer.writerow([code])

            # Code is valid, proceed to success response
            return True

        else:
            # Code is not in the file, return invalid message
            return False