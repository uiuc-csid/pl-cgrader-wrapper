# PrairieLearn cgrader wrapper for Coursera

This is a basic wrapper around the PrairieLearn project's `cgrader` (also referred to as `grader-c` or `c-grader` in various PrairieLearn repositories), which is a framework for autograding C and C++ programming assignments. This wrapper helps you adapt your existing PrairieLearn-format programming questions for deployment on Coursera.

## Using a single question's tests

Copy your PL question's `tests` directory contents into the `tests` directory provided here, replacing the example file. The wrapper entrypoint will try to find either `test.py` or `tests.py` at runtime to minimize configuration problems.

The PL cgrader generally expects to find the file `tests/test.py`. Naming the file `tests.py` is a common mistake that could cause a startup error. Some legacy questions with this naming discrepancy may have customized the entrypoint in their PL question info.json file to launch successfully in spite of the unconventional naming. The wrapper tries to support either convention.

## Building the grader

After you have placed the test files, use the provided script `make-grader-build-zip.sh` to create a zip file containing a Docker recipe that you can upload to Coursera in the edit sreen for your specific programming assignment. The zip will contain the wrapper scripts and your question's test files. After you upload the build zip, Coursera should handle the build step automatically in its cloud infrastructure. When it finishes building, you can publish the assignment and test it in the student view mode.

You will need to create a separate build zip for each PL question that you wish to adapt, switching the the contents of the `tests` directory before generating each zip.

## Student submission format

In your Coursera assignment, students should submit a file `submission.zip` containing exactly those files that you expected to grade. You could provide students with whatever type of submission script you find appropriate to automate this, but those details are beyond the scope of this wrapper.

## Limitations

Currently, the wrapper does not support advanced feeback such as bundled image files.

The feedback is provided as plain text only.

The score is internally converted into Coursera's required fraction out of 1.0, although students might see this post-multiplied by the number of points you specify in your grading rubric for the assignment on Coursera.

## References

- (PL cgrader source code)[https://github.com/PrairieLearn/PrairieLearn/tree/master/graders/c]
- (PL cgrader Docker image)[https://hub.docker.com/r/prairielearn/grader-c]
- (PL documentation on the cgrader)[https://docs.prairielearn.com/c-grader/]
- (Coursera's autograder testing tool)[https://github.com/coursera/coursera_autograder]
- (Coursera's documentation on their V2 feedback specification)[https://github.com/coursera/programming-assignments-demo/tree/master/custom-graders]
