import pandas as pd
import leetcode
from time import sleep
import json

leetcode_session = ""
csrf_token = ""

configuration = leetcode.Configuration()

configuration.api_key["x-csrftoken"] = csrf_token
configuration.api_key["csrftoken"] = csrf_token
configuration.api_key["LEETCODE_SESSION"] = leetcode_session
configuration.api_key["Referer"] = "https://leetcode.com"
configuration.debug = False

api_instance = leetcode.DefaultApi(leetcode.ApiClient(configuration))

av_df = pd.read_csv('./adversarial_samples.csv')
av_df["Status"] = ""

with open(f"./problem_urls_dict.json", "r") as problem_url_dict_f:
    problem_url_dict = json.load(problem_url_dict_f)
    problem_url_dict = {v: k for k, v in problem_url_dict.items()}

def get_slug(problem_id):
    problem_url = problem_url_dict[problem_id]
    return problem_url.split("/")[-1]
    
for index, row in av_df.iterrows():
    code = row["adv_code"]
    lang = row["lang"]
    problem_id = row["problem_id"]
    problem_slug = get_slug(problem_id)
    
    submission = leetcode.Submission(
        judge_type="large", typed_code=code, question_id=problem_id, test_mode=False, lang="csharp"
    )

    submission_id = api_instance.problems_problem_submit_post(
        problem=problem_slug, body=submission
    )

    sleep(5)

    submission_result = api_instance.submissions_detail_id_check_get(
        id=submission_id.submission_id
    )

    av_df.at[index, "Status"] = submission_result["status_msg"]
    

av_df.to_csv('adversarial_samples_v2.csv', index=False)



