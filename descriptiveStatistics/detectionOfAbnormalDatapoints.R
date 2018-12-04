# set working directory
setwd("/Users/yun/Downloads/GluGo2.0-master/csvData/csvOutData/")
fn <- "OUTPUT_data_download_Kate_access.csv"
dataset <- read.csv(fn, header=TRUE)

# subset the whole dataset based on days
names (dataset)
dataset.mon <- subset(dataset, Weekday == '0')
dataset.tue <- subset(dataset, Weekday == '1')
dataset.wed <- subset(dataset, Weekday == '2')
dataset.thu <- subset(dataset, Weekday == '3')
dataset.fri <- subset(dataset, Weekday == '4')
dataset.sat <- subset(dataset, Weekday == '5')
dataset.sun <- subset(dataset, Weekday == '6')

# subset the whole dataset based on months
dataset.jan <- subset(dataset, Month == '1')
dataset.feb <- subset(dataset, Month == '2')
dataset.mar <- subset(dataset, Month == '3')
dataset.apr <- subset(dataset, Month == '4')
dataset.may <- subset(dataset, Month == '5')
dataset.jun <- subset(dataset, Month == '6')
dataset.jul <- subset(dataset, Month == '7')
dataset.aug <- subset(dataset, Month == '8')
dataset.sep <- subset(dataset, Month == '9')
dataset.oct <- subset(dataset, Month == '10')
dataset.nov <- subset(dataset, Month == '11')
dataset.dec <- subset(dataset, Month == '12')

# subset the whole dataset based on hours
dataset.0hr <- subset(dataset, Hour == '0')
dataset.1hr <- subset(dataset, Hour == '1')
dataset.2hr <- subset(dataset, Hour == '2')
dataset.3hr <- subset(dataset, Hour == '3')
dataset.4hr <- subset(dataset, Hour == '4')
dataset.5hr <- subset(dataset, Hour == '5')
dataset.6hr <- subset(dataset, Hour == '6')
dataset.7hr <- subset(dataset, Hour == '7')
dataset.8hr <- subset(dataset, Hour == '8')
dataset.9hr <- subset(dataset, Hour == '9')
dataset.10hr <- subset(dataset, Hour == '10')
dataset.11hr <- subset(dataset, Hour == '11')
dataset.12hr <- subset(dataset, Hour == '12')
dataset.13hr <- subset(dataset, Hour == '13')
dataset.14hr <- subset(dataset, Hour == '14')
dataset.15hr <- subset(dataset, Hour == '15')
dataset.16hr <- subset(dataset, Hour == '16')
dataset.17hr <- subset(dataset, Hour == '17')
dataset.18hr <- subset(dataset, Hour == '18')
dataset.19hr <- subset(dataset, Hour == '19')
dataset.20hr <- subset(dataset, Hour == '20')
dataset.21hr <- subset(dataset, Hour == '21')
dataset.22hr <- subset(dataset, Hour == '22')
dataset.23hr <- subset(dataset, Hour == '23')

