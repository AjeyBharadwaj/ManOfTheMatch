import urllib2;

#IPL 1
#page = urllib2.urlopen( 'http://www.espncricinfo.com/ci/engine/match/335982.html' ).read();
startPage = 335982;
endPage	  = 336041;

for fileno in xrange( startPage, endPage):
	page = urllib2.urlopen( 'http://www.espncricinfo.com/ci/engine/match/'+str( fileno )+'.html' ).read();
	newFile = open( str( fileno )+'.txt' , 'w' );
	newFile.write( page );
	newFile.close();
	print 'Saved '+ str( fileno-startPage+1 ) + 'th match result.';
	
#IPL 2
#page = urllib2.urlopen( 'http://www.espncricinfo.com/ci/engine/match/335982.html' ).read();
startPage = 392181;
endPage	  = 392240;

for fileno in xrange( startPage, endPage):
	page = urllib2.urlopen( 'http://www.espncricinfo.com/ipl2009/engine/match/'+str( fileno )+'.html' ).read();
	newFile = open( str( fileno )+'.txt' , 'w' );
	newFile.write( page );
	newFile.close();
	print 'Saved '+ str( fileno-startPage+1 ) + 'th match result.';


#IPL 3
startPage = 419106;
endPage	  = 419166;

for fileno in xrange( startPage, endPage):
	page = urllib2.urlopen( 'http://www.espncricinfo.com/ipl2010/engine/match/'+str( fileno )+'.html' ).read();
	newFile = open( str( fileno )+'.txt' , 'w' );
	newFile.write( page );
	newFile.close();
	print 'Saved '+ str( fileno-startPage+1 ) + 'th match result.';
	
#IPL 4
startPage = 501198;
endPage	  = 501272;

for fileno in xrange( startPage, endPage):
	page = urllib2.urlopen( 'http://www.espncricinfo.com/indian-premier-league-2011/engine/match/'+str( fileno )+'.html' ).read();
	newFile = open( str( fileno )+'.txt' , 'w' );
	newFile.write( page );
	newFile.close();
	print 'Saved '+ str( fileno-startPage+1 ) + 'th match result.';
	
#IPL 5
startPage = 548306;
endPage	  = 548382;

for fileno in xrange( startPage, endPage):
	page = urllib2.urlopen( 'http://www.espncricinfo.com/indian-premier-league-2012/engine/match/'+str( fileno )+'.html' ).read();
	newFile = open( str( fileno )+'.txt' , 'w' );
	newFile.write( page );
	newFile.close();
	print 'Saved '+ str( fileno-startPage+1 ) + 'th match result.';		
