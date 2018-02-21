import random
import time
import csv


def generate_fake_ehr(number_of_records, file_name):
    """
    Generate random EHR records for blockChain POC

    :param number_of_records: int number of records to create
    :param file_name: str name for the csv file we will create
    :return: csv file with random records

    Each simulated EHR will have the following
        1. Patient Name
        2. Gender
        3. Patient ID Number
        4. Date of record
        5. Chief complaint
        6. Summary
        7. Diagnosis
    """

    common_diagnoses = ['Hypertension', 'Hyperlipidemia', 'Diabetes', 'Back pain', 'Anxiety',
                        'Obesity', 'Allergic rhinitis', 'Reflux esophagitis', 'Respiratory problems',
                        'Hypothyroidism', 'Visual refractive errors', 'General medical exam',
                        'Osteoarthritis', 'Fibromyalgia / myositis', 'Malaise and fatigue',
                        'Pain in joint', 'Acute laryngopharyngitis', 'Acute maxillary sinusitis',
                        'Major depressive disorder', 'Acute bronchitis', 'Asthma', 'Depressive disorder',
                        'Nail fungus','Coronary atherosclerosis', 'Urinary tract infection']

    common_complaints = ['Cysts', 'Acne', 'Dermatitis', 'Osteoarthritis', 'Back problems',
                         'Cholesterol problems', 'Upper respiratory condition', 'Anxiety',
                         'Bipolar disorder', 'Depression', 'Chronic neurologic disorder',
                         'High blood pressure', 'Headaches', 'Migraines', 'Diabetes']

    # Create csv file and write the header
    #
    records = open(file_name + ".csv", "w")
    writer = csv.writer(records)
    header = ["Date", "Patient Name", "Gender", "Patient ID", "Chief Complaint", "Summary", "Diagnosis"]

    writer.writerow(header)

    for x in range(number_of_records):
        # Date
        #
        row = []
        date = random_timestamp("1/1/1975 12:00 PM", "2/20/2018 12:00 AM")
        row.append(date)

        # Name
        #
        first_name, last_name, gender = generate_full_name()
        row.append(first_name + " " + last_name)
        row.append(gender)

        patient_id = 1000 + x
        row.append(patient_id)

        complaint = common_complaints[random.randint(0, len(common_complaints) - 1)]
        row.append(complaint)

        summary = generate_random_summary()
        row.append(summary)

        diagnosis = common_diagnoses[random.randint(0, len(common_diagnoses) - 1)]
        row.append(diagnosis)
        writer.writerow(row)

    return None


def random_timestamp(start, end):
    """
    Remark: (strftime-style) = '%m/%d/%Y %I:%M %p' Ex: "1/1/2018 1:30 PM"

    :param start: starting date (in format)
    :param end: ending date (in format)
    :param date_format: date time format (strftime-style)
    :return: random date between start and end in mm/dd/yyyy format
    """
    date_format = "%m/%d/%Y %I:%M %p"

    start_time = time.mktime(time.strptime(start, date_format))
    end_time = time.mktime(time.strptime(end, date_format))

    random_time = start_time + random.random() * (end_time - start_time)

    date_string = time.strftime(date_format, time.localtime(random_time))
    date_split = date_string.split()
    return date_split[0].lstrip(' ')


def test_random_date():
    for x in range(100):
        print(random_timestamp("1/1/1975 12:00 PM", "2/20/2018 12:00 AM"))

# test_random_date()


def generate_first_name():
    gender = random.choice(('male', 'female'))
    random_number = random.random() * 80

    if gender == 'male':
        # Generate a random male name
        #
        with open("MaleFirstNames.csv", 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                name = row[0]
                cumulative = float(row[2])
                if cumulative > random_number:
                    return name, gender
    else:
        # Generate a random male name
        #
        with open("FemaleFirstNames.csv", 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                name = row[0]
                cumulative = float(row[2])
                if cumulative > random_number:
                    return name, gender


def generate_last_name():
    random_number = random.random() * 80

    with open("LastNames.csv", 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            last_name = row[0]
            cumulative = float(row[2])
            if cumulative > random_number:
                return last_name


def generate_full_name():
    first_name, gender = generate_first_name()
    last_name = generate_last_name()

    return first_name, last_name, gender


def test_generate_first_name():
    for x in range(100):
        print(generate_first_name())


def test_generate_last_name():
    for x in range(100):
        print(generate_last_name())


def test_generate_full_name():
    for x in range(100):
        print(generate_full_name())

# test_generate_first_name()
# test_generate_last_name()
# test_generate_full_name()


def generate_random_summary():
    # 100 random lipsums from https://www.lipsum.com/
    #
    random_number = random.randint(0, 99)

    csv_file = open("RandomLipsum.csv", 'r')
    reader = csv.reader(csv_file)
    for i, row in enumerate(reader):
        if i == random_number:
            return row[0]


def test_generate_random_summary():
    for x in range(2):
        print(generate_random_summary())

# test_generate_random_summary()

generate_fake_ehr(200, "SampleRecords")