# plot frequency table
mon_ds<-as.data.frame(table(cut(dataset.mon$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(mon_ds)<-c("numbers","Freq")
mon_high <- mon_ds[3,2]*100/length(dataset.mon$Glucose..ml.dL.)
mon_high
mon_low <- mon_ds[1,2]*100/length(dataset.mon$Glucose..ml.dL.)
mon_low

tue_ds<-as.data.frame(table(cut(dataset.tue$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(tue_ds)<-c("numbers","Freq")
total_length <- length(dataset.tue$Glucose..ml.dL.)
tue_high <- tue_ds[3,2]*100/total_length
tue_high
tue_low <- tue_ds[1,2]*100/total_length
tue_low

wed_ds<-as.data.frame(table(cut(dataset.wed$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(wed_ds)<-c("numbers","Freq")
total_length <- length(dataset.wed$Glucose..ml.dL.)
wed_high <- wed_ds[3,2]*100/total_length
wed_high
wed_low <- wed_ds[1,2]*100/total_length
wed_low

thu_ds<-as.data.frame(table(cut(dataset.thu$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(thu_ds)<-c("numbers","Freq")
total_length <- length(dataset.thu$Glucose..ml.dL.)
thu_high <- thu_ds[3,2]*100/total_length
thu_high
thu_low <- thu_ds[1,2]*100/total_length
thu_low

fri_ds<-as.data.frame(table(cut(dataset.fri$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(fri_ds)<-c("numbers","Freq")
total_length <- length(dataset.fri$Glucose..ml.dL.)
fri_high <- fri_ds[3,2]*100/total_length
fri_high
fri_low <- fri_ds[1,2]*100/total_length
fri_low

sat_ds<-as.data.frame(table(cut(dataset.sat$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(sat_ds)<-c("numbers","Freq")
total_length <- length(dataset.sat$Glucose..ml.dL.)
sat_high <- sat_ds[3,2]*100/total_length
sat_high
sat_low <- sat_ds[1,2]*100/total_length
sat_low

sun_ds<-as.data.frame(table(cut(dataset.sun$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(sun_ds)<-c("numbers","Freq")
total_length <- length(dataset.sun$Glucose..ml.dL.)
sun_high <- sun_ds[3,2]*100/total_length
sun_high
sun_low <- sun_ds[1,2]*100/total_length
sun_low

boxplot(dataset.mon$Glucose..ml.dL., dataset.tue$Glucose..ml.dL., dataset.wed$Glucose..ml.dL., dataset.thu$Glucose..ml.dL., dataset.fri$Glucose..ml.dL., dataset.sat$Glucose..ml.dL., dataset.sun$Glucose..ml.dL.,
        main="Boxplot of glucose level in each day", names=c('M','T','W','R','F','S','S'))

zero_ds<-as.data.frame(table(cut(dataset.0hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(zero_ds)<-c("numbers","Freq")
zerohr_high <- zero_ds[3,2]*100/length(dataset.0hr$Glucose..ml.dL.)
zerohr_high
zerohr_low <- zero_ds[1,2]*100/length(dataset.0hr$Glucose..ml.dL.)
zerohr_low

onehr_ds<-as.data.frame(table(cut(dataset.1hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(onehr_ds)<-c("numbers","Freq")
onehr_high <- onehr_ds[3,2]*100/length(dataset.1hr$Glucose..ml.dL.)
onehr_high
onehr_low <- onehr_ds[1,2]*100/length(dataset.1hr$Glucose..ml.dL.)
onehr_low

twohr_ds<-as.data.frame(table(cut(dataset.2hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(twohr_ds)<-c("numbers","Freq")
twohr_high <- twohr_ds[3,2]*100/length(dataset.2hr$Glucose..ml.dL.)
twohr_high
twohr_low <- twohr_ds[1,2]*100/length(dataset.2hr$Glucose..ml.dL.)
twohr_low

threehr_ds<-as.data.frame(table(cut(dataset.3hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(threehr_ds)<-c("numbers","Freq")
threehr_high <- threehr_ds[3,2]*100/length(dataset.3hr$Glucose..ml.dL.)
threehr_high
threehr_low <- threehr_ds[1,2]*100/length(dataset.3hr$Glucose..ml.dL.)
threehr_low

frhr_ds<-as.data.frame(table(cut(dataset.4hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(frhr_ds)<-c("numbers","Freq")
frhr_high <- frhr_ds[3,2]*100/length(dataset.4hr$Glucose..ml.dL.)
frhr_high
frhr_low <- frhr_ds[1,2]*100/length(dataset.4hr$Glucose..ml.dL.)
frhr_low

fivhr_ds<-as.data.frame(table(cut(dataset.5hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(fivhr_ds)<-c("numbers","Freq")
fivhr_high <- fivhr_ds[3,2]*100/length(dataset.5hr$Glucose..ml.dL.)
fivhr_high
fivhr_low <- fivhr_ds[1,2]*100/length(dataset.5hr$Glucose..ml.dL.)
fivhr_low

sixhr_ds<-as.data.frame(table(cut(dataset.6hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(sixhr_ds)<-c("numbers","Freq")
sixhr_high <- sixhr_ds[3,2]*100/length(dataset.6hr$Glucose..ml.dL.)
sixhr_high
sixhr_low <- sixhr_ds[1,2]*100/length(dataset.6hr$Glucose..ml.dL.)
sixhr_low

sevhr_ds<-as.data.frame(table(cut(dataset.7hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(sevhr_ds)<-c("numbers","Freq")
sevhr_high <- sevhr_ds[3,2]*100/length(dataset.7hr$Glucose..ml.dL.)
sevhr_high
sevhr_low <- sevhr_ds[1,2]*100/length(dataset.7hr$Glucose..ml.dL.)
sevhr_low

eithr_ds<-as.data.frame(table(cut(dataset.8hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(eithr_ds)<-c("numbers","Freq")
eithr_high <- eithr_ds[3,2]*100/length(dataset.8hr$Glucose..ml.dL.)
eithr_high
eithr_low <- eithr_ds[1,2]*100/length(dataset.8hr$Glucose..ml.dL.)
eithr_low

ninhr_ds<-as.data.frame(table(cut(dataset.9hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(ninhr_ds)<-c("numbers","Freq")
ninhr_high <- ninhr_ds[3,2]*100/length(dataset.9hr$Glucose..ml.dL.)
ninhr_high
ninhr_low <- ninhr_ds[1,2]*100/length(dataset.9hr$Glucose..ml.dL.)
ninhr_low

tenhr_ds<-as.data.frame(table(cut(dataset.10hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(eithr_ds)<-c("numbers","Freq")
tenhr_high <- tenhr_ds[3,2]*100/length(dataset.10hr$Glucose..ml.dL.)
tenhr_high
tenhr_low <- tenhr_ds[1,2]*100/length(dataset.10hr$Glucose..ml.dL.)
tenhr_low

dix_onehr_ds<-as.data.frame(table(cut(dataset.11hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(dix_onehr_ds)<-c("numbers","Freq")
dix_onehr_high <- dix_onehr_ds[3,2]*100/length(dataset.11hr$Glucose..ml.dL.)
dix_onehr_high
dix_onehr_low <- dix_onehr_ds[1,2]*100/length(dataset.11hr$Glucose..ml.dL.)
dix_onehr_low

dix_2hr_ds<-as.data.frame(table(cut(dataset.12hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(dix_2hr_ds)<-c("numbers","Freq")
dix_2hr_high <- dix_2hr_ds[3,2]*100/length(dataset.12hr$Glucose..ml.dL.)
dix_2hr_high
dix_2hr_low <- dix_2hr_ds[1,2]*100/length(dataset.12hr$Glucose..ml.dL.)
dix_2hr_low

dix_3hr_ds<-as.data.frame(table(cut(dataset.13hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(dix_3hr_ds)<-c("numbers","Freq")
dix_3hr_high <- dix_3hr_ds[3,2]*100/length(dataset.13hr$Glucose..ml.dL.)
dix_3hr_high
dix_3hr_low <- dix_3hr_ds[1,2]*100/length(dataset.13hr$Glucose..ml.dL.)
dix_3hr_low

dix_4hr_ds<-as.data.frame(table(cut(dataset.14hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(dix_4hr_ds)<-c("numbers","Freq")
dix_4hr_high <- dix_4hr_ds[3,2]*100/length(dataset.14hr$Glucose..ml.dL.)
dix_4hr_high
dix_4hr_low <- dix_4hr_ds[1,2]*100/length(dataset.14hr$Glucose..ml.dL.)
dix_4hr_low

dix_5hr_ds<-as.data.frame(table(cut(dataset.15hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(dix_5hr_ds)<-c("numbers","Freq")
dix_5hr_high <- dix_5hr_ds[3,2]*100/length(dataset.15hr$Glucose..ml.dL.)
dix_5hr_high
dix_5hr_low <- dix_5hr_ds[1,2]*100/length(dataset.15hr$Glucose..ml.dL.)
dix_5hr_low

dix_6hr_ds<-as.data.frame(table(cut(dataset.16hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(dix_6hr_ds)<-c("numbers","Freq")
dix_6hr_high <- dix_6hr_ds[3,2]*100/length(dataset.16hr$Glucose..ml.dL.)
dix_6hr_high
dix_6hr_low <- dix_6hr_ds[1,2]*100/length(dataset.16hr$Glucose..ml.dL.)
dix_6hr_low

dix_7hr_ds<-as.data.frame(table(cut(dataset.17hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(dix_7hr_ds)<-c("numbers","Freq")
dix_7hr_high <- dix_7hr_ds[3,2]*100/length(dataset.17hr$Glucose..ml.dL.)
dix_7hr_high
dix_7hr_low <- dix_7hr_ds[1,2]*100/length(dataset.17hr$Glucose..ml.dL.)
dix_7hr_low

dix_8hr_ds<-as.data.frame(table(cut(dataset.18hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(dix_8hr_ds)<-c("numbers","Freq")
dix_8hr_high <- dix_8hr_ds[3,2]*100/length(dataset.18hr$Glucose..ml.dL.)
dix_8hr_high
dix_8hr_low <- dix_8hr_ds[1,2]*100/length(dataset.18hr$Glucose..ml.dL.)
dix_8hr_low

dix_9hr_ds<-as.data.frame(table(cut(dataset.19hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(dix_9hr_ds)<-c("numbers","Freq")
dix_9hr_high <- dix_9hr_ds[3,2]*100/length(dataset.19hr$Glucose..ml.dL.)
dix_9hr_high
dix_9hr_low <- dix_9hr_ds[1,2]*100/length(dataset.19hr$Glucose..ml.dL.)
dix_9hr_low

vingt_0hr_ds<-as.data.frame(table(cut(dataset.20hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(vingt_0hr_ds)<-c("numbers","Freq")
vingt_0hr_high <- vingt_0hr_ds[3,2]*100/length(dataset.20hr$Glucose..ml.dL.)
vingt_0hr_high
vingt_0hr_low <- vingt_0hr_ds[1,2]*100/length(dataset.20hr$Glucose..ml.dL.)
vingt_0hr_low

vingt_1hr_ds<-as.data.frame(table(cut(dataset.21hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(vingt_1hr_ds)<-c("numbers","Freq")
vingt_1hr_high <- vingt_1hr_ds[3,2]*100/length(dataset.21hr$Glucose..ml.dL.)
vingt_1hr_high
vingt_1hr_low <- vingt_1hr_ds[1,2]*100/length(dataset.21hr$Glucose..ml.dL.)
vingt_1hr_low

vingt_2hr_ds<-as.data.frame(table(cut(dataset.22hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(vingt_2hr_ds)<-c("numbers","Freq")
vingt_2hr_high <- vingt_2hr_ds[3,2]*100/length(dataset.22hr$Glucose..ml.dL.)
vingt_2hr_high
vingt_2hr_low <- vingt_2hr_ds[1,2]*100/length(dataset.22hr$Glucose..ml.dL.)
vingt_2hr_low

vingt_3hr_ds<-as.data.frame(table(cut(dataset.23hr$Glucose..ml.dL.,breaks=c(0,70,230,1000),labels=c("0-70","70-230","230+"))) )
colnames(vingt_3hr_ds)<-c("numbers","Freq")
vingt_3hr_high <- vingt_3hr_ds[3,2]*100/length(dataset.23hr$Glucose..ml.dL.)
vingt_3hr_high
vingt_3hr_low <- vingt_3hr_ds[1,2]*100/length(dataset.23hr$Glucose..ml.dL.)
vingt_3hr_low

# create boxplot
boxplot(dataset.0hr$Glucose..ml.dL.,dataset.1hr$Glucose..ml.dL.,dataset.2hr$Glucose..ml.dL.,dataset.3hr$Glucose..ml.dL.,dataset.4hr$Glucose..ml.dL.,dataset.5hr$Glucose..ml.dL.,dataset.6hr$Glucose..ml.dL.,dataset.7hr$Glucose..ml.dL.,dataset.8hr$Glucose..ml.dL.,dataset.9hr$Glucose..ml.dL.,dataset.10hr$Glucose..ml.dL.,dataset.11hr$Glucose..ml.dL.,dataset.12hr$Glucose..ml.dL.,dataset.13hr$Glucose..ml.dL.,dataset.14hr$Glucose..ml.dL.,dataset.15hr$Glucose..ml.dL.,dataset.16hr$Glucose..ml.dL.,dataset.17hr$Glucose..ml.dL.,dataset.18hr$Glucose..ml.dL.,dataset.19hr$Glucose..ml.dL.,dataset.20hr$Glucose..ml.dL.,dataset.21hr$Glucose..ml.dL.,dataset.22hr$Glucose..ml.dL.,dataset.23hr$Glucose..ml.dL.,
        main="Boxplot of glucose level in each hour", names=c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23), xlab="Hours")
