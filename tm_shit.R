library(tm)

getSources()	# shows list of available text courses currently loaded
dir <- "/Users/sinn/NLP-Stuff/Texts"
(thursday <- Corpus(DirSource(dir), readerControl = list(language = 'eng')))
summary(thursday)		# as expected
inspect(thursday[1])	# prints entire 1st doc in corpus thursday

# access in-house texts repos
reut21578 <- system.file("texts", "crude", package = "tm")
reuters <- Corpus(DirSource(reut21578), readerControl = list(reader = readReut21578XML))
reuters <- tm_map(reuters, as.PlainTextDocument)
reuters <- tm_map(reuters, stripWhitespace)
reuters <- tm_map(reuters, tolower)
reuters <- tm_map(reuters, removeWords, stopwords("english"))
dtm.reu <- DocumentTermMatrix(reuters)
# simple word cound trend (there's prob an easier way to do this, though):
word.counts <- data.frame()
for (d in 2:40) {
	num.docs <- length(findFreqTerms(dtm.reu, d))
	word.counts <- rbind(word.counts,
						 data.frame(Freq = d, 
						 			NumWords = num.docs))
}
ggplot(word.counts, aes(x = Freq, y = NumWords)) +
	geom_point() +
	geom_line()

# gets the words that have a 60%+ correlation w/ "crude"
# fucking expensive function on large data sets..
findAssocs(dtm.reu, "crude", 0.6)
# creates a term-doc matrix with only words occuring in more than
# 40% of documents in the set..
inspect(removeSparseTerms(dtm.reu, 0.6))

# can also use dictionaries to pre-exclude terms from dtm
d <- Dictionary(c("prices", "crude", 'house'))
inspect(DocumentTermMatrix(reuters, list(dictionary = d)))

# doc-term
dtm <- DocumentTermMatrix(corpus.of.interst)
# gets list of terms in dtm occuring at least the desired num of times
findFreqTerms(dtm, desired.freq)
# matrix in place of dtm
findAssocs(dtm, word.of.interest, desired.correlation.min)