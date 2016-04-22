
### Important
## How to effectively use topic models for software engineering tasks? an approach based on genetic algorithms - 2013, 75
https://github.com/ai-se/Pits_lda/issues/8
- applying it on software data, using the same parameter values used for natural language text, did not always produce the expected results [18] (http://www.cs.wm.edu/semeru/papers/IR01.pdf)
- Common parameters, k, a, b, no of iterations.
- data and resultes mentioned [here] (http://www.distat.unimol.it/reports/LDA-GA)
- Validation in similar manner, checking for the overlaps of terms.
- Toolkit not mentioned


## On the equivalence of information retrieval methods for automated traceability link recovery - 2010, 108
http://www.cs.wm.edu/semeru/papers/IR01.pdf
- The analysis of precision and recall demonstrates that the LDA-based technique results in lower accuracy than the other three techniques
- Played with different configurations of lda.
- Combined LDA with other IR techniques to imrpove accuracy.
- Dataset and replication can be done from [here] (http://www.cs.wm.edu/semeru/data/icpc10-tr-lda/)
- Common parameters not mentioned. Validation not mentioned on topics overlap. Toolkit not mentioned.


## Source code retrieval for bug localization using latent dirichlet allocation - 2008, 131
http://www.unix.eng.ua.edu/~kw5639/PDFs/wcre.pdf
- analysis of 1,555 Java projects from SourceForge and Apache. Produced functional and easily interpretable topics.
- Toolkit - open-source software tool for LDA analysis called GibbsLDA++
- No validation done on the topics generated whether they are stable or not. Common parameters, k, a, b, no of iterations.
- K=100, α=0.05(50/K), and β=0.01


## How do users like this feature? a fine grained sentiment analysis of app reviews - 2014, 44
https://mobis.informatik.uni-hamburg.de/wp-content/uploads/2014/06/FeatureSentiments.pdf
- number of topics (a parameter for LDA) can be manually tuned for each app by the project team to get less duplicate topics and better coherence and precision
- Manual topic coherence evaluation based on requirements engineering.
- dataset [here] (https://mobis.informatik.uni-hamburg.de/app-review-analysis/)
- toolkit can be gibbslda++ or python
- No mention about Common parameters


## Analysis of user comments: an approach for software requirements evolution - 2013, 61
http://dl.acm.org/citation.cfm?id=2486865
- analysis of user comments. Results show that the automatically extracted topics match the manually extracted ones. Very solid statement.
- Stable levels are achieved for bigger values of k.
- Toolkit not mentioned, No validation done on the topics generated whether they are stable or not. No mention about Common parameters.
- Public data set of 3 mobile apps.


## A large scale study of programming languages and code quality in github - 2014, 36
http://web.cs.ucdavis.edu/~filkov/papers/lang_github.pdf
- Data of Github
- Here they just try to find each project belonging to which different topics with its probabilities. (Kind of soft assignment)
- Toolkit not mentioned, No validation done on the topics generated whether they are stable or not. No mention about Common parameters.


## Improving trace accuracy through data-driven configuration and composition of tracing features - 2013, 27
http://re.cs.depaul.edu/papers/2013-ESEC-TraceConfiguration.pdf
- LDA-GA approach [28] (http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.380.7196&rep=rep1&type=pdf) uses a GA to configure the parameters of LDA (Latent Dirichlet Allocation) topic modelling technique, in order to improve the performance of traceability link recovery
- Toolkit not mentioned, No validation done on the topics generated whether they are stable or not. No mention about Common parameters. No dataset mentioned.



### Non determininstic so not many people have bothered about how their results might vary.
