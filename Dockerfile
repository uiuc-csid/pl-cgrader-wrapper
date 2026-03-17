FROM prairielearn/grader-c

RUN mkdir -p "/shared" "/shared/submission" \
    && mkdir -p "/grade/data" "/grade/data/student" \
    && echo "{}" > "/grade/data/data.json"

RUN apt-get update \
    && apt-get install -y --no-install-recommends zip unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ["wrapper-entrypoint.sh", "postprocess.py", "/wrapper/"]
RUN chmod u+rx,go-rwx /wrapper /wrapper/wrapper-entrypoint.sh /wrapper/postprocess.py
COPY ["tests", "/grade/tests/"]

ENTRYPOINT ["/wrapper/wrapper-entrypoint.sh"]
