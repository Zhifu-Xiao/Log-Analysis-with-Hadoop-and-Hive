# COMS 4121: Computer System: Log Analysis
# author: Zhifu Xiao (zx2201@columbia.edu)

Part 1:

# Clean the dataset
@ bash
cat july.txt | sed 's/\ \-\ \-//g' | sed 's/"//g' | sed 's/\[//g' | sed 's/\]//g' | sed -e 's/\// /1' | sed -e 's/\// /1' | sed -e 's/\:/ /1' >> clean.txt

# Create data schema
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

# Load data into hive table
LOAD DATA LOCAL INPATH 'clean.txt' INTO TABLE nasa;

# Problem a:
SELECT COUNT(1) FROM nasa WHERE `status_code` = 200;
Result: 18556092

# Problem b:
SELECT COUNT(DISTINCT `source_ip`) AS count FROM nasa WHERE `month` = 'Aug';
Result: 75048

# Problem c:
SELECT `request_url`, COUNT(1) as count FROM nasa WHERE `year` = 1995 GROUP BY `request_url` ORDER BY count DESC LIMIT 1;
Result: /images/NASA-logosmall.gif	1252722

# Problem d:
@bash
hive -e 'SELECT `day`, COUNT(1) as count FROM nasa WHERE `month` = "Oct" GROUP BY `day` ORDER BY `day` ASC' > temp.csv

# Create bar chart for the data
@R
library(ggplot2)
data <- read.csv('temp.csv', header = FALSE, sep = "\t")
data <- data[-31:-32,]
c(1,3:31)
ggplot(data) + 
  geom_bar(aes(x = c(1,3:31), weight = V2))
  
# See the plot as plot.png

Part 2:

# Problem a:
@ bash
cat clean.txt | ./Mapper.py | sort | ./Reducer.py | sort -k 2 -r -n > results.txt

# Problem b:
cat clean.txt | ./Mapper2.py | ./Reducer2.py
Result: 154781124600
