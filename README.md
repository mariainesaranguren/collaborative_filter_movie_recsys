This is a project that does collaborative filtering on movie ratings to provide recommendations for users based on the ratings of other users and the similarity between them.

*** This project must be run using python3 ***

Where to find what:
- Report is in this same directory (PDF)
- Code:
	user.py 		-- User class definition
	recsyscollfilter.py 	-- most of the functionality of the code
	tasks*.py		-- tasks 1-4 in separate files
- Results collected in "Results" directory. This is just a sample of the results.

This project is broken down into four main tasks:
Task 1: Reading in data and simple data statistics 
Run with the following command:
	$ python3 task1.py [options]

	Options:
	-u to print user statistics
        -i to print item statistics
        -g to print general statistics
        --help to see usage menu

Task 2: Mean item rating
Run with the following command:
	$ python3 task2.py

Task 3: Distance-based collaborative filtering
Run with the following command:
	$ python3 task3.py [options]

	Options:
  	-h, --help  show this help message and exit
  	--a         All of the below
  	--kp        K-nearest neighborhoods based on Pearson's similarity
  	--kc        K-nearest neighborhoods based on cosine similarity
  	--pp        Top n percent neighborhoods based on Pearson's similarity
  	--pc        Top n percent neighborhoods based on cosine similarity
  	--tp        Minimum similarity threshold neighborhoods based on Pearson's
              	    similarity
  	--tc        Minimum similarity threshold neighborhoods based on cosine
       		    similarity

Task 4: Distance-based collaborative filtering with Resnick's Formula
Run with the following command:
        $ python3 task4.py [options]

        Options:
        -h, --help  show this help message and exit
        --a         All of the below
        --kp        K-nearest neighborhoods based on Pearson's similarity
        --kc        K-nearest neighborhoods based on cosine similarity
        --pp        Top n percent neighborhoods based on Pearson's similarity
        --pc        Top n percent neighborhoods based on cosine similarity
        --tp        Minimum similarity threshold neighborhoods based on Pearson's
                    similarity
        --tc        Minimum similarity threshold neighborhoods based on cosine
                    similarity


If you are interested in only making a few predictions, please run the following commands:
	$ import recsyscollfilter as rec
	$ users = {}
    	$ item_ratings = {}
    	$ ratings_count = 0

    	$ # Read in data
    	$ item_ratings, users, ratings_count = rec.read_data()
    	$ item_count = len(item_ratings)
    	$ user_count = len(users)

Once you have read in the data and organized it, you can do predictions for a specific user and item pair:
For simple mean item rating:
	$ prediction = rec.mean_item_rating(users, user_id, item_id, item_ratings)
For any of the similarity-based ratings, first run these commands to calculate similarity between users:
	$ similarity_metric = rec.<similarity method> where <similarity method> can be cosine_similarity or pearson_similarity
	$ user_similarity, user_sim_mean, user_sim_stdev = rec.populate_user_similarity(similarity_metric, min_corated_items, users)
Then, to create neighborhoods, choose your method and run the corresponding command(s):
	$ k = <val>
	$ rec.assign_neighbors_k_nearest(users, user_similarity, k, similarity_metric)
		-- or --
	$ p = <decimal percent>
	$ rec.assign_neighbors_percent(users, user_similarity, percent, similarity_metric)
	        -- or --
	$ similarity_minimum = <value>
	$ rec.assign_neighbors_threshold(users, user_similarity, similarity_min)
Finally, to make the prediction, run the two following commands and then choose one of the three methods (make sure that you choose the correct one between resnicks_pearson and resnicks_cosine to match with your similarity metric):
	$ user_id = <value>
	$ item_id = <value>

	$ rec.mean_item_rating_neighbors(users, user_id, item_id, item_ratings)
	        -- or --
	$ rec.resnicks_pearson_prediction(users, user_id, item_id, user_similarity)
	        -- or --
	$ rec.resnicks_cosine_prediction(users, user_id, item_id, user_similarity)
