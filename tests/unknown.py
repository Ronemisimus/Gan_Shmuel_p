
from subprocess import check_output
import subprocess


ret_code = subprocess.call(['ls','-a'])
print(ret_code)