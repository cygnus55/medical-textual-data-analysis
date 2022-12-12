import pymongo
from dotenv import load_dotenv
import os
import json
from med_terms import LABS, VITALS
import glob

load_dotenv()

text_data = glob.glob("./data/text/*.txt")

try:
    txt = open(text_data[0], encoding='utf-8')
    t = txt.read()
finally:
    txt.close()


def isnumber(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def get_allergies(raw_allergies):
    if raw_allergies[1] == 'No Known Allergies':
        return None
    allergies = []
    for allergy in raw_allergies[1:]:
        A = allergy.split(": ")[1].strip().split(" (")
        try:
            allergies.append({"to": A[0], "type": A[1][:-1]})
        except Exception:
            allergies.append({"to": A[0], "type": 'medicine'})
    return allergies


def get_name(filepath):
    try:
        txt = open(filepath, encoding='utf-8')
        return txt.readlines()[0].strip()
    finally:
        txt.close()


def get_medications(raw_medications):
    medications = []
    for medication in raw_medications[1:]:
        if '[CURRENT]' in medication:
            M = medication.split(" : ")
            medications.append({'medicine': M[1], 'from': M[0][2:12]})
    return medications


def get_conditions(raw_conditions):
    conditions = []
    for condition in raw_conditions[1:]:
        if not '(finding)' in condition:
            C = condition.split(" : ")
            condition = C[1]
            date = C[0].split(" - ")
            conditions.append(
                {'condition': condition,
                    'from': date[0].strip(), 'to': date[1].strip()}
            )
    return conditions

def get_care_plans(raw_care_plans):
    care_plans = []
    for care_plan in raw_care_plans[1:]:
        care_plan = care_plan.strip()
        if '[CURRENT]' in care_plan or '[STOPPED]' in care_plan:
            care_plans.append({'careplan': care_plan.split(" : ")[1], 'date': care_plan.split(
                " : ")[0][:10], 'activities': [], 'status': care_plan.split(" : ")[0][10:]})
        elif care_plan.strip().startswith("Reason: "):
            care_plans[-1]['reason'] = care_plan.replace("Reason: ", '')
        elif care_plan.strip().startswith("Activity: "):
            care_plans[-1]['activities'].append(
                care_plan.replace("Activity: ", ''))
    return care_plans


def get_vitals(raw_vitals, category='VITALS'):
    A = VITALS if category == 'VITALS' else LABS
    vitals = []
    for vital in raw_vitals[1:]:
        vital = vital.strip()
        for V in A:
            if V["DESCRIPTION"] in vital:
                val = vital.split(V["UNITS"])[0].strip().split()[-1]
                if isnumber(val):
                    try:
                        if not any([V["DESCRIPTION"] == v['description'] for v in vitals]):
                            vitals.append(
                                {'description': V["DESCRIPTION"], 'units': V["UNITS"]})
                            vitals[-1]["value"] = vital.split(
                                V["UNITS"])[0].strip().split()[-1]
                    except KeyError:
                        vitals.append(
                            {'description': V["DESCRIPTION"], 'units': V["UNITS"]})
                        vitals[-1]["value"] = vital.split(
                            V["UNITS"])[0].strip().split()[-1]
    return vitals


def get_immunization(raw_immunization):
    immunizations = []
    for imm in raw_immunization[1:]:
        imm = imm.strip()
        date, immunization = imm.split(" : ")
        immunizations.append({'immunization': immunization, 'date': date})
    return immunizations


def get_imaging_studies(raw_imaging):
    imagings = []
    for imm in raw_imaging[1:]:
        imm = imm.strip()
        date, imaging = imm.split(" : ")
        imagings.append({'imaging': imaging, 'date': date})
    return imagings


def wrangle(filepath: str):
    data = {}
    data["patient_name"] = get_name(filepath)
    try:
        txt = open(filepath, encoding='utf-8')

        # Name
        data["patient_name"] = get_name(filepath)

        t = txt.read()
        split1 = t.split("="*len(data["patient_name"]))
        split2 = split1[1].split(
            '--------------------------------------------------------------------------------')
        # print(split2[0].strip().split("\n"))
        # Demographics
        data["demographics"] = {d.split(':')[0].lower(): d.split(
            ':')[1].strip() for d in split2[0].strip().split("\n")}

        # Allergies
        # print(split2[1].strip().split("\n"))
        data["allergies"] = get_allergies(split2[1].strip().split("\n"))

        # Medications
        # print(split2[2].strip().split("\n"))
        data["medications"] = get_medications(split2[2].strip().split("\n"))

        # Conditions
        # assert split2[3].strip().split("\n")[0] == 'CONDITIONS:'
        # print(split2[3].strip().split("\n"))
        data["conditions"] = get_conditions(split2[3].strip().split("\n"))

        # Care plans
        # print(split2[4].strip().split("\n"))
        data["care_plans"] = get_care_plans(split2[4].strip().split("\n"))

        # Vitals
        raw_vitals = split2[5].strip().split("\n")
        raw_vitals.extend(split2[6].strip().split("\n"))

        data["vitals"] = get_vitals(raw_vitals)
        # assert all([isnumber(v["value"]) for v in data["vitals"]])

        # Lab
        data["labs"] = get_vitals(raw_vitals, category='LABS')
        # assert all([isnumber(v["value"]) for v in data["labs"]])

        # Immunization
        raw_immunization = split2[8].strip().split("\n")
        # print(raw_immunization)
        data["immunization"] = get_immunization(raw_immunization)

        # Imaging
        raw_imaging = split2[10].strip().split("\n")
        # print(raw_imaging)
        data["imaging_studies"] = get_imaging_studies(raw_imaging)

        return data
    finally:
        txt.close()


for i in range(len(text_data)):
    try:
        r = wrangle(text_data[i])
    except Exception as e:
        print(e)
        print(i)


data_list = [wrangle(data) for data in text_data]


with open('./data/output/data.json', 'w') as fp:
    json.dump(data_list, fp)

json.dumps(data_list[0])

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")


client = pymongo.MongoClient(
    f"mongodb+srv://{username}:{password}@cluster0.lxsbb.mongodb.net/?retryWrites=true&w=majority")
db = client.medical_record
collection = db["report"]


with open('./data/output/data.json', 'r') as fp:
    data_json = json.load(fp)

# Uncomment the line below.
# collection.insert_many(data_json)
