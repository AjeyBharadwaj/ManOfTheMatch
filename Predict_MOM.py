import sys;
import urllib2;

Page = 0;
tempPage = 0;
flag = 0;
count = 0;
index = 0;
MOM = 0;
Players = 0;

batZScore = 1.34910375631;
bowlZScore = 0.607580831982;

def getBatsman( page ):
	dnbIndex1 = page.find('class="inningsTable"');
	dnbIndex2 = page.find('class="playerName"');
	
	if( dnbIndex1 < dnbIndex2 ):
		return [ page, '0',  0];
	
	index = page.find('class="inningsRow"');
	
	if ( index == -1 ):		# Global Exit .
		return [ page, '0',  0];
		
	page = page[index+5:];
	
	index = page.find( 'class="playerName"');
	if ( index == -1 ):
		return [ page, '0',  0];
		
	page = page[index+5:];
	
	index = page.find( 'class="playerName"');
	if ( index == -1 ):
		return [ page, '0',  0];
		
	page = page[index+1:];
		
	index1 = page.find('>');
	if ( index1 == -1 ):
		return [ page, '0',  0];
		
	index2 = page.find('<');
	if ( index2 == -1 ):
		return [ page, '0',  0];
	
	playerName = page[index1+1:index2];
	
	index = page.find('class="battingRuns"');
	page = page[index+1:];
	
	index1 = page.find('>');
	if ( index1 == -1 ):
		return [ page, '0',  0];
		
	index2 = page.find('<');
	if ( index2 == -1 ):
		return [ page, '0',  0];

	playerRuns = page[index1+1:index2];		
		
	return [ page, playerName, playerRuns ];
	
def getBatsmanNotBatted( page ):
	dnbIndex1 = page.find('class="inningsRow"');
	dnbIndex2 = page.find('class="playerName"');
	
	if( dnbIndex1 < dnbIndex2 ):
		#print str( dnbIndex1 );
		return [ page, '0',  0];
	
	index = page.find( 'class="playerName"');
	if ( index == -1 ):
		return [ page, '0',  0];
		
	page = page[index+1:];
		
	index1 = page.find('>');
	if ( index1 == -1 ):
		return [ page, '0',  0];
		
	index2 = page.find('<');
	if ( index2 == -1 ):
		return [ page, '0',  0];
	
	playerName = page[index1+1:index2];
	
	return [ page, playerName, 0 ];	
	
def getBowler( page ):
	dnbIndex1 = page.find('class="inningsTable"');
	dnbIndex2 = page.find('class="playerName"');
	
	if( dnbIndex1 < dnbIndex2 and dnbIndex1 != -1):
		#print page[dnbIndex1:dnbIndex1+150];
		return [ page, '0',  0];
	
	index = page.find('class="inningsRow"');
	
	if ( index == -1 ):		# Global Exit .
		#print '1';
		return [ page, '0',  0];
		
	page = page[index+5:];
	
	index = page.find( 'class="playerName"');
	if ( index == -1 ):
		#print '2';
		return [ page, '0',  0];
		
	page = page[index+5:];
	
	index = page.find( 'class="playerName"');
	if ( index == -1 ):
		#print '3';
		return [ page, '0',  0];
		
	page = page[index+1:];
		
	index1 = page.find('>');
	if ( index1 == -1 ):
		#print '4';
		return [ page, '0',  0];
		
	index2 = page.find('<');
	if ( index2 == -1 ):
		#print '5';
		return [ page, '0',  0];
	
	playerName = page[index1+1:index2];		
	
	for x in xrange(1,5):
		index = page.find('class="bowlingDetails"');
		page = page[index+1:];
	
	index1 = page.find('>');
	if ( index1 == -1 ):
		return [ page, '0',  0];
		
	index2 = page.find('<');
	if ( index2 == -1 ):
		return [ page, '0',  0];

	playerWick = page[index1+1:index2];		
	
	return [ page, playerName, playerWick ];	

