![SFGAD](https://raw.githubusercontent.com/sudrich/sf-gad/master/doc/img/logo.png)
---
[![Travis](https://api.travis-ci.com/sudrich/sf-gad.svg?branch=master)](https://travis-ci.com/sudrich/sf-gad)
[![PyPi](https://badge.fury.io/py/sfgad.svg)](https://badge.fury.io/py/sfgad)


SFGAD is a tool for detecting anomalies in **graph** and **graph streams** with python.


I provides:

* Efficient computation of graph **features**
* Statistical models for detecting **anomalous behavior**
* Graph scanning to detect **connected graph anomalies**
* A customizable detection framework with **6** components
* Several pre-defined **configurations**

### Process
---

![Process](https://raw.githubusercontent.com/sudrich/sf-gad/master/doc/img/sfgad.png)


### Installation
---

#### Dependencies

* Python: 3.5 or higher
* NumPy: 1.8.2 or higher
* SciPy: 0.13.3 or higher
* Pandas: 0.22.0 or higher
* NetworkX: 1.11.0 or higher

#### Installation

Installation of the latest release is available at the [Python
package index](https://pypi.org/project/sfgad).

```sh
pip install sfgad
```

The source code is currently available on GitHub:
https://github.com/sudrich/sf-gad

#### Testing

For testing use pytest from the source directory:

```sh
pytest sfgad
```

### Usage

The framework defines an modular interface that allows full customization of the analysis process. For examples, see the tutorials on [using a pre-defined analyzer](https://github.com/sudrich/sf-gad/blob/master/examples/predefined_analyzer.ipynb) and [using a custom analyzer](https://github.com/sudrich/sf-gad/blob/master/examples/custom_analyzer.ipynb).

## Acknowledgements

This work originated from the QuestMiner project (grant no. 01IS12051) and was partially funded by the German Federal Ministry of Education and Research (BMBF). The work was supported by the [SDIL](http://www.sdil.de), which also maintains, this code base within the BMBF SDI-X Project (grant no. 01IS15035A)
