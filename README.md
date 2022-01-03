<p align="center">
  <a href="https://kirgizov.link/teaching/esirem/advanced-information-systems-2021/TP-PROJET.pdf" target="blank"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Masala_Chai.JPG/280px-Masala_Chai.JPG" width="320" alt="Thaï" /></a>
</p>

# TCHAI-JULIEN-BOULLY-YOUSSEF-TALEB

***
[![pypi](https://img.shields.io/pypi/v/sysbus.svg)](https://pypi.python.org/pypi/sysbus)
[![pypi](https://img.shields.io/pypi/pyversions/sysbus.svg)](https://pypi.python.org/pypi/sysbus)
[![MIT License](https://img.shields.io/github/license/rene-d/sysbus.svg?logoColor=silver&logo=open-source-initiative&label=&color=blue)](https://github.com/rene-d/sysbus/blob/master/LICENSE)
## Description

* <p>Objective: to design an electronic transaction system with guaranteed integrity using HTTP. The project uses a local SQLite database. </p>

* <p>TP subject: <a href="https://kirgizov.link/teaching/esirem/advanced-information-systems-2021/TP-PROJET.pdf" target="blank">kirgizov.link - TP-PROJET.pdf</a></p>


## Project structure

* <p> Project versions: each version of the project is on its own branch ("project v1" is on the branch "v1").</p>

* <p> The project offers a web interface. All the Html and CSS files are contained in the folders "static" and "templates" </p> 

* <p> The file "config.json" contains the configuration of the project.</p>

## Project features

There is two main features of the project:

* <p> An HTTP API: when the app is run, we can use HTTP requests to call the API in the format "127.0.0.1:5000/api/...".</p>

* <p> A web interface: a simple web interface accessible on the browser with the address "127.0.0.1:5000". It uses the API the interact with the local database.</p>


## Installation

Create database :
```bash
python3 create_database.py
```

## Running the app

```bash
python3 api_http.py
```

<p> If it is the first time to run the app, we advise to run also the script "create_database.py". 
It will create a fresh SQLite database locally with 2 transactions </p>

```bash
python3 create_database.py
```

## Test

The scripts to attack the system are contained in the folder "tests".
For example, to attack the first version of the project, we run the program "test_script_attack_v1.py":
```bash
python3 test_script_attack_v1.py
```

#### Details
* Version 1 attack: the script "test_script_attack_v1.py" aims to change the data stored in the database. In fact, the program updates the first transaction by modifying the amount of the transaction with an SQLite "update" request. The new amount is set randomly. 


## License
TCHAI-JULIEN-BOULLY-YOUSSEF-TALEB is [MIT licensed](LICENSE).

## Authors
* Julien BOULLY - julien_boully@etu.u-bourgogne.fr
* Youssef TALEB - youssef_taleb@etu.u-bourgogne.fr
