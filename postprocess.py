#!/usr/bin/env python3

import sys
import json


DEFAULT_FEEDBACK_FILENAME = "/shared/feedback.json"
DEFAULT_ERROR = "Error during grading process. Please contact course staff."


def make_feedback_object(score, feedback):
    return {
        "fractionalScore": score,
        "feedback": feedback
    }


def write_feedback_object(feedback_object, filename=DEFAULT_FEEDBACK_FILENAME):
    with open(filename, "w") as f:
        # to avoid errors on Coursera, do not add any whitespace with the
        # indent= option
        json.dump(feedback_object, f, indent=None)


def exit_feedback_error(message=DEFAULT_ERROR, exception=None):
    # The message will be shown to the student, but the exception will only
    # be shown to staff in the logs.
    if exception:
        print(exception)
        print(exception, file=sys.stderr)
    feedback = make_feedback_object(0, message)
    print(feedback)
    print(feedback, file=sys.stderr)
    write_feedback_object(feedback)
    sys.exit(0)


def handle_single_test_result(test_result):
    feedback_string = ""

    name = test_result.get("name", None)
    if name:
        feedback_string += f"\n\nTest name: {name}"

    description = test_result.get("description", None)
    if description:
        feedback_string += f"\n\nDescription: {description}"

    points = test_result.get("points", None)
    max_points = test_result.get("max_points", None)
    if None not in (points, max_points):
        feedback_string += f"\n\nPoints: {points} out of {max_points}"

    message = test_result.get("message", None)
    if message:
        feedback_string += f"\n\nMessage: {message}"

    output = test_result.get("output", None)
    if output:
        feedback_string += f"\n\nOutput: {output}"

    images = test_result.get("images", None)
    if images and len(images):
        feedback_string += "\n\nWARNING: The grader returned images but these are not currently supported by the server."

    return feedback_string


def handle_pl_results(pl_results):
    # An example results json can be found here:
    # https://prairielearn.readthedocs.io/en/latest/externalGrading/#grading-results
    # The basic checks are similar to processGradingResult:
    # https://github.com/PrairieLearn/PrairieLearn/blob/master/apps/prairielearn/src/lib/externalGrader.ts
    # The individual test parsing is similar to the pl-external-grader-results element:
    # https://github.com/PrairieLearn/PrairieLearn/blob/master/apps/prairielearn/elements/pl-external-grader-results/pl-external-grader-results.py

    gradable = pl_results.get("gradable", True)
    succeeded = pl_results.get("succeeded", True)
    if gradable and succeeded:
        try:
            score = pl_results["score"]
        except KeyError as e:
            wrapped_e = Exception(f"Grader did not return a score. Exception: {e}")
            exit_feedback_error(exception=wrapped_e)
        try:
            score = float(score)
            if score < 0.0 or score > 1.0:
                raise Exception("Score out of range.")
        except Exception as e:
            exit_feedback_error(exception=e)
    else:
        score = 0.0

    message = pl_results.get("message", "[No feedback summary message given by grader.]")
    feedback_string = f"{message}"

    output = pl_results.get("output", "[No program output text reported by grader.]")
    feedback_string += f"\n\n{output}"

    format_errors = pl_results.get("format_errors", None)
    if format_errors:
        try:
            format_errors = format_errors.get("_external_grader")
        except:
            format_errors = str(format_errors)
        feedback_string += f"\n\nThe grader found these format errors: {format_errors}"

    images = pl_results.get("images", [])
    if images and len(images):
        feedback_string += "\n\nWARNING: The grader returned images but these are not currently supported by the server."

    tests = pl_results.get("tests", [])
    if tests and len(tests):
        feedback_string += f"\n\nIndividual test case results:"
        for test in tests:
            processed_test_output = handle_single_test_result(test)
            feedback_string += f"\n\n{processed_test_output}"

    feedback_object = make_feedback_object(score, feedback_string)
    print(feedback_object)
    print(feedback_object, file=sys.stderr)
    write_feedback_object(feedback_object)


def main(pl_results_filename):
    try:
        with open(pl_results_filename) as f:
            pl_results = json.load(f)
        handle_pl_results(pl_results)
    except Exception as e:
        # We don't disambiguate grading system errors for the student at this
        # level. Only the staff will see the detailed exception.
        exit_feedback_error(exception=e)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("[Error] Expected argument: PL results filename (results.json)")
        sys.exit(1)
    main(sys.argv[1])
