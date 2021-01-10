# gpx2csv
`gpx2cvs` is a Python3 script to parse gpx file (XML schema for GPS data format for software applications), get element data from its tags "<trkpt>" (track points) and save the result on csv file. Moreover, it's possible to filter the parsed result from two variables speed range and stopover time. 
Finally, it's also possible to configure the column labels of the first row of output file CSV (csv_hedear) in the config/global_settings.py.

At the moment I only tested it with files similar to the one used for the sample.gpx tests, so the script should crash if it is analyzing something different from what expected ... otherwise, it is a bug.

The script is meant to be expandable to other formats in both input and output, so if I need to parse another file type I will update this.

## Usage

```
usage: gpx2csv [-h] [--stopping-time] [--speed-range ] [--output-path] filetoparse

Parse file and save the result in csv file with same name

positional arguments:
  filetoparse       If no path is specified the file will be searched in the current directory

optional arguments:
  -h, --help        show this help message and exit

  --stopping-time   (integer) is the value (in seconds) of how long a stopover should lasts for the vehicle or the user to be 
                    considered unmoving, eg. a car in the traffic makes many stops (generally short) and therefore cannot be considered parked.
                    *You must use it together with the speed-range eg. --stopping-time 600 --speed-range 0 5

  --speed-range     Are min and max values (in km/h) to consider the vehicle or the user unmoving. *You must use it together with   
                    the stopping-time eg. --stopping-time 600 --speed-range 0 5
                    
  --output-path     output directory, must exist. If no path is specified the file will be saved in the current directory
```

### Example

```
$ python gpx2csv.py sample.gpx --speed-range 0 5 --stopping-time 600 --output-path ~/Desktop
```
It will create in the output folder (`~/Desktop/`) the sample.csv file
