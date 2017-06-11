MAN OF THE MATCH PREDICTOR

File : 
		Cricket.py          	:           Python files that runs in Google App Engine.
		Generate_Vector.py		:			Find the normalising vector by taking the historical data as reference .
		Predict_MOM.py			:			For a given URL find Man of the match ( actual and predicted ) .
		Save_Data.py			:			Download the historical data ( results of all matches in IPL 1-5 ) .						
		Readme.txt				:			This file .
		
Steps to run app locally : 
		1 . Run Save_Data.py which downloads historical data .
		2 . Run Generate_Vector.py which generates normalising vector .		
		3 . Substitute these values in the file Predict_MOM.py .
		4 . Run Predict_MOM.py by passing files name as argument .
