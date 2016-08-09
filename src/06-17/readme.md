- All the logs (runtime, parameter variation, stabiity score, final generation in the pareto frontier)
- VEM (Untuned, tuned)
- Gibbs sampling (Untuned, tuned)
- different figures.
- pickle files are in src/06-17/dump, runtime src/06-17/out
- log files are in results/06-17/
- Spark vem with all logs.

Command on spark
- ~/spark/spark_latest/bin/spark-submit --driver-memory 6G --executor-memory 6G lda_spark_untuned.py spark://152.46.18.203:7077 pitsA 152.46.18.203 aagrawa8 >> pitsA.log &
- Localhost
  - ~/spark/bin/spark-submit --driver-memory 6G --executor-memory 6G GITHUB/Pits_lda/src/06-17/lda_spark_untuned.py spark://amrit-PC:7077 pitsA 127.0.0.1 amrit > pitsA.log &
  - ~/spark/spark_latest/bin/spark-submit --driver-memory 6G --executor-memory 6G lda_spark_untuned.py spark://152.46.18.203:7077 pitsA 152.46.18.203 aagrawa8 > pitsA.out &
  - ssh -Y aagrawa8@152.46.20.174 "firefox --no-remote"