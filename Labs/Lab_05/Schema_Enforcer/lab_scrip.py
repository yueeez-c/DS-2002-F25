import pandas as pd
import json
def generate_raw_data():
    student_id = "id"
    major = "mj"
    GPA = 4
    is_cs_major ="Yes"
    credits_taken = "18.0"
    output_filename = "Labs/Lab_05/Schema_Enforcer/raw_survey_data.csv"
    raw_data = {
        "student_id": [student_id],
        "major": [major],
        "GPA": [GPA],
        "is_cs_major": [is_cs_major],
        "credits_taken": [credits_taken]
    }
    df = pd.DataFrame(raw_data)
    df.to_csv(output_filename, index=False)

    courses_list = [
                        {
                            "course_id": "DS2002",
                            "section": "001",
                            "title": "Data Science Systems",
                            "level": 2000,
                            "instructors": [
                            {"name": "Austin Rivera", "role": "Primary"}, 
                            {"name": "Heywood Williams-Tracy", "role": "TA"} 
                            ]
                        },
                        {
                            "course_id": "DS2004",
                            "section": "003",
                            "title": "Data Ethics",
                            "level": 2000,
                            "instructors": [
                            {"name": "Emanueal Moss"}
                            ]
                        },
                        {
                            "course_id": "CS4710",
                            "section": "002",
                            "title": "Artificial Intelligence",
                            "level": 4000,
                            "instructors": [
                            {"name": "Ferdinando Fioretto", "role": "Primary"}
                            ]
                        }
                        ]
    json_output_filename = "Labs/Lab_05/Schema_Enforcer/raw_course_catalog.json"
    with open(json_output_filename, 'w') as json_file:
        json.dump(courses_list, json_file, indent=4)
def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        raw_data = json.load(json_file)
    df = pd.json_normalize(raw_data, record_path=['instructors'], meta=['course_id', 'section', 'title', 'level'], errors='ignore')
    df.to_csv("Labs/Lab_05/Schema_Enforcer/clean_course_catalog.csv", index=False)
    pass
def read_csv_file(file_path):
    raw_data = pd.read_csv(file_path)
    raw_data['is_cs_major'] = raw_data['is_cs_major'].replace({"Yes": True, "No": False})
    raw_data['GPA'] = raw_data['GPA'].astype(float)
    raw_data['credits_taken'] = raw_data['credits_taken'].astype(float)
    raw_data.to_csv("Labs/Lab_05/Schema_Enforcer/clean_survey_data.csv", index=False)
    pass
if __name__ == "__main__":
    generate_raw_data()
    json_file_path = "Labs/Lab_05/Schema_Enforcer/raw_course_catalog.json"
    csv_file_path = "Labs/Lab_05/Schema_Enforcer/raw_survey_data.csv"
    read_csv_file(csv_file_path)
    read_json_file(json_file_path)

