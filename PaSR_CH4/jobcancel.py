
from subprocess import run

for i in range(4386851,4387001):
    run(['scancel','{:d}'.format(i)])
