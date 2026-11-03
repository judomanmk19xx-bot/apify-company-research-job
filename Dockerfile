FROM apify/actor-python:3.12

COPY requirements.txt ./

RUN echo "Python version:" \
 && python --version \
 && echo "Pip version:" \
 && pip --version \
 && pip install --no-cache-dir -r requirements.txt

COPY . ./

CMD ["python", "-m", "src.main"]
