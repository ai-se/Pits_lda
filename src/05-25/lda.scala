package lda

import org.apache.log4j.{Level, Logger}
//import scopt.OptionParser
import scala.collection.mutable
import org.apache.spark.mllib.linalg.{Vector, Vectors}
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkContext._
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.feature.{CountVectorizer, CountVectorizerModel, RegexTokenizer, StopWordsRemover,HashingTF, IDF, Tokenizer, IDFModel}
import org.apache.spark.mllib.clustering.{DistributedLDAModel, EMLDAOptimizer, LDA, OnlineLDAOptimizer}
import org.apache.spark.sql.{Row, SQLContext}
import java.io.File
import java.io.PrintWriter
import scala.io.Source


/**
 * An example Latent Dirichlet Allocation (LDA) app. Run with
 * {{{
 * ./bin/run-example mllib.LDAExample [options] <input>
 * }}}
 * If you use it as a template to create your own app, please use `spark-submit` to submit your app.
 */
object lda {

  /*private case class Params(
      input: Seq[String] = Seq.empty,
      k: Int = 20,
      maxIterations: Int = 10,
      docConcentration: Double = -1,
      topicConcentration: Double = -1,
      vocabSize: Int = 10000,
      stopwordFile: String = "",
      algorithm: String = "em",
      checkpointDir: Option[String] = None,
      checkpointInterval: Int = 10) extends AbstractParams[Params]*/

  def main(args: Array[String]) {


    run(args)
    
  }

  private def run(args: Array[String]) {
val getCurrentDirectory = new java.io.File( "." ).getCanonicalPath
val conf = new SparkConf().setAppName("lda")
conf.setMaster(args(1))
conf.set("spark.executor.memory", "6g")
conf.set("spark.driver.memory", "6g")
conf.set("spark.driver.maxResultSize", "6g")
conf.set("spark.yarn.executor.memoryOverhead", "2g")
conf.set("spark.yarn.driver.memoryOverhead", "2g")


conf.set("spark.eventLog.enabled", "true")
conf.set("spark.eventLog.dir", "hdfs://"+args(3)+"/user/"+args(4)+"/Logs/")
val sc = new SparkContext(conf)

val corpus1: String = "hdfs://"+args(3)+"/user/"+args(4)+"/In/"+args(2)

    Logger.getRootLogger.setLevel(Level.WARN)

    // Load documents, and prepare them for LDA.
    val preprocessStart = System.nanoTime()
    val (corpus, vocabArray, actualNumTokens) =
      preprocess(sc, corpus1, 50000, "")
    corpus.cache()
    val actualCorpusSize = corpus.count()
    val actualVocabSize = vocabArray.size
    val preprocessElapsed = (System.nanoTime() - preprocessStart) / 1e9

    println()
    println(s"Corpus summary:")
    println(s"\t Training set size: $actualCorpusSize documents")
    println(s"\t Vocabulary size: $actualVocabSize terms")
    println(s"\t Training set size: $actualNumTokens tokens")
    println(s"\t Preprocessing time: $preprocessElapsed sec")
    //println(s"\t Vocabulary array")
//vocabArray.collect().foreach(println)
    println()
    val writer = new PrintWriter(new File("Write.txt"))

    // Run LDA.
	for( a <- 1 to 10){
	writer.write("Run : "+ a+"\n")
    val lda = new LDA()
    val  checkpointDir: Option[String] = None
    val optimizer = "online".toLowerCase match {
      case "em" => new EMLDAOptimizer
      // add (1.0 / actualCorpusSize) to MiniBatchFraction be more robust on tiny datasets.
      case "online" => new OnlineLDAOptimizer().setMiniBatchFraction(0.05 + 1.0 / actualCorpusSize)
      case _ => throw new IllegalArgumentException(
        s"Only em, online are supported but got em.")
    }

    lda.setOptimizer(optimizer)
      .setK(30)
      .setMaxIterations(10)
      .setDocConcentration(-1)
      .setTopicConcentration(-1)
      .setCheckpointInterval(10)
    if (checkpointDir.nonEmpty) {
      sc.setCheckpointDir(checkpointDir.get)
    }
    val startTime = System.nanoTime()
    val ldaModel = lda.run(corpus)
    val elapsed = (System.nanoTime() - startTime) / 1e9
          //println(s"\t Terms")
	//val a=ldaModel.topicsMatrix.toArray
      //println(s"\t $a")

    println(s"Finished training LDA model.  Summary:")
    println(s"\t Training time: $elapsed sec")

    if (ldaModel.isInstanceOf[DistributedLDAModel]) {
      val distLDAModel = ldaModel.asInstanceOf[DistributedLDAModel]
      val avgLogLikelihood = distLDAModel.logLikelihood / actualCorpusSize.toDouble
      println(s"\t Training data average log likelihood: $avgLogLikelihood")
      println(s"\t Terms")
      //println(s"\t $distLDAModel.topicsMatrix().toArray()")
      println()
    }


    // Print the topics, showing the top-weighted terms for each topic.
    val topicIndices = ldaModel.describeTopics(maxTermsPerTopic = 10)
	//println(s"\t Topic Indices")
//topicIndices.collect().foreach(println)

    val topics = topicIndices.map { case (terms, termWeights) =>
      terms.zip(termWeights).map { case (term, weight) => (vocabArray(term.toInt), weight) }
    }

    println(s"30 topics:")
    topics.zipWithIndex.foreach { case (topic, i) =>
      println(s"TOPIC $i")
      topic.foreach { case (term, weight) =>
        println(s"$term\t$weight")
	writer.write(term + " ")

      }
	writer.write("\n")	
      println()
    }

	}
	    	writer.close()
    sc.stop()
  }

