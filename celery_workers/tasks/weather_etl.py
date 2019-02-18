import ftplib
import os

import arrow

from workers_config.celery_app import celery_app
from handlers.db.stations_model import DBStationsHandler


@celery_app.task
def pull_weather_data(selected_date):
    """Task to update the bids of an account, optionally within an experiment.
    """
    ftp_url = "ftp-cdc.dwd.de"
    folder_name = "/pub/CDC/observations_germany/climate/daily/kl/recent/"
    destination_folder = "/tmp"

    with ftplib.FTP(ftp_url) as ftp:
        ftp.login()
        ftp.cwd(folder_name)
        file_names = ftp.nlst()

        for file_name in file_names:
            if not file_name.endswith(".zip"):
                continue

            with open(os.path.join(destination_folder, file_name), "wb") as file:
                ftp.retrbinary("RETR " + file_name, file.write)


@celery_app.task
def update_station_locations():
    """Pulls the data from the text file and inserts all the stations present in the same.
    It is not idempotent and following executions will raise Integrity exceptions"""
    ftp_url = "ftp-cdc.dwd.de"
    ftp_file_name = "/pub/CDC/observations_germany/climate/daily/kl/recent/KL_Tageswerte_Beschreibung_Stationen.txt"
    destination_folder = "/tmp"
    local_file_name = os.path.join(destination_folder, "stations.txt")

    with ftplib.FTP(ftp_url) as ftp:
        ftp.login()

        with open(local_file_name, "wb") as file:
            ftp.retrbinary("RETR " + ftp_file_name, file.write)

        headers = [
            "station_id",
            "from_date",
            "to_date",
            "stations_hoehe",
            "latitude",
            "longitude",
            "station_name",
        ]
        # encoding detected with chardet
        with open(local_file_name, "r", encoding="ISO-8859-1") as file:
            for i, line in enumerate(file):
                if i > 1:
                    line = line.split()
                    # the last 2 fields are not easy to separate so we will merge them
                    last = line[6:]
                    line = line[:6]
                    line.append("-".join(last))
                    new_station = dict(zip(headers, line))
                    new_station["from_date"] = (
                        arrow.get(new_station["from_date"]).date().isoformat()
                    )
                    new_station["to_date"] = (
                        arrow.get(new_station["to_date"]).date().isoformat()
                    )
                    DBStationsHandler.add(**new_station)
