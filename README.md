# qpAdm-Rotate version 1.0.1 (01-Sep-22) (For Python3+, Linux & Mac)
Python script to run rotating qpAdm models for admixture based on qpfstats output

This package will help implement multiple qpAdm (package Admixtools necessary, install separately from https://github.com/DReichLab/AdmixTools) rotation models and collate the output to a CSV file in a neat format.

This package contains one script file.
1. qpadmrotate.py

and sample files: parqpadm (param file), excl (excludelistfile), fstats6.txt (qpfstats output), lista (All labels in fstats6,txt present here)

________________

HOW TO INSTALL

Download the script file and save it in your working folder. That is all.
Needs the itertools module, combinations function.
_ _ _ _ _ _ _ _

HOW TO CALL THE SCRIPT


Navigate to working folder, call: 
python3 qpadm_rotate.py --poplist poplistfilename --target targetlabel --nsources (integer, number of sources at a time) --parfile NameofqpadmParameterfile --out nameofoutputfile.csv --totalexclude excludelistfilename,optional parameter --excludesrc exludesourcesfilename, optional --fixsrc fixedsourcesfilename, optional

for help: python3 qpadmrotate.py --help
_ _ _ _ _ _ _ _ _ _ _ _


parfile - required in working folder (format given below)

fstatsname:   <name of output file from qpfstats> (geno.snp/ind not accepted, qpfstats has to be run manually by user before rotate is run)
popleft:       left ## dont change name, file will be automatically created
popright:      right ## use same name, file will be automatically created
details: YES
_______

Poplistfile - required in working folder

1 population label per line. 
Ensure all labels in this file are included in qpfstats run before this. If label is unavailable in qpfstats output or if spelling is different, script will fail.
1st population is Outgroup, it will not be used as one of the sources. 
___________
  
  
Excludelistfile - required only if parameter is used

1 population label per line. 
If you want to remove any label in poplistfile from both left and right, use this option.
Optional parameter. otherwise all labels in Poplistfile will be used in either left or right.
___________
  
Excludesourcesfile - required only if parameter is used

1 population label per line. 
If you want to prohibit any label in poplistfile from use in sources (but keep in right pops), use this option.
Optional parameter. otherwise all labels in Poplistfile will be used in either left or right.
___________

Fixedsourcesfile - required only if parameter is used

1 population label per line. 
If you want to fix some sources and rotate the other remaining sources, use this option. Number of labels in file must be less than nsources.
Optional parameter. otherwise all labels in Poplistfile will be used in either left or right.
___________

qpfstats()

Prerequisite is availabaility of qpfstats output file. Refer Admixtools github for help.
_______________


eg. python3 qpadmrotate.py --poplist lista --target Yamnaya_Samara --nsources 3 --parfile parqpadm --out rotate_output.csv --totalexclude excludelistfilename --excludesrc excsourcefilename --fixsrc fixsourcefilename


__________________________________________________________________________________________________________________________________________________________

This is a fresh script, there may be bugs. Please raise issue if you experience any.
