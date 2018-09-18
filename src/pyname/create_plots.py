import os
from pynameplot import Name, drawMap
import glob


def plot_all(inputs):
    """
    Plot all of the datapoints for all of the output files using pyNAMEplot
    :param inputs: running args
    :return:
    """

    rundir = inputs['outputdir']

    # Parse input params into plot options
    plotoptions = {'station': (inputs['longitude'], inputs['latitude'])}

    plotoptions['outdir'] = os.path.join(rundir, "plots")

    files = glob.glob(os.path.join(rundir, 'outputs', '*_group*.txt'))
    if len(files) == 0:
        raise Exception("Unable to find any output files to plot. File names must be named '*_group*.txt'")

    print("Plot options: %s" % plotoptions)

    for filename in os.listdir(os.path.join(rundir, 'outputs')):
        if '_group' in filename and filename.endswith('.txt'):
            n = Name(os.path.join(rundir, 'outputs', filename))
            for column in n.timestamps:
                plotoptions['outfile'] = "name_%s_%s_%s_%sdayback_%sm.png" % (inputs['title'],
                                                                                  filename.split('_')[0],
                                                                                  column.split(' ')[1].replace(':', ''),
                                                                                  inputs['time'],
                                                                                  inputs['elevation_out'])
                try:
                    drawMap(n, column, **plotoptions)
                except:
                    print("Failed to plot %s" % column)

    return
