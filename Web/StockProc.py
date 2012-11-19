
import nltk, re, from urllib import urlread

yahooBase = "http://finance.yahoo.com/d/quotes.csv?s="
yahooTail = "&f=sl1b2b3c6"
#Open .txt file of symbols and descriptions
f = open("/Users/sinn/Documents/Internet Stock Stuff/NYSE.txt",'r')
raw = f.read()
tokens = re.split(r'[\t\n\r]+',raw)
f.close()


#Build dictionary of symbol-to-company name
#First pair is "Symbol" and "Description"
NYSEdict = {}
for num in range(len(tokens)/2):
	NYSEdict[tokens[num*2]] = [tokens[num*2+1]]
	
#...or reverse...
for num in range(len(tokens)/2):
	NYSEdict[tokens[num*2+1]] = [tokens[num*2]]

#
#Build list of stock symbols for easy reference
NYSEsl = []
for num in range(len(tokens)/2-1):
	NYSEsl.append(tokens[(num+1)*2])
#..and create "plugin" for URL
NYSES = '+'.join(NYSEsl)

#
#First length rejected is 476, so assuming 450 is max...
#Actually, limit is 200..oops
for num in range(1,len(NYSEsl),25):
    url = yahooBase+'+'.join(NYSEsl[:num])+yahooTail
    try:
        NYSEcsv = urlopen(url).read()
        output_file = open('/Users/sinn/Documents/Internet Stock Stuff/Stocks/output.txt','w')
        output_file.write(NYSEcsv)
        output_file.write('\n%s' % num)
    except IOError:
        print "Attempt %s failed" % (num)
    if NYSEcsv[-7:-3]=='BODY':
	    print 'First length rejected is %s' % num
	    sys.exit()


#
#This is the base code for obtaining the stock info for the entire list
input_file = open('/Users/sinn/Documents/Internet Stock Stuff/NYSEsl.txt')
raw = input_file.read()
NYSEsl = re.split(r'\n',raw)
NYSEcsv=''
for num in range(200,len(NYSEsl)+(201-len(NYSEsl)%200),200):
    if num > len(NYSEsl):
        url = yahooBase+'+'.join(NYSEsl[-(len(NYSEsl)%200):])+yahooTail
    else:
        url = yahooBase+'+'.join(NYSEsl[num-200:num])+yahooTail
    NYSEcsv = NYSEcsv+urlopen(url).read()

#Appending ('a') is safer than Writing ('w')
output_file = open('/Users/sinn/Documents/Internet Stock Stuff/Stocks/output.txt','a')
output_file.write(TimeStamp+'\n')
output_file.write(NYSEcsv)
output_file.close()

input_file = open('/Users/sinn/Documents/Internet Stock Stuff/Stocks/output.txt','r')
raw = input_file.read()
tokens = re.split(r'[\t\n\r]+|,',raw)
input_file.close()


#Get rid of "dud" stocks...
Ind=0,Remove=[]
while Ind < len(tokens):
	try:
		Place = tokens.index("N/A",Ind)
		Remove.append(Place-Place%5)
		Ind = Remove[-1]+5
	except ValueError:
		Ind = len(tokens)+5
		print 'Done; %s stocks found' % len(Remove)

DudStockIndex = [num/5 for num in Remove]
NumSoFar=0
for Ind in DudStockIndex:
    NYSEsl.remove(NYSEsl[Ind-NumSoFar])
    NumSoFar=NumSoFar+1


#Find duplicates in list...
DupList=[]
Ind=0
while Ind < len(tokens):
    try:
        Place = tokens.index(tokens[Ind],Ind+1)
        DupList.append(Place)
        Ind=Ind+5
    except ValueError:
        Ind=Ind+5
#...and remove them.
while len(DupList) > 0:
    Ind = DupList.pop(-1)
    tokens[Ind:]= tokens[Ind+5:]

    
