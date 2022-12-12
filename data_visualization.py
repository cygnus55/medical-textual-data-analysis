import os
import json
from dotenv import load_dotenv
import pymongo
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


load_dotenv()

username = os.environ.get("USERNAME")
password = os.environ.get("PASSWORD")

client = pymongo.MongoClient(f"mongodb+srv://{username}:{password}@cluster0.lxsbb.mongodb.net/?retryWrites=true&w=majority")
db = client.medical_record
collection = db["report"]


a = collection.find({})
b = list(a)


patient = {
    k:[] for k in b[0]["demographics"].keys()
}
patient["patient_id"] = []
for d in b:
    patient["patient_id"].append(d["_id"]),
    for k, v in d["demographics"].items():
        patient[k].append(v)

df_patient = pd.DataFrame(patient)

fig_patient_gender = px.bar(
    x=df_patient["gender"].value_counts().index,
    y=df_patient["gender"].value_counts(),
)

fig_patient_gender.update_layout(
    title="Distribution of Gender",
    xaxis_title="Gender",
    yaxis_title="Frequency",
)

fig_patient_race = px.bar(
    x=df_patient["race"].value_counts().index,
    y=df_patient["race"].value_counts()
)

fig_patient_race.update_layout(
    title="Distribution of race",
    xaxis_title="Race",
    yaxis_title="Frequency",
)

allergies = {
    k:[] for k in b[0]["allergies"][0].keys()
}
allergies["patient_id"] = []
for d in b:
    if d["allergies"]:
        for allergy in d["allergies"]:
            allergies["patient_id"].append(d["_id"])
            for k, v in allergy.items():
                allergies[k].append(v)
    else:
        allergies["patient_id"].append(d["_id"])
        keys = list(allergies.keys())[:-1]
        for k in keys:
            allergies[k].append(None)

df_allergy = pd.DataFrame(allergies)

allergic = df_allergy.groupby("patient_id")["to"].count()
allergic = allergic.gt(0).replace({True:"allergic", False:"not allergic"})


fig_allergy = px.pie(
    values=allergic.value_counts(),
    names=allergic.value_counts().index,
)

fig_allergy.update_layout(
    title="Percentage of Allergic and Non-allergic patients Patients",
)

fig_allergy_type = px.bar(
    x=df_allergy["type"].value_counts().index,
    y=df_allergy["type"].value_counts(),
)

fig_allergy_type.update_layout(
    title="Different types of allergies",
    xaxis_title="Types of allergies",
    yaxis_title="Number of patients",
)


conditions = {
     k:[] for k in b[0]["conditions"][0].keys()
}
conditions["patient_id"] = []
for d in b:
    if d["conditions"]:
        for condition in d["conditions"]:
            conditions["patient_id"].append(d["_id"])
            for k, v in condition.items():
                conditions[k].append(v)
    else:
        conditions["patient_id"].append(d["_id"])
        keys = list(conditions.keys())[:-1]
        for k in keys:
            conditions[k].append(None)


df_conditions = pd.DataFrame(conditions)


top_10_conditions = df_conditions["condition"].value_counts().head(10)


# top_10_conditions.plot(
#     kind="bar",
#     title="Top ten conditions of patients",
#     xlabel="Conditions",
#     ylabel="Number of patients"
# );

fig_top_conditions = px.bar(
    x=top_10_conditions.index,
    y=top_10_conditions,
)

fig_top_conditions.update_layout(
    title="Top ten conditions of patients",
    xaxis_title="Different Conditions",
    yaxis_title="Number of patients",
)


df_demographic_condition = pd.merge(
    df_patient, df_conditions, how='inner', on=["patient_id"]
)[["gender", "condition"]]


top_conds = top_10_conditions.index


df_demographic_condition["gender"] = df_demographic_condition["gender"].replace({"M": "male", "F": "female"})

cond_gender = {k:{"male":0, "female":0} for k in top_conds}

for index, row in df_demographic_condition.iterrows():
    if row["condition"] in top_conds:
        cond_gender[row["condition"]][row["gender"]] += 1

df_cond_gender = pd.DataFrame(cond_gender).T

fig_cond_gender = px.bar(
    df_cond_gender,
    barmode='group'
)

fig_cond_gender.update_layout(
    title="Top ten conditions of patients distributed among genders",
    xaxis_title="Different Conditions",
    yaxis_title="Number of patients",
)


immunizations = {
    k:[] for k in b[0]["immunization"][0].keys()
}

immunizations["patient_id"] = []

for d in b:
    if d["immunization"]:
        for imm in d["immunization"]:
            immunizations["patient_id"].append(d["_id"])
            for k, v in imm.items():
                immunizations[k].append(v)
    else:
        immunizations["patient_id"].append(d["_id"])
        keys = list(immunizations.keys())[:-1]
        for k in keys:
            immunizations[k].append(None)


df_imm = pd.DataFrame(immunizations)
df_imm["date"] = pd.to_datetime(df_imm['date'])
df_imm["immunization"].value_counts()
df_imm_covid = df_imm[df_imm["immunization"].str.contains("COVID")==True].sort_values(by='date')
df_imm["month_year"] = df_imm_covid["date"].dt.to_period('M')
covid_21_22 = df_imm.groupby("month_year")["immunization"].count()

fig_covid_21_22 = px.line(
    x=covid_21_22.index.strftime("%Y-%m"),
    y=covid_21_22
)

fig_covid_21_22.update_layout(
    title="Time plot of COVID vaccination from Jan 2021 to June 2022",
    xaxis_title="Month and Year of vaccination",
    yaxis_title="Number of patients",
)
# covid_21_22.plot(
#     title="Time plot of COVID vaccination from Jan 2021 to June 2022",
#     xlabel="Time",
#     ylabel="Frequency of vaccination"
# );