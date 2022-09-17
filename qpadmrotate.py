import argparse
import csv
import subprocess
import sys
from itertools import combinations

parser = argparse.ArgumentParser(description='Run qpAdm Rotation models')

parser.add_argument('--poplist', type=str, required=True,
                    help='Name of File with list of pops')
parser.add_argument('--target', type=str, required=True,
                    help='target Label for qpAdm')
parser.add_argument('--nsources', type=int, required=True,
                    help='Type number of sources to test')
parser.add_argument('--parfile', type=str, required=True,
                    help='Type name of parameter file')
parser.add_argument('--out', type=str, required=True,
                    help='Type name of output csv file, with.csv')
parser.add_argument('--totalexclude', type=str, required=False,
                    help='Optional: Filename of pops to exclude from left and right')
parser.add_argument('--excludesrc', type=str, required=False,
                    help='Optional: Filename of pops to exclude from only left as source')
parser.add_argument('--fixsrc', type=str, required=False,
                    help='Optional: Filename of pops to forcefully include as source')

args = parser.parse_args()
qpadmargs = ("qpAdm", "-p", args.parfile)

with open(args.poplist, 'r') as popfile:
    pops = popfile.read().splitlines()

pops = list(s.strip() for s in pops)
pops = list(filter(None, pops))

if args.totalexclude is not None:
    with open(args.totalexclude, "r") as excludelist:
        excludepops = excludelist.read().splitlines()
    excludepops = list(s.strip() for s in excludepops)
    excludepops = list(filter(None, excludepops))

    for m in excludepops:
        if m == args.target:
            sys.exit("Target label also present in TotalExclude pops")
        try:
            pops.remove(m)
        except (Exception,):
            sys.exit("Label in ExcludePops not present in Poplist. Exiting.")

try:
    pops.remove(args.target)  # Remove target from list of source
except (Exception,):
    sys.exit("Target not present in Poplist")

pops_dup = list(pops)
outgroup = pops.pop(0)
# Remove Mbuti.DG or similar outgroup pop from potential sources and also store it as outgroup for use in right pop
# file later

header = ['SNo', 'Target', 'Chisq', 'PValue']

# Create 1st row of Output CSV File with headers
for i in range(args.nsources):
    globals()['Source%s' % (i + 1)] = ""
    header.append("Source" + str(i + 1))
for i in range(args.nsources):
    header.append("S" + str(i + 1) + "%")
for i in range(args.nsources):
    header.append("Src" + str(i + 1) + "SE")
# Create 1st row of Output CSV File with headers


with open(args.out, 'w+') as output:
    writer = csv.writer(output)
    writer.writerow(header)

if args.excludesrc is not None:
    with open(args.excludesrc, "r") as sourceexcludelist:
        excludedsources = sourceexcludelist.read().splitlines()
    excludedsources = list(s.strip() for s in excludedsources)
    excludedsources = list(filter(None, excludedsources))

    for m in excludedsources:
        if m == args.target:
            sys.exit("Target label also present in ExcludedSources pops")
        try:
            pops.remove(m)
        except (Exception,):
            print(m)
            sys.exit("Above Label in ExcludedSource is either Outgroup or not present in Poplist. Exiting.")


fixsrcno = 0
if args.fixsrc is not None:
    with open(args.fixsrc, "r") as fixedsourcelist:
        fixedsources = fixedsourcelist.read().splitlines()
    fixedsources = list(s.strip() for s in fixedsources)
    fixedsources = list(filter(None, fixedsources))
    fixsrcno = len(fixedsources)
    if fixsrcno >= args.nsources:
        sys.exit("Fixed sources should be < nsources")

    for m in fixedsources:
        if m == args.target:
            sys.exit("Target cant be fixed source")
        try:
            pops.remove(m)
        except (Exception,):
            print(m)
            sys.exit("Label in FixedSources is Outgroup or is not present in Poplist. Exiting.")

# all combinations of sources from List, except Outgroup and target
sourcecomb = combinations(pops, args.nsources - fixsrcno)
sno = 1  # counter for serial number of model

for j in list(sourcecomb):
    count = 0  # counter for Name of source in model

    # write left list
    with open('left', 'w+') as left:
        j = list(j)
        j.insert(0, args.target)
        if args.fixsrc is not None:
            for z in fixedsources:
                j.append(z)
        for items in j:
            if count > 0:
                globals()['Source%s' % count] = j[count]  # write names of sources for this model

            count = count + 1
            left.writelines(items + '\n')
            # left list writing over

    # Create rightpop set for this model
    j = set(j)
    pops1 = set(pops)
    rightrefs = list(pops1.difference(j))
    rightrefs.insert(0, outgroup)
    if args.excludesrc is not None:
        for k in excludedsources:
            rightrefs.append(k)
    with open('right', 'w+') as right:
        for items in rightrefs:
            right.writelines(items + '\n')

    # right pops file writing over

    # starting qpAdm
    popen = subprocess.Popen(qpadmargs, stdout=subprocess.PIPE)
    popen.wait()

    output = str(popen.stdout.read(), 'utf-8')

    index = output.find("fixed pat")
    index2 = output.find('\n', index)
    index3 = output.find('\n', index2 + 1)
    s = output[index2 + 3:index3]
    spl = s.split()

    index4 = output.find("std. errors:")
    index5 = output.find('\n', index4)
    stderrorline = output[(index4 + 12):index5]
    stderrors = stderrorline.split()

    header = [sno, args.target, spl[3], spl[4]]
    sno = sno + 1
    infeas = ""
    for k in range(args.nsources):
        header.append(globals()['Source%s' % (k + 1)])
    for k in range(args.nsources):
        if float(spl[5 + k]) < -0.03:
            infeas = "Infeasible"
        header.append(spl[5 + k])
    for k in range(args.nsources):
        header.append(stderrors[k])
    header.append(infeas)

    with open(args.out, 'a') as output:
        writer = csv.writer(output)
        writer.writerow(header)
