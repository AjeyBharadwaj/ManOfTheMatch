import cgi
import webapp2
import urllib2;
import Predict_MOM;

from google.appengine.api import users

from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage( webapp2.RequestHandler ):
    def get(self):
        self.response.out.write("""
          <html>
          	<head>
          		<title> Predict Man of the Match . </title>
                        <style>
                            h1 {text-align:center}
                            input#search
                                {
                                    width: 200px;
                                    height: 200px;
                                }
                        </style>
          	</head>
          	
          	<body>
    			<h1>MAN OF THE MATCH PREDICTOR</h1>  
    			<form action="/result" method="post">
                            <h2>Enter URL here : </h2><input type = "text" name = "siteurl" size = "100"/><br/>
	                <br/><div><input type="submit" value="Find MOM" style="width: 100px; height: 50px;"/></div>
	            </form>
	            <h3>Special thanks to : </br>
	            	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 1 . https://www.cricinfo.com .</br>
	            	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 2 . https://www.developers.google.com/appengine/ .</br>
	            	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 3 . https://www.wikipedia.com .</br>
                <h3>Steps : <br/>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 1 . Paste URL of Crickinfo.com into the text box . (Ex : http://www.espncricinfo.com/indvsl2009/engine/current/match/430887.html ) .<br/>
                    &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 2 . Click "Find MOM" button .<br/>
                </h3>
                <h3>Algorithm : </br>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 1 . Read the page source of given url .<br/>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 2 . Read each players attributes ( runs, wickets ) .<br/>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 3 . Compute the individual z-score .<br/>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 4 . Normalize the data .<br/>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 5 . Find which player has heighest contribution( combining runs and wickets ) .<br/>
                </h3>
                <h3>Steps used to find normalising vector : </br>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 1 . Taken 5 IPL seasons data as historical data .<br/>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 2 . For each match calculate the z-score of the player who has got man of the match.<br/>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 3 . Find the average value .<br/>
                </h3>
                <h3>Problems with the predictor : </br>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 1 . Works only for One-day and T20.<br/>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 2 . Cannot predict if the match ends with no result.<br/>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 3 . Cannot predict if anybody is reteired hurt .<br/>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 4 . Taken only runs and wickets as deciding factors on man of the match.<br/>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 5 . Player in the winning team will have heighest priority.</br>
                	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp 6 . Concentrates only on overall performance .
                </h3>
	        </body>
          </html>""");


class DispResult(webapp2.RequestHandler):
    def post(self):
    	text = urllib2.urlopen( self.request.get('siteurl') ).read();
    	self.response.headers['Content-Type'] = 'text/html';
        [Players, MOM, My] = Predict_MOM.main( text );
        
        tableData = '';
        tableData = '<tr><th><pre><h2>          Player Name      </h2></pre></th><th><pre><h2>  Runs </h2></pre><th><pre><h2>   Wickets </h2></pre><th><pre><h2>      Team      </h2></pre><th><pre><h2>     Batting Contribution   </h2></pre><th><pre><h2>      Bowling Contribution   </h2></pre><th></tr>';
        
	for x in range(1,23):
            tableData = tableData + '<tr><td>    ' + str( Players[x][0] ) + '    </td>' + '<td>    ' + str( Players[x][1] ) + '    </td>' + '<td>    ' + str( Players[x][2] ) + '    </td>' + '<td>    ' + str( Players[x][3] ) + '    </td>' + '<td>    ' + str( Players[x][4] ) + '    </td>' + '<td>    ' + str( Players[x][5] ) + '    </td>' + '</tr>';																		
        
        self.response.out.write( """<html>
          	<head>
          		<title> Predict Man of the Match . </title>
          	</head>
          	<body>
                    <table border = "1"> """ + tableData + """</table><br/>
                    <h2> Man of the Match </h2> <table border = "1"> <tr> <th> <pre><h2>  Actual  </h2></pre></th><th><pre><h2>  Predicted  </h2></pre></th></tr> <tr><td><h4> """ + MOM[0] + """ </h4></td><td><h4> """ + My[0] + """ </h4></td> </tr> </table> 
                </body>
                </html>""" );
        
app = webapp2.WSGIApplication([('/', MainPage),
                              ('/result', DispResult)],
                              debug=True);
