#!/bin/bash

cd ./extractNeperInp
python3 extractData.py

cd ..

python3 generateInp.py
python3 generateProperty.py
