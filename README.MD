# Log Analysis with Hadoop and Hive
# author: Zhifu Xiao

# Purpose: 

In the previous assignment you worked with the Hadoop, HDFS and Hive environments to perform MapReduce jobs, loading data in HDFS and querying a small Hive database. Now we shall see and learn how to work with actual big data. In this assignment, you shall write your own MapReduce programs to perform more sophisticated tasks. Further you will create your own Hive database given the dataset in raw form and run few queries on it.

This assignment can be performed on the same cloudera virtual machine that was used for the previous assignment. No further setup or installation will be needed. Although we recommend Python, you are free to use any language of your choice for this assignment.

# Dataset: Nasa Server Logs

**File Name** - server-logs.gz

**Size** - The total size of the dataset is roughly 1GB after uncompressing the .gz file. 

**Description** - The given data set contains Apache Logs gathered by NASA's server in the months of July-October, 1995.

The logs follow the standard [Apache log](https://httpd.apache.org/docs/2.4/logs.html#accesslog) format whereby each line denotes one request.

- Source IP 
- Timestamp 
- HTTP Method
- Request URL
- HTTP Protocol
- Status Code 
- Response Bytes

```
129.188.154.200 - - [01/Jul/1995:00:03:14 -0400] "GET /images/launchpalms-small.gif HTTP/1.0" 200 11473
```

Dataset can be obtained from [here](https://drive.google.com/open?id=0B6qnKGQsJnFfWG02N2loUVluck0).

# Part 1:

## Clean the dataset
@ bash
cat july.txt | sed 's/\ \-\ \-//g' | sed 's/"//g' | sed 's/\[//g' | sed 's/\]//g' | sed -e 's/\// /1' | sed -e 's/\// /1' | sed -e 's/\:/ /1' >> clean.txt

## Create data schema
@ hive
CREATE TABLE nasa (
    `source_ip` STRING,
    `day` INT,
    `month` STRING,
    `year` INT,
    `time` DATE,
    `time_zone` STRING,
    `http_method` STRING,
    `request_url` STRING,
    `http_protocol` STRING,
    `status_code` INT,
    `response_bytes` INT
    ) row format delimited fields terminated by ' ' stored as textfile;

## Load data into hive table
LOAD DATA LOCAL INPATH 'clean.txt' INTO TABLE nasa;

## Problem a:
SELECT COUNT(1) FROM nasa WHERE `status_code` = 200;
Result: 18556092

## Problem b:
SELECT COUNT(DISTINCT `source_ip`) AS count FROM nasa WHERE `month` = 'Aug';
Result: 75048

## Problem c:
SELECT `request_url`, COUNT(1) as count FROM nasa WHERE `year` = 1995 GROUP BY `request_url` ORDER BY count DESC LIMIT 1;
Result: /images/NASA-logosmall.gif	1252722

## Problem d:
@bash
hive -e 'SELECT `day`, COUNT(1) as count FROM nasa WHERE `month` = "Oct" GROUP BY `day` ORDER BY `day` ASC' > temp.csv

## Create bar chart for the data
@R
library(ggplot2)
data <- read.csv('temp.csv', header = FALSE, sep = "\t")
data <- data[-31:-32,]
c(1,3:31)
ggplot(data) + 
  geom_bar(aes(x = c(1,3:31), weight = V2))
  
See the plot as plot.png

# Part 2:

## Problem a:
@ bash
cat clean.txt | ./Mapper.py | sort | ./Reducer.py | sort -k 2 -r -n > results.txt

## Problem b:
cat clean.txt | ./Mapper2.py | ./Reducer2.py
Result: 154781124600
