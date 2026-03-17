#!/bin/bash

set +H

feedback_error () {
    local contents="$@"
    echo "$contents"
    echo "$contents" >&2
    echo "$contents" > /shared/feedback.json
}

exit_error () {
    feedback_error "{\"fractionalScore\": 0, \"feedback\": \"Error: $@\"}"
    exit 3
}

EXPECTED_SUBMISSION_FILE="/shared/submission/submission.zip"
if [ ! -f "$EXPECTED_SUBMISSION_FILE" ] ; then
    staff_log_msg="Could not find file $EXPECTED_SUBMISSION_FILE"
    echo "$staff_log_msg"
    echo "$staff_log_msg" >&2
    find /shared
    find /shared >&2
    exit_error "submission.zip file not found. Please try resubmitting."
fi

(
    cd /shared/submission || exit
    mkdir -p /grade/student || exit
    unzip submission.zip -d /grade/student || exit
)

if [ $? -ne 0 ] ; then
    exit_error "There was a problem extracting your zip file. Please try resubmitting."
fi

GRADER_ENTRYPOINT="/cgrader/entrypoint.sh"
EXPECTED_TEST_FILE="/grade/tests/test.py"

# for resilience and ease of deployment with existing questions
EXPECTED_TEST_FILE_ALT="/grade/tests/tests.py"
if [ ! -f "$EXPECTED_TEST_FILE" ] && [ -f "$EXPECTED_TEST_FILE_ALT" ] ; then
    staff_log_msg="Did not find $EXPECTED_TEST_FILE but did find $EXPECTED_TEST_FILE_ALT - making a copy as a workaround."
    echo "$staff_log_msg"
    echo "$staff_log_msg" >&2
    cp -av "$EXPECTED_TEST_FILE_ALT" "$EXPECTED_TEST_FILE"
fi

if [ ! -f "$EXPECTED_TEST_FILE" ] ; then
    staff_log_msg="The expected file \"$EXPECTED_TEST_FILE\" was not found. Staff: Please check that the file is being included in the container build and that it is spelled correctly."
    echo "$staff_log_msg"
    echo "$staff_log_msg" >&2
    exit_error "Grader not configured correctly. Please report this to the course staff."
fi

if [ ! -f "$GRADER_ENTRYPOINT" ] ; then
    exit_error "Grader entrypoint not found. Please report this to the course staff."
fi
if [ ! -x "$GRADER_ENTRYPOINT" ] ; then
    exit_error "Grader entrypoint not executable. Please report this to the course staff."
fi

/cgrader/entrypoint.sh &

wait

if [ ! -r "/grade/results/results.json" ] ; then
    exit_error "Error processing grade results. Your code might have crashed."
fi

exec /wrapper/postprocess.py /grade/results/results.json
