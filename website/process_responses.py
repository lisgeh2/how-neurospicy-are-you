from pathlib import Path
from statistics import mean
import json
import render_certificate as rc

DATA_FILE = Path(__file__).parent / "full_database" / "data" / "responses.jsonl"

from statistics import NormalDist


responses = []


def reload_responses():
    responses.clear()
    if DATA_FILE.exists():
        responses.extend(
            json.loads(line)
            for line in DATA_FILE.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    return responses


reload_responses()
# take token as an arugment everywhere

def likert_to_number(likert_item):
    num = likert_item[0]
    try:
        return int(num)
    except TypeError as e:
        print(f"this doesn't have a proper likert format, first letter is {num}")
        return None

def calculate_sum(list_of_vars, token="0dbf99c72f98247392b90464ec3eb13a90f8244d9610fef4817cbc1fe327fc91"):
    list_of_vars_int = []
    for var in list_of_vars:
        user_record = next(r for r in responses if r["token"] == token)
        answer = user_record["answers"][var]
        if isinstance(answer, str):
            num = likert_to_number(answer)
            if "_r_" in var:
                num = 6-num
            list_of_vars_int.append(num)
        else:
            list_of_vars_int.append(answer)
    # We ignore Nones:
    list_of_vars_int = [answer for answer in list_of_vars_int if answer is not None]

    return sum(list_of_vars_int)


def find_questions_end_with(suffix="_autism", token=...):
    user_record = next(r for r in responses if r["token"] == token)
    return [key for key in user_record["answers"] if key.endswith(suffix)]



AUTISM_GROUP_MEAN = 74.95
AUTISM_GROUP_SD = 11.56

NORM_AUTISM_GROUP_MEAN = 38.72
NORM_AUTISM_GROUP_SD = 12.84

ADHD_GROUP_MEAN = 41.57
ADHD_GROUP_SD = 9.93

NORM_ADHD_GROUP_MEAN = 19.69
NORM_ADHD_GROUP_SD = 6.68



if __name__ == "__main__":
    autism_mean = calculate_sum(find_questions_end_with("_autism", token="36474d9016610351a4955b014a496bc30db936b8b8497451a71c08772a9bfc08"), token="36474d9016610351a4955b014a496bc30db936b8b8497451a71c08772a9bfc08")
    adhd_mean = calculate_sum(find_questions_end_with("_adhd", token="36474d9016610351a4955b014a496bc30db936b8b8497451a71c08772a9bfc08"), token="36474d9016610351a4955b014a496bc30db936b8b8497451a71c08772a9bfc08")
    certificate_html = (rc.render_title_html() + rc.render_adhd_html(adhd_mean) + rc.render_autism_html(autism_mean))
    with open("preview.html", "w", encoding="utf-8") as f:
        f.write(
            "<!doctype html><meta charset='utf-8'>"
            "<body style='margin:0;padding:24px;background:#f9fafb;max-width:820px'>"
            f"{certificate_html}</body>"
        )
    print("preview.html geschrieben")
