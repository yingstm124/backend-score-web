# Dockerfile - this is a comment. Delete me if you want.
FROM tensorflow/tensorflow
COPY . /app
WORKDIR /app
# RUN pip install -r requirements.txt
RUN pip install pymysql
# RUN pip install tensorflow
RUN pip install flask
RUN pip install Flask-Cors
# RUN pip install cv2
# RUN pip3 install json
RUN pip install numpy
# ENTRYPOINT ["python"]
CMD ["python", "./app.py"]

