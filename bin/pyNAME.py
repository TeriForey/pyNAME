#! /usr/bin/env python

import argparse
import ConfigParser
from pyname.run_name import run_name
from pyname.create_plots import plot_all
from datetime import datetime

def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def parse_config(configfile):
    """
    Parse config file and test all options are present and valid
    :return: config parser object
    """
    cparser = ConfigParser.SafeConfigParser()
    cparser.read([configfile])

    args = {}

    if cparser.has_section('data') and cparser.has_section('jasmin'):
        pass
    else:
        raise Exception("Config file needs to contain a section called 'data' and a section called 'jasmin'")

    data_options = ['title', 'longitude', 'latitude', 'elevation', 'elevation_out', 'backwards', 'ndays',
                    'resolution', 'outputdir']
    for option in data_options:
        if cparser.has_option('data', option):
            args[option] = cparser.get('data', option)
        else:
            raise Exception("Config file is missing option '%s' in section 'data'" % option)

    jasmin_options = ['namedir', 'topodir', 'utilsdir']
    for option in jasmin_options:
        if cparser.has_option('jasmin', option):
            args[option] = cparser.get('jasmin', option)
        else:
            raise Exception("Config file is missing option '%s' in section 'jasmin'" % option)

    # Check no exceptions are raised with non-string values
    args['runBackwards'] = cparser.getboolean('data', 'backwards')
    args['longitude'] = cparser.getfloat('data', 'longitude')
    args['latitude'] = cparser.getfloat('data', 'latitude')
    args['elevation'] = cparser.getint('data', 'elevation')
    args['time'] = cparser.getint('data', 'ndays')
    args['resolution'] = cparser.getfloat('data', 'resolution')
    args['domain'] = [float(x) for x in cparser.get('data', 'domain').split(', ')]
    args['elevationOut'] = [tuple([int(x) for x in cparser.get('data', 'elevation_out').split('-')])]

    return args


def main():
    """
    Main function that will run NAME and generate plots
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('config', help='configuration file')
    parser.add_argument('startdate', type=valid_date, help='start date to run from - Format YYYY-MM-DD')
    parser.add_argument('enddate', type=valid_date, help='end date to run to (inclusive) - Format YYYY-MM-DD')
    args = parser.parse_args()

    configs = parse_config(args.config)
    configs['startdate'] = args.startdate
    configs['enddate'] = args.enddate
    configs['timeFmt'] = 'days'
    configs['timestamp'] = '3-hourly'

    print "Settings"
    for k, v in configs.items():
        print("%s: %s" % (k, v))
    print

    run_name(configs)

    plot_all(configs)

    print("All done!")
    return


if __name__ == "__main__":
    main()
