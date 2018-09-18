import os
from datetime import timedelta, datetime
import shutil
import subprocess
import time

from .utils import daterange
from .write_inputfile import generate_inputfile
from .write_scriptfile import write_file


def run_name(params):
    """
    This is the function to actually run NAME
    :param params: input parameters
    :param response: the WPS response object
    :return: names of the output dir and zipped file
    """

    # replace any white space in title with underscores
    params['title'] = params['title'].replace(' ', '_')
    params['title'] = params['title'].replace(',', '')
    params['title'] = params['title'].replace('(', '')
    params['title'] = params['title'].replace(')', '')

    runtype = "FWD"
    if params['runBackwards']:
        runtype = "BCK"

    params['runid'] = "{}_{}".format(datetime.strftime(params['startdate'], "%Y-%m-%d"),
                                     datetime.strftime(params['enddate'], "%Y-%m-%d"))

    params['outputdir'] = os.path.join(params['outputdir'], params['runid'])

    if os.path.exists(params['outputdir']):
        shutil.rmtree(params['outputdir'])

    os.makedirs(params['outputdir'])
    os.makedirs(os.path.join(params['outputdir'], 'inputs'))
    os.makedirs(os.path.join(params['outputdir'], 'outputs'))

    # Will write a file that lists all the input parameters
    with open(os.path.join(params['outputdir'], 'user_input_parameters.txt'), 'w') as ins:
        for p in sorted(params):
            if p == 'outputdir':
                continue
            ins.write("%s: %s\n" % (p, params[p]))

    # Will loop through all the dates in range, including the final day
    for i, cur_date in enumerate(daterange(params['startdate'], params['enddate'] + timedelta(days=1))):
        os.makedirs(os.path.join(params['outputdir'], 'met_data', "input{}".format(i+1)))
        with open(os.path.join(params['outputdir'], "inputs", "input{}.txt".format(i+1)), 'w') as fout:
            fout.write(generate_inputfile(params, cur_date, i+1))

    with open(os.path.join(params['outputdir'], 'script.bsub'), 'w') as fout:
        fout.write(write_file(params, i+1))

    # TODO: We'll insert the commands to run NAME here.
    print("Running NAME...")
    cat = subprocess.Popen(['cat', os.path.join(params['outputdir'], 'script.bsub')], stdout=subprocess.PIPE)
    runbsub = subprocess.Popen('bsub', stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=cat.stdout)
    sout, serr = runbsub.communicate()
    jobid = sout.split(' ')[1].replace('>', '').replace('<', '')
    jobrunning = True
    while jobrunning:
        time.sleep(30)
        checkjob = subprocess.check_output('bjobs')
        if jobid in checkjob:
            print("Job %s is still running" % jobid)
            processesrunning = 0
            for l in checkjob.split('\n'):
                if jobid in l:
                    processesrunning += 1
            percentcomplete = (((i+1)-processesrunning)/float(i+1))*100
            print "{}%".format(percentcomplete),
        else:
            jobrunning = False
    print("Done")

    return params['runid']
