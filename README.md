![alt text](./Assets/csv_to_oracle_table.png)

# Fast way to turn a CSV file into a Oracle db table

## Prerequisites

### Python

### Python packages:

~~~Bash
$ pip install pandas
$ pip install cx_Oracle
$ pip install unidecode
~~~

## ImportCSV editing the Python file

### 1. Download the ImportCSV.py file.

<a href="https://github.com/gabrielquenu/csv_to_oracle_table/releases/download/Release/ImportCSV.py"><img alt="ImportCSV.py Download" src="./Assets/ImportCSV_py.png"></a>

### 2. Place it in the same folder that it is the CSV file.

### 3. Configure the variables in ImportCSV.py file.

![Variables Setup](./Assets/variables_setup.png)

### 4. Run the Python script.

~~~Bash
$ python ImportCSV.py
~~~

### Congratulations, your Oracle db table is ready!

## ImportCSV with input file

### 1. Download the ImportCSV_Input.py file.

<a href="https://github.com/gabrielquenu/csv_to_oracle_table/releases/download/Release/ImportCSV_Input.py"><img alt="ImportCSV_Input.py Download" src="./Assets/ImportCSV_Input_py.png"></a>

### 2. Place it in the same folder that it is the CSV file.

### 3. Run the Python script.

~~~Bash
$ python ImportCSV_Input.py
~~~

### 4. Insert the variables in terminal.

![Variables Input](./Assets/variables_input.png)

### Congratulations, your Oracle db table is ready!