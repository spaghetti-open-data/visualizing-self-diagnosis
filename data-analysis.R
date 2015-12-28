# First analysis script

# data extracted directly from downloaded gzipped file at URL: https://dumps.wikimedia.org/other/pagecounts-all-sites/2015/2015-11/pagecounts-20151101-060000.gz
pagecounts.20151101.060000 <- read.csv2(gzfile("pagecounts-20151101-060000.gz"), header=FALSE, row.names=NULL, sep="", stringsAsFactors=FALSE)# load csv file derived from the source code of URL: https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Medicine/Lists_of_pages/Articles
# load csv file derived from the source code of URL: https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Medicine/Lists_of_pages/Articles
wikiproject_medicine <- read.csv2("wikiproject_medicine.csv", header=FALSE, stringsAsFactors=FALSE)
# join both dataframes (rough solution to cope with default names - TO DO: rename fields)
ccc <- merge (x=wikiproject_medicine, y=pagecounts.20151101.060000, by.x="V1", by.y="V2")
#convert character field to integer
ccc$V3.y <- as.numeric(ccc$V3.y)
# density plot
d <- density (ccc$V3.y)
plot(d, xlim=c(0, 50))
# plot frequency histogram
table(ccc$V3.y)
barplot(table(ccc$V3.y))
# plot frequency histogram (log axis)
barplot(table(ccc$V3.y), log="xy")
