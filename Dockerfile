FROM selenium/standalone-chrome

USER root
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install selenium



# set display port to avoid crash
ENV DISPLAY=:99


#
WORKDIR /code

#
COPY ./requirements.txt code/src/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r code/src/requirements.txt

#
COPY . /code/

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
