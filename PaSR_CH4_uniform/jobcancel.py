
import subprocess

date_start = '2017-11-17'
date_end = '2017-11-18'
jobid_lb = 4423675
jobid_ub = 4424346

# get job status
sqout = subprocess.run(['sacct',
                        '-S',date_start,
                        '-E',date_end,
                        '-u','luz0a',
                        '-b'],
                       check=True,
                       stdout=subprocess.PIPE
                       ).stdout

lines = str(sqout,'utf-8').split('\n')

for line in lines:

    job = line.split()
    # skip empty lines
    if not job: continue
    try:
        jobid = int(job[0])
    except ValueError:
        continue

    # cancel job
    if jobid >= jobid_lb and jobid <= jobid_ub:
        subprocess.run(['scancel','{:d}'.format(jobid)])
