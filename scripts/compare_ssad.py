#!/usr/bin/python

'''
Script to compare ssads
'''

__author__ = "Mark Wilber"
__copyright__ = "Copyright 2012, Regents of the University of California"
__credits__ = ["John Harte"]
__license__ = None
__version__ = "0.1"
__maintainer__ = "Mark Wilber"
__email__ = "mqw@berkeley.edu"
__status__ = "Development"

gui_name = '''SSAD Analysis'''

summary = '''Compares a dataset's observed ssad(s) against theoretical ssads'''

explantion = '''This script takes in a dataset(s) and a list of distributions
to which the observed dataset(s)'s ssads will be compared.  The required
parameters for this script are the following: 

'subset' : How one would like to initially subset his data (see DataTable 
class docstring). 

'criteria' : How one would like to divide her dataset when caluculating the 
ssad(s). The theoretical distributions are compared against every ssad that is 
generated from the cutting specified in this parameter.  See Patch class 
docstring for details

'dist_list' : The list of distributions to which one could compare her observed
ssad(s).  The full list of distributions can be found in distributions.py

'rarity_measure' : This parameter specifies what the user would like to
consider rare for a given analysis.  For example, setting this parameter to
[10, 1] would specify that the user would like to consider all counts less than
or equal to 10 as rare and all counts less than or equal to 1 as rare.

This script outputs a summary file for the ssad for each species given the
divisions specified in criteria. a rank-abundance plot, a cdf plot and data 
files with the rank-abundance distributions used to build the rank-abundance 
plots and the cdf plots.  A species unique identifier can be found in the file
names and in the graph titles'''

required_params = {'subset' : 'Dictionary of initial subsets', 'criteria' :
        'Dictionary of how to split the data', 'dist_list' : 'List of' +\
        'distributions to compare',
        'rarity_measure' : 'A list of values to consider rare'}

if __name__ == '__main__':

    import logging
    from macroeco.utils.workflow import Workflow
    from macroeco.empirical import Patch
    import macroeco.compare as comp
    from macroeco.output import DistOutput

    wf = Workflow(required_params=required_params, clog=True, 
                                                            svers=__version__)
    
    for data_path, output_ID, params in wf.single_datasets():

        patch = Patch(data_path, subset=params['subset'])
        ssad = patch.ssad(params['criteria'])

        cmpr = comp.CompareDistribution(ssad, params['dist_list'],patch='ssad')
        rads = cmpr.compare_rads()

        sout = DistOutput(output_ID, 'ssad')
        sout.write_summary_table(cmpr.summary(rads,
                   mins_list=params['rarity_measure']), criteria=cmpr.spp_list)
        sout.plot_rads(rads, criteria=cmpr.spp_list)
        sout.plot_cdfs(cmpr.compare_cdfs(), cmpr.data_list,
                        criteria=cmpr.spp_list)
        logging.info('Completed analysis %s\n' % output_ID)
    logging.info("Completed 'compare_sad.py' script")




        








