import shutil
import os
import __main__
import sys

if 'Z://ann//' not in sys.path:
    sys.path.append('Z://ann//')

####################### python script 저장 ##########################

if hasattr(__main__, '__file__'):
    mainfile = __main__.__file__
    print(mainfile)
else:
    mainfile = None

# fullfoldername = 'D:\\Research\\Python_practice\\'

currentpath = os.getcwd() 
scriptname     = 'copy_test_2022-12-22.py'

if mainfile != None :
        shutil.copyfile(mainfile,
                        os.path.normpath(currentpath + "/" +  scriptname))
else:
    raise('스크립트 저장 중 에러 발생!')
    
######################################################################