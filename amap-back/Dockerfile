# our base image
FROM debian:stable-slim

# Install npm and quasar-cli
ENV LC_ALL=C
RUN apt-get update
RUN apt-get -y install python3-dev
RUN apt-get -y install python3-pip
RUN apt-get -y install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config
RUN apt-get -y install libsm6 libxext6 libxrender-dev
RUN pip3 install opencv-contrib-python
RUN pip3 install flask
RUN pip3 install flask_cors
RUN pip3 install requests
RUN pip3 install tesserocr
RUN pip3 install pillow
RUN pip3 install shapely
RUN pip3 install scikit-image
RUN pip3 install gunicorn

# Copy Quasar src files
ADD . / /usr/backend/

# tell the port number the container should expose
EXPOSE 5000

# run the application
WORKDIR /usr/backend/
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "amap2-serv:app"]