def findTeams( page ):
	index = page.find( '<div class="notesSectionMain">' );
	page = page[index:];
	
	index1 = page.find('<b>');
	index2 = page.find(' innings');
	
	team1 = page[index1+3:index2];
	
	page = page[index2+2:];
	
	index1 = page.find('<b>');
	index2 = page.find(' innings');
	
	team2 = page[index1+3:index2];
	
	return [ team1, team2 ];

def findMOM( page ):
	
	index = page.find( 'Player of the match' );
	if( index == -1 ):
		print 'No Result';
		return [ 0, 0];
	page = page[index+20:];
	index1 = page.find('>');
	index2 = page.find(' (');
	
	MOMPlayer = page[index1+2:index2];
	 
	index1 = page.find(' (');
	index2 = page.find(')');
	
	wonTeam = page[index1+2:index2];
		
	return [MOMPlayer, wonTeam];
	
def predictedMOM():	
	totalRunsMean = 0.0;
	totalWickMean = 0.0;
	runsSD = 0.0;
	wickSD = 0.0;
	Max = 0;
	count = 0;
	Player = '';
	Team = '';
	global batZScore;
	global bowlZScore;
	
	for y in xrange(1, 12):
		if( Players[y] != []):
			totalRunsMean = totalRunsMean + float( Players[y][1] );
			totalWickMean = totalWickMean + float( Players[y][2] );
			count = count+1;
	
	totalRunsMean = totalRunsMean/count;
	totalWickMean = totalWickMean/count;
	
	#print totalRunsMean;
	#print totalWickMean;
	
	for y in xrange(1, 12):
		runsSD = runsSD + ( ( float( Players[y][1] ) - totalRunsMean ) * ( float( Players[y][1] ) - totalRunsMean ) );
		wickSD = wickSD + ( ( float( Players[y][2] ) - totalWickMean ) * ( float( Players[y][2] )- totalWickMean ) );
	
	runsSD = runsSD/count;
	wickSD = wickSD/count;
	
	runsSD = pow(runsSD, .5);
	wickSD = pow(wickSD, .5);
	
	
	for y in xrange(1, 12):
		if( Players[y] != [] ):
			Players[y][4] = ( float( Players[y][1] ) - totalRunsMean ) / runsSD ;	
			if( totalWickMean != 0):	
				Players[y][5] = ( float( Players[y][2] ) - totalWickMean ) / wickSD;	
	
	totalRunsMean = 0;
	totalWickMean = 0;
	runsSD = 0;
	wickSD = 0;
	count = 0;
			
	for y in xrange(12, 23):
		if( Players[y] != []):
			totalRunsMean = totalRunsMean + float( Players[y][1] );
			totalWickMean = totalWickMean + float( Players[y][2] );
			count = count+1;
	
	totalRunsMean = totalRunsMean/count;
	totalWickMean = totalWickMean/count;
	
	#print totalRunsMean;
	#print totalWickMean;
	
	for y in xrange(12, 23):
		runsSD = runsSD + ( ( float( Players[y][1] ) - totalRunsMean ) * ( float( Players[y][1] ) - totalRunsMean ) );
		wickSD = wickSD + ( ( float( Players[y][2] ) - totalWickMean ) * ( float( Players[y][2] )- totalWickMean ) );
	
	runsSD = runsSD/count;
	wickSD = wickSD/count;
	
	runsSD = pow(runsSD, .5);
	wickSD = pow(wickSD, .5);
	
	for y in xrange(12, 23):
		if( Players[y] != [] ):
			Players[y][4] = ( float( Players[y][1] ) - totalRunsMean ) / runsSD ;	
			if( totalWickMean != 0):	
				Players[y][5] = ( float( Players[y][2] ) - totalWickMean ) / wickSD;
	
	for y in xrange(1, 23):
		if( Players[y] != [] ):
			#X = pow( pow( ( float(Players[y][4]) - 1.3785 ), 2 )+ pow( ( float(Players[y][5]) - 0.602014), 2 ) , .5 );
			 
			X = float( Players[y][4] ) * batZScore + float( Players[y][5] ) * bowlZScore; 
			if( X > Max and Players[y][3] == MOM[1]):
				#print Players[y][0] + str( X );
				Player = Players[y][0];
				Team = Players[y][3];
				Max = X;
				
	#print 'Predicted : ' + Player ;
	return [ Player, Team ];

