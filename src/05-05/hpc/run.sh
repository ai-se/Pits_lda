#! /bin/tcsh

rm err/* # Flush error logs
rm out/* # Flush output logs
rm log/*
rm dump/*

#datasets name
foreach VAR ("101pitsA_2.txt" "101pitsB_2.txt" "101pitsC_2.txt" "101pitsD_2.txt" "101pitsE_2.txt" "101pitsF_2.txt")
  bsub -W 6000 -n 8 -o ./out/$VAR.out.%J -e ./err/$VAR.err.%J /share/aagrawa8/miniconda/bin/python2.7 DE_hpc.py _test "$VAR" > log/"$VAR".log
end
