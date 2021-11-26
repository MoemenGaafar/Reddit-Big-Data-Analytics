#!/bin/bash

export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export HADOOP_HOME=/home/moemen/CIE427/hadoop-3.3.1
export PATH=${JAVA_HOME}/bin:${HADOOP_HOME}/bin:${PATH}
export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar:${HADOOP_HOME}/share/hadoop/tools/lib/*

${HADOOP_HOME}/bin/hdfs namenode -format
${HADOOP_HOME}/bin/hdfs --daemon start namenode
${HADOOP_HOME}/bin/hdfs --daemon start datanode
${HADOOP_HOME}/bin/hdfs dfs -mkdir /user
${HADOOP_HOME}/bin/hdfs dfs -mkdir /user/$USER
${HADOOP_HOME}/bin/hdfs dfs -mkdir /user/$USER/MiniProject1
${HADOOP_HOME}/bin/hdfs dfs -mkdir /user/$USER/MiniProject1/input1
${HADOOP_HOME}/bin/hdfs dfs -put /home/moemen/CIE427/MiniProject1/input/RC_2015-01.bz2 MiniProject1/input1

echo "MapReduce1 ready for action"

hadoop org.apache.hadoop.streaming.HadoopStreaming \
-input MiniProject1/input1 \
-output MiniProject1/output1 \
-mapper /home/moemen/CIE427/MiniProject1/mapper.py \
-combiner /home/moemen/CIE427/MiniProject1/identity.py \
-reducer /home/moemen/CIE427/MiniProject1/reducer1.py

echo "MapReduce2 ready for action"

hadoop org.apache.hadoop.streaming.HadoopStreaming \
-input MiniProject1/output1 \
-output MiniProject1/output2 \
-mapper /home/moemen/CIE427/MiniProject1/identity.py \
-combiner /home/moemen/CIE427/MiniProject1/identity.py \
-reducer /home/moemen/CIE427/MiniProject1/reducer2.py

echo "MapReduce3 ready for action"

hadoop org.apache.hadoop.streaming.HadoopStreaming \
-input MiniProject1/output2 \
-output MiniProject1/output3 \
-mapper /home/moemen/CIE427/MiniProject1/identity.py \
-combiner /home/moemen/CIE427/MiniProject1/identity.py \
-reducer /home/moemen/CIE427/MiniProject1/reducer3.py

${HADOOP_HOME}/bin/hdfs dfs -get MiniProject1/output3 /home/moemen/CIE427/MiniProject1