def prettyPrint():
	
	print '%20s %s %s %20s %10s %10s' %( 'Player', 'Runs', 'Wickets', 'Team', 'BatCont', 'BowCont');
	
	for x in xrange(1,12):
		print '%20s %3s %2s %20s %10s %10s' %(Players[x][0], Players[x][1], Players[x][2], Players[x][3], Players[x][4], Players[x][5]);
	
	print '';
	for x in xrange(12,23):
		print '%20s %3s %2s %20s %10s %10s' %(Players[x][0], Players[x][1], Players[x][2], Players[x][3], Players[x][4], Players[x][5]);
		

def main( url ):

	global flag;
	flag = 0;
	global count;
	count = 1;
	
	global Players;
	Players = [[]*24 for x in xrange(24)];

	for x in xrange(1, 24):
		Players[x].append('');	# Name
		Players[x].append(0);	# Runs
		Players[x].append(0);	# Wickets
		Players[x].append('');	# Team
		Players[x].append(0);	# Percentage Contribution in Batting
		Players[x].append(0);	# Percentage Contribution in Bowling
	
	Page = url;	
	tempPage = Page;	
	
	index = Page.find('class="inningsRow"');
	Page = Page[index:];
	
	Teams = findTeams(tempPage);
	#print Teams;

	#print '\n1st Side :'
	#print '\tBatsman batted: '

	for x in xrange(1,12):					# Get Batsman
		playerData = getBatsman( Page );	
		Page = playerData[0];
		name = playerData[1];
		runs = playerData[2];
	
		if( name == '0' ):
			#print 'Player not exist';
			break;
		else:
			#print '\t\t' + name +'\t'+ str( runs );
			name = name;
		
		for y in xrange(1, 23):
			if( Players[y] != [] and flag == 0):
				if( name == Players[y][0] ):
					Players[y][1] = runs;
					Players[y][3] = Teams[0];
					flag = 1;
				
		if( flag != 1 ):
			Players[count][0] = name;
			Players[count][1] = runs;
			Players[count][2] = 0;
			Players[count][3] = Teams[0];
			count = count+1;
		
		flag = 0;
		
	index = Page.find('class="inningsTable"');
	
	if ( index == -1 ):		
		#return [ page, '0',  0];
		#print index;
		exit();
	
	Page = Page[index+5:];

	index = Page.find( 'class="inningsDetails"');
	if ( index == -1 ):
		#return [ page, '0',  0];
		#print index;
		exit();
	
	Page = Page[index+5:];

	#print '\n\tBatsman not batted:';
	for x in xrange(1,12):					# Get Batsman not batted .
		playerData = getBatsmanNotBatted( Page );	
		Page = playerData[0];
		name = playerData[1];
		runs = playerData[2];
	
		if( name == '0' ):
			#print 'Player not exist';
			print '';
			break;
		else:
			#print '\t\t' + name + '\t' + str( runs );
			name = name;
	
		for y in xrange(1, 23):
			if( Players[y] != [] and flag == 0):
				if( name == Players[y][0] ):
					Players[y][1] = runs;
					Players[y][3] = Teams[0];
					flag = 1;
				
		if( flag != 1 ):
			Players[count][0] = name;
			Players[count][1] = 0;
			Players[count][2] = 0;
			Players[count][3] = Teams[0];
			count = count+1;
		
		flag = 0;
		
	index = Page.find('class="inningsRow"');
	Page = Page[index:];
		
	#print '\n\tBowler bowled:'; 		
	for x in xrange(1,12):					# Get Bowler
		playerData = getBowler( Page );	
		Page = playerData[0];
		name = playerData[1];
		wick = playerData[2];
	
		if( name == '0' ):
			#print 'Player not exist';
			break;
		else:
			#print '\t\t' + name +'\t' + str( wick ) ;
			name = name;
		
		for y in xrange(1, 23):
			if( Players[y] != [] and flag == 0):
				if( name == Players[y][0] ):
					Players[y][2] = wick;
					Players[y][3] = Teams[1];
					flag = 1;
				
		if( flag != 1 ):
			Players[count][0] = name;
			Players[count][1] = 0;
			Players[count][2] = wick;
			Players[count][3] = Teams[1];
			count = count+1;
		
		flag = 0;

	index = Page.find('class="inningsRow"');
	Page = Page[index:];

	#print '\n2nd Side :'
	#print '\tBatsman batted: '
	for x in xrange(1,12):					# Get Batsman
		playerData = getBatsman( Page );	
		Page = playerData[0];
		name = playerData[1];
		runs = playerData[2];
	
		if( name == '0' ):
			#print 'Player not exist';
			break;
		else:
			#print '\t\t' + name +'\t'+ str( runs );
			name = name;
	
		for y in xrange(1, 23):
			if( Players[y] != [] and flag == 0):
				if( name == Players[y][0] ):
					Players[y][1] = runs;
					Players[y][3] = Teams[1];
					flag = 1;
				
		if( flag != 1 ):
			Players[count][0] = name;
			Players[count][1] = runs;
			Players[count][2] = 0;
			Players[count][3] = Teams[1];
			count = count+1;
		
		flag = 0;
		
	index = Page.find('class="inningsTable"');
	
	if ( index == -1 ):		
		#return [ page, '0',  0];
		#print index;
		exit();
	
	Page = Page[index+5:];

	index = Page.find( 'class="inningsDetails"');
	if ( index == -1 ):
		#return [ page, '0',  0];
		#print index;
		exit();
	
	Page = Page[index+5:];

	#print '\n\tBatsman not batted:';
	for x in xrange(1,12):					# Get Batsman not batted .
		playerData = getBatsmanNotBatted( Page );	
		Page = playerData[0];
		name = playerData[1];
		runs = playerData[2];
	
		if( name == '0' ):
			#print 'Player not exist';
			print '';
			break;
		else:
			#print '\t\t' + name + '\t' + str( runs );
			name = name;
		
		for y in xrange(1, 23):
			if( Players[y] != [] and flag == 0):
				if( name == Players[y][0] ):
					Players[y][1] = 0;
					Players[y][3] = Teams[1];
					flag = 1;
				
		if( flag != 1 ):
			Players[count][0] = name;
			Players[count][1] = 0;
			Players[count][2] = 0;
			Players[count][3] = Teams[1];
			count = count+1;
	
		flag = 0;				
		
	index = Page.find('class="inningsRow"');
	Page = Page[index:];
		
	#print '\n\tBowler bowled:'; 		
	for x in xrange(1,12):					# Get Bowler
		playerData = getBowler( Page );	
		Page = playerData[0];
		name = playerData[1];
		wick = playerData[2];
	
		if( name == '0' ):
			#print 'Player not exist';
			break;
		else:
			#print '\t\t' + name +'\t' + str( wick ) ;
			name = name;			
	
		for y in xrange(1, 23):
			if( Players[y] != [] and flag == 0):
				if( name == Players[y][0] ):
					Players[y][2] = wick;
					Players[y][3] = Teams[0];
					flag = 1;
				
		if( flag != 1 ):
			Players[count][0] = name;
			Players[count][1] = 0;
			Players[count][2] = wick;
			Players[count][3] = Teams[0];
			count = count+1;
	
		flag = 0;	

	global MOM;
	MOM = findMOM( tempPage );
	My = predictedMOM();
	prettyPrint();	



	print '\nActual : Man of Match : ' + MOM[0] + ' . Team : ' + MOM[1];	
	print '\nPredicted : Man of Match : ' + My[0] + ' . Team : ' + My[1];	
	for y in xrange(1, 23):
		if( Players[y] != [] and flag == 0):
			if( MOM[0] == Players[y][0] ):
				#print '%s	%s' %( Players[y][4], Players[y][5]);
				flag = flag;
	#print Players
	return [Players, MOM, My];			
