# -*- coding: utf-8 -*-


from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import StringIndexer, VectorAssembler, OneHotEncoder
from pyspark.ml.classification import LogisticRegression, RandomForestClassifier
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import pandas as pd

# Inisialisasi Spark Session
spark = SparkSession.builder.appName("ChurnPrediction").getOrCreate()

# Mengimpor data dari file CSV
file_path = 'telecustomer.csv'
data = pd.read_csv(file_path)


# Menghilangkan kolom dengan banyak nilai NaN dan kolom 'customerID'
data_cleaned = data.dropna(axis=1, how='all')  # Menghilangkan kolom dengan semua nilai NaN
data_cleaned = data_cleaned.drop(['customerID'], axis=1)  # 'customerID' tidak relevan untuk analisis


# Menghilangkan baris dengan nilai NaN di 'TotalCharges'
data_cleaned['TotalCharges'] = pd.to_numeric(data_cleaned['TotalCharges'], errors='coerce')
data_cleaned = data_cleaned.dropna(subset=['TotalCharges'])

# Ubah DataFrame Pandas ke PySpark DataFrame
spark_df = spark.createDataFrame(data_cleaned)

# Mengubah kolom target 'Churn' menjadi numerik
indexer = StringIndexer(inputCol="Churn", outputCol="label")
df = indexer.fit(spark_df).transform(spark_df)

# Feature Engineering
categoricalColumns = [col for col, dtype in df.dtypes if dtype == "string"]
stages = []  # stages dalam pipeline

for categoricalCol in categoricalColumns:
    stringIndexer = StringIndexer(inputCol=categoricalCol, outputCol=categoricalCol + "Index")
    encoder = OneHotEncoder(inputCols=[stringIndexer.getOutputCol()], outputCols=[categoricalCol + "classVec"])
    stages += [stringIndexer, encoder]

numericCols = [col for col, dtype in df.dtypes if dtype in ["double", "int"] and col != "label"]
assemblerInputs = [c + "classVec" for c in categoricalColumns] + numericCols
assembler = VectorAssembler(inputCols=assemblerInputs, outputCol="features")
stages += [assembler]

# Pipeline
pipeline = Pipeline(stages=stages)
pipelineModel = pipeline.fit(df)
df = pipelineModel.transform(df)

from pyspark.ml.evaluation import MulticlassClassificationEvaluator
# Pembagian Data
train, test = df.randomSplit([0.7, 0.3], seed=2023)


rf = RandomForestClassifier(featuresCol="features", labelCol="label")

# Tuning Hyperparameter dengan Cross Validation
paramGrid = ParamGridBuilder() \
    .addGrid(rf.numTrees, [10, 20, 30]) \
    .addGrid(rf.maxDepth, [5, 10, 15]) \
    .build()

crossval = CrossValidator(estimator=rf,
                          estimatorParamMaps=paramGrid,
                          evaluator=MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy"),
                          numFolds=5)

# Latih model dengan Cross Validation
cvModel = crossval.fit(train)

# Evaluasi Model
predictions = cvModel.transform(test)
evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)

print(f"Accuracy: {accuracy}")
