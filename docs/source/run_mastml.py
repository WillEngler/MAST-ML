#!/apps/share64/debian7/anaconda/anaconda-6/bin/python
from mastml import mastml_driver
import os
cwd = os.getcwd()

# Set paths for config file, data file and where to put output
conf = os.path.join(cwd,'tests/conf/example_input.conf')
csv = os.path.join(cwd,'tests/csv/example_data.csv')
output = os.path.join(cwd,'results/example_results')

# Start MASTML session
mastml_driver.main(conf, csv, output)