  /**
   * Load documents, tokenize them, create vocabulary, and prepare documents as term count vectors.
   * @return (corpus, vocabulary as array, total token count in corpus)
   */
  private def preprocess(
      sc: SparkContext,
      paths: String,
      vocabSize: Int,
      stopwordFile: String): (RDD[(Long, Vector)], Array[String], Long) = {

    val sqlContext = SQLContext.getOrCreate(sc)
    import sqlContext.implicits._

    // Get dataset of document texts
    // One document per line in each text file. If the input consists of many small files,
    // this can result in a large number of small partitions, which can degrade performance.
    // In this case, consider using coalesce() to create fewer, larger partitions.
    /*val documents: RDD[Seq[String]] = sc.textFile(paths).map(_.split(" ").toSeq)
    val hashingTF = new HashingTF()
    val tf: RDD[Vector] = hashingTF.transform(documents)
    tf.cache()
    val idf = new IDF(minDocFreq = 2).fit(tf)
    val tfidf: RDD[Vector] = idf.transform(tf)
	println(tfidf)*/

    val df = sc.textFile(paths).toDF("docs")
    val customizedStopWords: Array[String] = if (stopwordFile.isEmpty) {
      Array.empty[String]
    } else {
      val stopWordText = sc.textFile(stopwordFile).collect()
      stopWordText.flatMap(_.stripMargin.split("\\s+"))
    }
    val tokenizer = new RegexTokenizer()
      .setInputCol("docs")
      .setOutputCol("rawTokens")
    val stopWordsRemover = new StopWordsRemover()
      .setInputCol("rawTokens")
      .setOutputCol("tokens")
    stopWordsRemover.setStopWords(stopWordsRemover.getStopWords ++ customizedStopWords)
    val hashingTF = new HashingTF()
      .setInputCol("tokens")
      .setOutputCol("hashfeatures")
    val idf = new IDF()
      .setInputCol("hashfeatures")
      .setOutputCol("idffeatures")
    val countVectorizer = new CountVectorizer()
      .setInputCol("tokens")
      .setOutputCol("features")

    /*val pipeline1 = new Pipeline()
      .setStages(Array(tokenizer, stopWordsRemover,hashingTF, idf))
    val model1 = pipeline1.fit(df)
    val documents1 = model1.transform(df)
      .select("idffeatures")
      .rdd
      .map { case Row(idffeatures: Vector) => idffeatures }
      .zipWithIndex()
      .map(_.swap)*/

    val pipeline = new Pipeline()
      .setStages(Array(tokenizer, stopWordsRemover, countVectorizer))
    val model = pipeline.fit(df)
    val documents = model.transform(df)
      .select("features")
      .rdd
      .map { case Row(features: Vector) => features }
      //.map { case Row(features: Vector) =>  model1.transform(df).select("idffeatures").map { case Row(idffeatures: Vector) => idffeatures }}
      .zipWithIndex()
      .map(_.swap)



	//println(s"\t documents for idf")
//documents1.collect().foreach(println)
//	println(s"$documents")
//documents.collect().foreach(println)
    (documents,
      model.stages(2).asInstanceOf[CountVectorizerModel].vocabulary,  // vocabulary
      documents.map(_._2.numActives).sum().toLong) // total token count
  }
}
