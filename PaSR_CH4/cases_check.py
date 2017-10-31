"""
Zhen Lu 2017/10/21
Check case status
"""
import subprocess
import os

date_start = '2017-10-21'
date_end = '2017-10-22'
jobid_lb = 4316037
jobid_ub = 4316518

# output files
list_fail = open('list_fail.op','w')
list_comp = open('list_completed.op','w')
list_time = open('list_timeout.op','w')
list_step1500 = open('list_step1500.op','w')
 
# get job status
sqout = subprocess.run(['sacct','-S',date_start,'-E',date_end,'-u','luz0a','-b'],
        check=True,
        stdout=subprocess.PIPE).stdout

lines = str( sqout, 'utf-8' ).split('\n')

jobs = {}

num_run = 0
num_comp = 0
num_fail = 0
num_time = 0

for line in lines:

    job = line.split()
    # skip empty lines
    if not job: continue
    try:
        jobid = int(job[0])
    except ValueError:
        continue

    # store the jobid and status
    if jobid > jobid_lb and jobid < jobid_ub:

        job_status = job[1]

        # get job location and name based on the jobid
        file_name = 'job{:7d}.out'.format(jobid)
        sqout = subprocess.run(['find','-name',file_name],
                check = True,
                stdout = subprocess.PIPE).stdout
        file_loc = str(sqout,'utf-8')
        job_name = file_loc[2:file_loc.find(file_name)-1]

        # check steps
        os.chdir(job_name)
        try:
            with open('means.dat','r') as f:
                job_steps = len(f.readlines())-2
        except OSError:
            subprocess.run(['sbatch','run_shaheen.sh'])
            job_steps = 0
        os.chdir('..')

        jobs[jobid] = [job_status,job_name,job_steps]

        if job_status == 'COMPLETED':
            num_comp += 1
            list_comp.write('{0}\n'.format(job_name))
        elif job_status == 'FAILED':
            num_fail += 1
            list_fail.write('{0}\t{1:g}\n'.format(job_name,job_steps))
        elif job_status == 'TIMEOUT':
            num_time += 1
            list_time.write('{0}\t{1:g}\n'.format(job_name,job_steps))
        else:
            num_run += 1

        if job_steps > 1500 :
            list_step1500.write('{}\n'.format(job_name))

print('Numbers of FAILED jobs: {:g}'.format(num_fail))
print('Numbers of COMPLETED jobs: {:g}'.format(num_comp))
print('Numbers of RUNNING jobs: {:g}'.format(num_run))
print('Numbers of TIMEOUT jobs: {:g}'.format(num_time))

list_fail.close()
list_comp.close()
list_time.close()
list_step1500.close()
