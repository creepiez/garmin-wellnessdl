# About
garmin-wellnessdl is bulk daily wellness `*.fit` file downloader.
After downloading this script automatically unzip downloaded file.

# Important
This project is now archived.
The wellness download uri/service in the Garmin Connect is not available. (returns 402.)

# Prerequisite
Install `garminexport`; see ref [garminexport](https://github.com/petergardfjall/garminexport)

## Enviroment
I had checked with below conditions.
- Python 3.10
- Windows 10, Ubuntu 22

# Usage
Commandline like:
```
python3 garmin-wellnessdl.py your@email --password pwd --start 2023-1-1 --end 2023-1-2 --save /path/to/save
```
All arguments are all not options.
I thing you can guess all arguments by names ;)
