#!/usr/bin/python

'''
Script to compare sars
'''

__author__ = "Mark Wilber"
__copyright__ = "Copyright 2012, Regents of the University of California"
__credits__ = ["John Harte"]
__license__ = None
__version__ = "0.1"
__maintainer__ = "Mark Wilber"
__email__ = "mqw@berkeley.edu"
__status__ = "Development"

import macroeco.utils.global_strings as gb

gui_name = '''EAR'''#''' Analyze Species-Area Relationships'''

summary = '''Compares a dataset's observed species-area relationships against 
theoretical species-area relationships'''

columns_to_divide = '''\nThis parameter specifies which spatial columns you would
like to divide for the EAR analysis.  For example, if your data had spatial
columns 'x' and 'y' you would enter: ('x', 'y') '''

list_of_divisions_on_columns = '''\nThis parameter specifies how you would like
to divide the columns you named in the columns_to_divide parameter.  For
example, if you specified that you wanted to divide on columns 'x' and 'y' in
the parameter columns_to_divide and you wanted to divide your plot into fourths
and eighths you would input: [(2,2), (2,4)].  The first value splits the plot
into fourths and the second splits the plot into eighths.  The values within
each parentheses are divisions on 'x' and 'y', respectively.  Please note that
the number of species of the entire plot will be calculated even if you do not
enter the division (1,1).'''

predicted_EAR_curves = '''\nA list of EAR curves to which you can compare your
observed data.

In addition, you may combine any of the following SADs and SSADs:


SADs:
{0}

SSADs:
{1}

Please specify the SAD name followed by a '-' and then the SSAD name.

Example input: ['lognorm-binm', 'nbd_lt(k=1)-tgeo']  
'''.format(gb.SAD_distributions, gb.SSAD_distributions)

name = '''\nA name for the plot that will be generated.

Example input: My EAR Plot  
'''

explanation = '''ANALYSIS EXPALANTION\n
The compare_ear analysis allows you to compare observed endemic species-area
relationships (EAR) with any number of predicted EARs.  An EAR is a commonly
used macroecological metric which examines the number of endemic species found
in a given area. All EAR curves show increasing endemic species with increasing
area, but shape of this increasing curve differs depending on the theory used
to derive it. It is common practice to examine EAR plots on a log-log scale
because the curve often becomes close to a straight line. Using this analysis,
you can generate the observed EARs for any nested plots within your data.  For
example, if you had a fully censused plot with spatial coordinates x,y and you
wanted to examine an EAR looking at the anchor area (A), 1/2 * A, 1/4 * A, and
1/8 * A, you would input the appropriate parameters and this analysis would
divide the plot into halves, fourths, and eighths and take the average number
of endemic species across all of the smaller plots. Therefore, you can have a
fractional average number of endemic species per areas. For additional
information on EARs, please see the provided references and the references
therein.

OUTPUT

The compare_ear analysis outputs one folder per dataset, a logfile.txt, and, if
possible, a map of the location(s) of the dataset(s).  The folder has the name
ear_plots_compare_ear_* and contains a log(endemic species) vs. log(area
fraction) plot as a .png file.  Area fraction means that the anchor area
(largest area) for the plot is 1 and all smaller subplots are fractions less
than one. Each plot will have the observed EAR and any EAR generated by a
predicted EAR specified in the predicted_EAR_curves parameter. In addition to
this plot, this analysis will output csv files with the same file name as the
plot, but with the name of the predicted EAR appended to the end.  These files
contain the data for the given EAR used to make the plot.  For example, if you
choose two predicted EARs and run the analysis, you will get three csv files:
two with the predicted EAR data and one with the observed data. With these
files, you can re-plot the data in anyway you chose.  Please note that the file
names provide a detailed description of each file and should provide you with a
basic understanding of what the file contains.

The logfile.txt contains the analysis process information. Please see the
logfile if the analysis fails.


PARAMETER EXPLANATIONS

*** subset ***:

{0}

*** criteria ***:

{1}

For the compare_ear analysis (this analysis), you DO NOT need to enter your
divisions in the 'criteria' parameter.  Instead, you enter them in the
'columns_to_divide' and 'list_of_divisions_on_columns' parameters.  If the
columns you entered in the parameter 'columns_to_divide' are repeated in the
parameter criteria, the values that you assigned in criteria will be ignored.
For example, if you want to divide the columns 'x' and 'y' for your EAR
analysis you would input them into columns to divide as ('x', 'y'). If you were
to give columns 'x' and/or 'y' a value in the 'criteria' parameter, it would
then be ignored. Generating multiple EARs is not yet implemented. 

*** columns_to_divide **

{2}

*** list_of_divisions_on_columns ***

{3}

*** predicted_EAR_curves ***

{4}

*** name ***

{5}

REFERENCES

Harte, J. 2011. Maximum Entropy and Ecology: A Theory of Abundance,
Distribution, and Energetics. Oxford University Press.

Rosenzweig, M. L. 1995. Species Diversity in Space and Time. Cambridge
University Press.

'''.format(gb.subset, gb.criteria, columns_to_divide,
list_of_divisions_on_columns, predicted_EAR_curves, name)


required_params = {'criteria' : gb.req + gb.short_criteria,
                   'columns_to_divide' : gb.req + columns_to_divide,
                   'list_of_divisions_on_columns' :
                   gb.req + list_of_divisions_on_columns,
                   'predicted_EAR_curves' : gb.req + predicted_EAR_curves}

optional_params = {'subset' : (gb.optional + gb.short_subset, {}), 'name' : 
                    (gb.optional + name, 'Plot')}

if __name__ == '__main__':

    import logging
    from macroeco.utils.workflow import Workflow
    from macroeco.empirical import Patch
    import macroeco.compare as comp
    from macroeco.output import SAROutput, make_directory
    from copy import deepcopy
    import os

    wf = Workflow(required_params=required_params,
                optional_params=optional_params, clog=True, svers=__version__)

    folder_name = 'EAR_analysis'
    make_directory(folder_name)
    cwd = os.getcwd()
    
    # Maps are going to be saved outside of analysis folder
    for data_path, output_ID, params in wf.single_datasets():

        os.chdir(os.path.join(cwd,folder_name))

        try:
            params['list_of_divisions_on_columns'].index((1,1))
        except:
            logging.info("Adding base area to parameter " +
                                       "'list_of_divisions_on_columns': (1,1)")
            params['list_of_divisions_on_columns'].append((1,1))
        sad_criteria = deepcopy(params['criteria'])

        for nm in params['columns_to_divide']:
            sad_criteria[nm] = 'whole'
        patch = Patch(data_path, subset=params['subset'])
        sad = patch.sad(sad_criteria, clean=True)
        sar = patch.sar(params['columns_to_divide'], 
                    params['list_of_divisions_on_columns'], params['criteria'],
                    form='ear')
        cmpr = comp.CompareSAR([sar], params['predicted_EAR_curves'],
                                        [sad[0][1]], patch=True)
        srout = SAROutput(output_ID)
        srout.plot_sars(cmpr.compare_curves(form='ear'), names=[params['name']],
                                                                    form='ear')
        logging.info('Completed analysis %s\n' % output_ID)

        os.chdir(cwd)
    
    os.chdir(os.path.join(cwd,folder_name))
    fout = open('README_compare_ear', 'w')
    with fout:
        fout.write(explanation)
    os.chdir(cwd)

    logging.info("Completed 'compare_ear' analysis")




        








