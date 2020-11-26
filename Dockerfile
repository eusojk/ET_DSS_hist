# FROM amancevice/pandas:1.1.4
FROM eusojk/dssatv47-ubuntu:v0.0.2.2020

RUN mkdir -p /home/ET_DSS_HIST/dssat_files_dir
RUN cp -r /home/dssat-base-files/* /home/ET_DSS_HIST/dssat_files_dir
COPY . /home/ET_DSS_HIST

WORKDIR /home/ET_DSS_HIST

RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]