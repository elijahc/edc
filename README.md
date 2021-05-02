# edc
My portable personal library for loading datasets and utils

## Installation

```bash
pip install git+https://github.com/elijahc/edc
```

## Datasets

### National Hospitalized Ambulatory Care Survey

The National Hospital Ambulatory Medical Care Survey (NHAMCS) is designed to collect data on the utilization and provision of ambulatory care services in hospital emergency and outpatient departments and ambulatory surgery locations. Findings are based on a national sample of visits to the emergency departments,  outpatient departments, and ambulatory surgery locations of noninstitutional general and short-stay hospitals.

#### Usage

To load most recent year of published emergency department data:

```python
from edc.datasets import nhamcs
emergency = nhamcs.ed.load_data()
```

Or you can select years:

```python
from edc.datasets import nhamcs
emergency = nhamcs.ed.load_data(year=[2017,2018])
```

Outpatient data can be loaded similarly:

```python
from edc.datasets import nhamcs
outpatient = nhamcs.opd.load_data()
```


### National Ambulatory Medical Care Survey

The National Ambulatory Medical Care Surveys (NAMCS) supplydata on ambulatory medical care provided in physicians' offices. The 2006 survey contains information from 29,392 patient visits to 1,455physicians' offices. Data are available on the patient's smokinghabits, reason for the visit, expected source of payment, thephysician's diagnosis, and the kinds of diagnostic and therapeuticservices rendered. Other variables cover drugs/medications ordered,administered, or provided during office visits, with information onmedication code, generic name and code, brand name, entry status,prescription status, federal controlled substance status, compositionstatus, and related ingredient codes. Information is also included onthe physician's specialization and geographic location. Demographicinformation on patients, such as age, sex, race, and ethnicity, wasalso collected. In addition, the 2006 survey contains two new sampling strata which are from 104 Community Health Centers (CHCs) and 200 oncologists.

See [Cookbook](https://www.icpsr.umich.edu/SDA/NACDA/28403-0001/CODEBOOK/NMCS.htm) here for data dictionary and data management plan

#### Usage


```python
from edcutils.datasets import namcs

private_practice = namcs.load_data(year=[2013,2014])
```
> Downloading data from ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/dataset_documentation/namcs/spss/namcs2013-spss.zip