import pandas as pd
import timeit
from faker import Faker
from faker.providers import ssn
import datetime

fake = Faker('pl_PL')
fake.add_provider(ssn)

def generate_ssns(n):
  i = 0
  pesel_list = []
  while i < n:
    pesel = fake.ssn()
    pesel_list.append(pesel)
    i += 1
  ser = pd.Series(pesel_list, copy=True)
  return ser


def validate_ssn(pesel:str, expected_sex, birthdate = 'NaN'):
  # bithdate format: 'DD.MM.YYYY'
  # expected_sex: {'male', 'female'}
  century_bonus = 0

  #check for PESEL lenght
  if len(pesel) != 11:
    print('Incorrect lenght of PESEL number')
    return

  #check for sex input
  if expected_sex not in ('male', 'female'):
    print('Incorrect input for sex, should be \'male\' or \'female\'')
    return

  if birthdate != 'NaN':
    date_format = '%d.%m.%Y'
    if len(birthdate) != 10:
      print("Incorrect birhtdate format, should be DD.MM.YYYY")
      return
    else:
      try:
        date_obj = datetime.datetime.strptime(birthdate, date_format)
      except ValueError:
        print("Incorrect birhtdate format, should be DD.MM.YYYY")
        return

  #checksum for PESEL
  weights_for_check_digit = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
  check_sum = sum([weights_for_check_digit[i] * int(pesel[i]) for i in range(len(pesel)-1)])
  if str(check_sum)[-1] != '0' and str(10-check_sum%10) != pesel[-1]:
    print('Checksum shows the PESEL number is wrong')
    return
  
 
  ###translation of PESEL into date and sex in a machine readable format
  #translating sex
  pesel_sex_number = int(pesel[9])

  #translating date
  #century_check and modification of month's first digit
  if int(pesel[2]) == (0, 1):
    century_bonus = 0
  elif int(pesel[2]) in (2, 3):
    century_bonus = 1
    pesel_month_digit_one = int(pesel[2]) - 2
  elif int(pesel[2]) == (4, 5):
    century_bonus = 2
    pesel_month_digit_one = int(pesel[2]) - 4

  pesel_year = 1900 + 100 * century_bonus + 10 * int(pesel[0]) + int(pesel[1])
  pesel_month = 10 * pesel_month_digit_one + int(pesel[3])
  pesel_day = 10 * int(pesel[4]) + int(pesel[5])
  
  #checking sex in PESEL
  if (pesel_sex_number % 2) == 1:
    pesel_sex = 'male'
  else:
    pesel_sex = 'female'
  
  #checking validity of sex between PESEL and input
  sex_check = (expected_sex == pesel_sex)

  #checking if birthdate is given and translating input to machine readable format
  if birthdate == 'NaN':
    birthdate_check_state = False
  else:
    birthdate_check_state = True
    birthdate_year = 1000 * int(birthdate[6]) + 100 * int(birthdate[7]) + 10 * int(birthdate[8]) + int(birthdate[9])
    birthdate_month = 10 * int(birthdate[3]) + int(birthdate[4])
    birthdate_day = 10 * int(birthdate[0]) + int(birthdate[1])

  #checking birthdate between PESEL and input
  if birthdate_check_state == True:
    birthdate_year_check = (birthdate_year == pesel_year)
    birthdate_month_check = (birthdate_month == pesel_month)
    birthdate_day_check = (birthdate_day == pesel_day)
    #final check for the whole date
    birthdate_check = (birthdate_year_check == True and birthdate_month_check == True and birthdate_day_check == True)


    #checking for date and sex 
    if birthdate_check == True and sex_check == True:
      print('PESEL is correct for given sex and birthdate')
      return True
    elif birthdate_check == True and sex_check == False:
      print('PESEL is correct for given birthdate, but is NOT correct for given sex')
      return False
    elif birthdate_check == False and sex_check == True:
      print('PESEL is correct for given sex, but is NOT correct for given birthdate')
      return False
    else:
      print('PESEL is NOT correct for given sex and birthdate')
      return False

  #check for just sex
  else:
    if sex_check == True:
      print('PESEL is correct for given sex')
      return True
    else:
      print('PESEL is NOT correct for given sex')
      return False

    
    

print(timeit.timeit("generate_ssns(10)",  setup="from __main__ import generate_ssns", number=1))
print(timeit.timeit("generate_ssns(100)",  setup="from __main__ import generate_ssns", number=1))
print(timeit.timeit("generate_ssns(1000)",  setup="from __main__ import generate_ssns", number=100))

print(timeit.timeit("for i in range(10):\n\tgenerate_ssns(1000)", setup="from __main__ import generate_ssns", number=1))
print(timeit.timeit("for i in range(100):\n\tgenerate_ssns(1000)", setup="from __main__ import generate_ssns", number=1))
print(timeit.timeit("for i in range(1000):\n\tgenerate_ssns(1000)", setup="from __main__ import generate_ssns", number=1))

#true inputs
validate_ssn('15270649970', "male", '06.07.2015')
validate_ssn('15270649970', "female", '06.07.2015')
validate_ssn('15270649970', "male", '07.07.2015')
validate_ssn('15270649970', "female", '06.04.2015')
validate_ssn('15270649970', "male")
validate_ssn('15270649970', "female")

#false inputs
validate_ssn('15270649970', "male", '06.25.2015')
validate_ssn('15270649970', "male", '06.7.2015')
validate_ssn('15270649970', "male", '6.07.2015')
validate_ssn('15270649970', "mal")
validate_ssn('15270649970', "femle", '06.25.2015')
