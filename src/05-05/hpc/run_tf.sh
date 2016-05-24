#! /bin/tcsh

rm err/* # Flush error logs
rm out/* # Flush output logs
rm log/*
rm dump/*

#datasets name
foreach VAR ("newab" "newac" "newad" "newae" "newaf" "newag" "newah" "newai" "newaj" "newak" "newal" "newam" "newan" "newao" "newap" "newaq" "newar" "newas" "newat")
  bsub -W 6000 -n 8 -o ./out/$VAR.out.%J -e ./err/$VAR.err.%J /share/aagrawa8/miniconda/bin/python2.7 so_tfidf_extracter.py _test "$VAR" > log/"$VAR".log
end
