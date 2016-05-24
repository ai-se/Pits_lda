#! /bin/tcsh

rm err/* # Flush error logs
rm out/* # Flush output logs
rm log/*
rm dump/*

#datasets name
foreach VAR ("F3CR7pop10" "F7CR3pop10" "F7CR3pop30" "F3CR7pop30")
  bsub -W 6000 -n 8 -o ./out/$VAR.out.%J -e ./err/$VAR.err.%J /share/aagrawa8/miniconda/bin/python2.7 DE_hpc_wiki.py _test "$VAR" > log/"$VAR".log
end
