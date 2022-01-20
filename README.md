# PESEL-validation

22/12/2021

Simple script checking validity of Polish PESEL number. First part generates PESEL numbers and checks performance of generating function with timeit library.
Second part uses a defined function to check the validity of PESEL number. Inputs are: PESEL number as string, male/female, (optional) date in format of DD.MM.YYYY. If date is not given the validation function will check just sex and checksum of the PESEL number. Date must be in the input to be checked. Proper error messages will be shown when input is incorrect.

Script was developed in Google Colaboratory. It requires pandas and faker libraries.
