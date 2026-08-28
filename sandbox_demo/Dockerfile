FROM python:3.10-slim

WORKDIR /workspace

COPY hello.py .
COPY cpu_demo.py .

USER 65532:65532

CMD ["python", "hello.py"]