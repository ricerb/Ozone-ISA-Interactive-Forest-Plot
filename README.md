# Ozone ISA Interactive Forest Plot Prototype

A Python Dash app presenting epidemiological study results from the 2019 draft Ozone ISA in a filterable format.

## Requirements

Using python 3.6 or higher:

```bash
# clone repo
git clone https://github.com/ricerb/Ozone-ISA-Interactive-Forest-Plot.git
cd Ozone-ISA-Interactive-Forest-Plot

# create python virtual environment
python -m venv venv

# activate environment
# (on mac/linux):
source venv/bin/activate
# (or on windows):
# venv\Scripts\activate

# update pip and install requirements
python -m pip install -U pip
pip install -r ./requirements.txt
```

To run the application:

```bash
python fp_ozone_resp.py
```

## Usage

Data from tables 3-13 (Hospital Admissions for Asthma) and 3-14 (Emergency Department Visits for Asthma) in the 2019 Ozone ISA (draft) are presented in a filterable format in this Python Dash app. This is intended as a proof of concept for evaluating the usefulness of an interactive data visualization in future digital assessments. Note that study results presented as relative risk or percent increase values were converted to odds ratios to create this app.

All options are selected for each drop down when the app is loaded. To filter the forest plot, click the "X" beside each value. Values can be added back to the figure by clicking the down arrow to the right of each field and selecting from the dropdown list.
