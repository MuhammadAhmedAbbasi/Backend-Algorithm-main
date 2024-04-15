FROM python:3.12
WORKDIR /mental-connect-algorithm
COPY . ./algorithm
RUN pip install flask==2.2.5
RUN pip install flask_mongoengine
RUN pip install flask_jwt_extended
RUN pip install gunicorn
RUN pip install redis
RUN pip install flask_restplus
RUN pip install torch
RUN pip install scikit-learn 

ENV FLASK_APP=Service/app.py

EXPOSE 8090

CMD ["flask","run", "--host", "0.0.0.0"]