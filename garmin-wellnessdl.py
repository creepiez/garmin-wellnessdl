# Dedicated by https://github.com/petergardfjall/garminexport
# Run first: 'pip install garminexport[cloudflare]'

import argparse
import getpass
import logging
import datetime
import zipfile
import os
import os.path
import time

from garminexport.garminclient import GarminClient

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

save = ""
saved_zip = []

def get_wellness(client, day):
    """Return the original file that was uploaded for a wellness.
    If the activity doesn't have any file source (for example,
    if it was entered manually rather than imported from a Garmin
    device) then :obj:`(None,None)` is returned.
    :day: Day of a wellness file.
    :returns: Not implemented. Please implement yourself!
    :rtype: (str, str)
    """
    filename="{}.zip".format(day.strftime("%Y-%m-%d"))
    response = client.session.get(
        "https://connect.garmin.com/proxy/download-service/files/wellness/{}".format(filename))
    # A 404 (Not Found) response is a clear indicator of a missing .fit
    # file. As of lately, the endpoint appears to have started to
    # respond with 500 "NullPointerException" on attempts to download a
    # .fit file for an activity without one.
    if response.status_code in [404, 500]:
        # Manually entered activity, no file source available
        log.error("Wellness file is not exist.")
        return None, None
    if response.status_code != 200:
        raise Exception(
            u"failed to get original activity file for {}: {}\n{}".format(
                day, response.status_code, response.text))
    
    path_elements = [save, filename]
    file_path = os.path.join(*path_elements)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    saved_zip.append(file_path)
    # sleeeeep for the server
    time.sleep(3)

    return None, None

def unzip_all():
    for zip in saved_zip:
        # mkdir
        zip_file_name = os.path.splitext(os.path.basename(zip))[0]
        log.info("Unzipping: " + zip_file_name)
        output_dir = os.path.join(save, zip_file_name)
        os.makedirs(output_dir, exist_ok=True)

        # unzip
        with zipfile.ZipFile(zip, 'r') as zf:
            zf.extractall(output_dir)

        # delete
        os.remove(zip)
    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Export all Garmin Connect activities")
    # positional args
    parser.add_argument(
        "username", metavar="<username>", type=str, help="Account user name.")
    # optional args
    parser.add_argument(
        "--password", type=str, help="Account password.")

    # from
    parser.add_argument(
        "--start", type=str, help="Start day (inc. this day.)")
    # to
    parser.add_argument(
        "--end", type=str, help="End day (inc. this day.)")

    # save path
    parser.add_argument(
        "--save", type=str, help="File save path")

    args = parser.parse_args()
    print(args)

    if not args.password:
        args.password = getpass.getpass("Enter password: ")

    save = args.save

    try:
        # args convert to datetime
        start_date = datetime.datetime.strptime(args.start, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(args.end, "%Y-%m-%d")
        with GarminClient(args.username, args.password) as client:

            while start_date <= end_date:
                log.info("Downloading: " + start_date.strftime("%Y-%m-%d"))
                get_wellness(client, start_date)
                start_date += datetime.timedelta(days=1)
            
        unzip_all()

    except Exception as e:
        log.error("failed with exception: %s", e)
    finally:
        log.info("done")