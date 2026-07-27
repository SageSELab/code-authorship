"""
Batch-verify that GPT-4-generated adversarial samples actually applied the
transformation rule they were asked to apply.

Reads the functionally-accepted adversarial samples (produced by
get-all-accepted-samples.py after submit2leetcode.py confirmed they still pass
LeetCode's tests), runs the matching rule checker from
adversarial_sample_verification.py on each, and records the verdict.

Usage:
  python verify-adversarial-samples.py \
      [--input_csv=adversarial_samples_GPT4_accepted.csv] \
      [--output_csv=adversarial_samples_GPT4_verified.csv] \
      [--invalid_dir=Invalid-Transformations]

Every sample judged invalid is also written out as a side-by-side markdown diff
under --invalid_dir/<rule>/, which is how the transformation rules were audited
manually for the paper.

The rule-checking functions themselves live in
adversarial_sample_verification.py and are covered by the unit tests in
adversarial-rule-unit-tests/ (run them with scripts/run-tests.sh).
"""

import argparse
import os

import pandas as pd

from adversarial_sample_verification import (
    are_comments_equal,
    check_rule6_and_7,
    check_rule_0,
    check_rule_1,
    check_rule_2,
    check_rule_3,
    check_rule_4,
    check_rule_5,
    check_rule_8,
    check_rule_9,
    check_rule_10,
    check_rule_11,
    check_rule_12,
    check_rule_13,
    check_rule_14,
    check_rule_15,
    check_rule_16,
    check_rule_17_and_18,
    check_rule_19_and_20,
    check_rule_21,
    check_rule_22,
    check_rule_23,
    check_rule_24,
    check_rule_25,
    check_rule_26,
    check_rule_27,
    find_code_snippet,
)

# Rule number -> checker. Rules 6/7, 17/18 and 19/20 are symmetric pairs
# (for->while and while->for, etc.) and share a single checker.
RULE_CHECKERS = {
    0: check_rule_0,
    1: check_rule_1,
    2: check_rule_2,
    3: check_rule_3,
    4: check_rule_4,
    5: check_rule_5,
    6: check_rule6_and_7,
    7: check_rule6_and_7,
    8: check_rule_8,
    9: check_rule_9,
    10: check_rule_10,
    11: check_rule_11,
    12: check_rule_12,
    13: check_rule_13,
    14: check_rule_14,
    15: check_rule_15,
    16: check_rule_16,
    17: check_rule_17_and_18,
    18: check_rule_17_and_18,
    19: check_rule_19_and_20,
    20: check_rule_19_and_20,
    21: check_rule_21,
    22: check_rule_22,
    23: check_rule_23,
    24: check_rule_24,
    25: check_rule_25,
    26: check_rule_26,
    27: check_rule_27,
}

# Rule 0 asks the model to strip comments, so a comment-equality check would
# contradict it. Every other rule must leave comments untouched.
RULES_WITHOUT_COMMENT_CHECK = {0}


def verify_sample(original_code, adversarial_code, language, rule):
    """Return True if `adversarial_code` is a valid application of `rule`."""
    checker = RULE_CHECKERS.get(rule)
    if checker is None:
        return False

    result = checker(original_code, adversarial_code, language)
    if rule not in RULES_WITHOUT_COMMENT_CHECK:
        result = result and are_comments_equal(original_code, adversarial_code, language)
    return result


def write_invalid_report(invalid_dir, rule, location, language, original_code, adversarial_code):
    """Write a side-by-side markdown diff for a sample that failed its rule."""
    rule_dir = os.path.join(invalid_dir, str(rule))
    os.makedirs(rule_dir, exist_ok=True)
    with open(os.path.join(rule_dir, f"{location}-{rule}.md"), "w") as f:
        f.write(f"Original Code:\n ```{language}\n{original_code}```\n")
        f.write(f"Adversarial Code:\n ```{language}\n{adversarial_code}```\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    parser.add_argument("--input_csv", default="adversarial_samples_GPT4_accepted.csv",
                        help="Adversarial samples that passed LeetCode's functional tests.")
    parser.add_argument("--output_csv", default="adversarial_samples_GPT4_verified.csv",
                        help="Where to write the input plus a 'valid_transformation' column.")
    parser.add_argument("--invalid_dir", default="Invalid-Transformations",
                        help="Directory for the per-rule markdown reports on invalid samples.")
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)
    df['valid_transformation'] = None

    errors = 0
    for index, row in df.iterrows():
        adversarial_code = row['adversarial_code']
        language = row['language']
        rule = row['rule']
        location = row['location']

        try:
            original_code = find_code_snippet(location)
            result = verify_sample(original_code, adversarial_code, language, rule)
            df.at[index, 'valid_transformation'] = result

            if not result:
                write_invalid_report(args.invalid_dir, rule, location, language,
                                     original_code, adversarial_code)
        except Exception as e:
            # Keep going rather than aborting the sweep, but surface the count.
            # The original script broke out of the loop on the first failure,
            # silently truncating the verification run.
            errors += 1
            print(f"Error processing rule {rule} for location {location}: {e}")

    df.to_csv(args.output_csv, index=False)

    valid = int((df['valid_transformation'] == True).sum())  # noqa: E712
    invalid = int((df['valid_transformation'] == False).sum())  # noqa: E712
    print(f"\nVerified {len(df)} samples: {valid} valid, {invalid} invalid, {errors} errored.")
    print(f"Wrote {args.output_csv}; invalid-sample reports in {args.invalid_dir}/")


if __name__ == '__main__':
    main()
