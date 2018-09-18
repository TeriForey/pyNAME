import os
from pynameplot import Name, drawMap
import glob
import shutil
import tempfile


def plot_all(inputs, runid):
    """
    Plot all of the datapoints for all of the output files using pyNAMEplot
    :param inputs: running args
    :return:
    """

    rundir = os.path.join(inputs['outputdir'], runid)

    # Parse input params into plot options
    plotoptions = {'station': (inputs['longitude'], inputs['latitude'])}

    plotoptions['outdir'] = os.path.join(rundir, "plots")

    files = glob.glob(os.path.join(rundir, 'outputs', '*_group*.txt'))
    if len(files) == 0:
        raise Exception("Unable to find any output files to plot. File names must be named '*_group*.txt'")

    print("Plot options: %s" % plotoptions)

    # We need to find all the groups and loop through them one at a time!
    groups = {}
    for filename in os.listdir(os.path.join(rundir, 'outputs')):
        groupnum = filename[14]
        try:
            groupnum = int(groupnum)
        except TypeError:
            raise Exception("Cannot identify groupnumber %s" % groupnum)

        if groupnum in groups:
            shutil.copy(os.path.join(rundir, 'outputs', filename), groups[groupnum])
        else:
            groups[groupnum] = tempfile.mkdtemp()
            shutil.copy(os.path.join(rundir, 'outputs', filename), groups[groupnum])

    for groupnum, tmpdir in sorted(groups.items()):
        for filename in os.listdir(tmpdir):
            if '_group' in filename and filename.endswith('.txt'):
                n = Name(os.path.join(tmpdir, filename))
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

        # Finished plotting so will now delete temp directory
        shutil.rmtree(tmpdir)

    return
