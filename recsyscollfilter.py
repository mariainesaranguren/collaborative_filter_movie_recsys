#!/usr/bin/python3
import csv
import statistics
import math
import time
from user import User

def cos_range_to_pearson_range(x):
    cos_min = 0
    cos_max = 1
    cos_range = cos_max - cos_min
    pearson_min = -1
    pearson_max = 1
    pearson_range = pearson_max - pearson_min
    return (((x-cos_min)*pearson_range)/cos_range)+pearson_min

def assign_neighbors_threshold(users, user_similarity, similarity_min):
    print("   Creating user neighborhoods...")
    time_start = time.time()
    for user in users.values():
        user.neighbors = []                                                         # Clear neighbors to re-assign them
    for user_id_1, user_1 in users.items():                                         # For every user, loop through all other users
        for user_id_2, user_2 in users.items():
            if user_id_1 != user_id_2:
                if user_id_1 < user_id_2:                                           # Determine if user would be in first or second key of user_similarity (nested dict of {user_1:{user_2:similarity}})
                    if user_similarity[user_id_1][user_id_2] >= similarity_min:     # If similarity metric meets minimum similarity requirement, save neighbor on neighbors attribute of user
                        user_1.neighbors.append(user_id_2)
                else:
                    if user_similarity[user_id_2][user_id_1] >= similarity_min:     # If similarity metric meets minimum similarity requirement, save neighbor on neighbors attribute of user
                        user_1.neighbors.append(user_id_2)
    time_end = time.time()
    print("\tTime taken to create neighborhoods:", time_end - time_start, "seconds")
    return


def assign_neighbors_percent(users, user_similarity, percent, similarity_metric):
    print("   Creating user neighborhoods...")
    time_start = time.time()
    for user_id, user in users.items():                                             # Loop through all users to assign their neighbors
        neighbors = {}                                                              # Create neighbors dictionary to store all related users
        if user_id in user_similarity.keys():                                       # Look for their related neighbors in user_similarity{} (nested dict of {user_1:{user_2:similarity}}) where the id is the first key
            for n, sim in user_similarity[user_id].items():
                neighbors[n] = sim
        for user_1, sim in user_similarity.items():                                 # Look for their related neighbors in user_similarity{} (nested dict of {user_1:{user_2:similarity}}) where the id is the second key
            for user_2, rating in sim.items():
                if user_id == user_2:
                    neighbors[user_1] = rating
        percent_size = int(len(neighbors)*percent)                                  # Calculate the amount of neighbors that represent the given percent of all neighbors
        neighbors = sorted(neighbors.items(), key=lambda x:x[1], reverse=True)      # Sort neighbors by descending value (similarity)
        for n in range (0, percent_size):                                           # Copy the key (id) of the top neighbors to the user's neighbors list
            n_id = neighbors[n][0]
            n_sim = neighbors[n][1]
            if (similarity_metric==pearson_similarity and n_sim > 0):               # If similarity metric is pearson similarity, only assign neighbor if similarity is positive
                user.neighbors.append(n_id)
            elif (similarity_metric is not pearson_similarity):
                user.neighbors.append(n_id)
    time_end = time.time()
    print("\tTime taken to create neighborhoods:", time_end - time_start, "seconds")
    return


def assign_neighbors_k_nearest(users, user_similarity, k, similarity_metric):
    print("   Creating user neighborhoods...")
    time_start = time.time()
    for user_id, user in users.items():                                             # Loop through all users to assign their neighbors
        neighbors = {}                                                              # Create neighbors dictionary to store all related users
        if user_id in user_similarity.keys():                                       # Look for their related neighbors in user_similarity{} (nested dict of {user_1:{user_2:similarity}}) where the id is the first key
            for n, sim in user_similarity[user_id].items():
                neighbors[n] = sim
        for user_1, sim in user_similarity.items():                                 # Look for their related neighbors in user_similarity{} (nested dict of {user_1:{user_2:similarity}}) where the id is the second key
            for user_2, rating in sim.items():
                if user_id == user_2:
                    neighbors[user_1] = rating
        neighbors = sorted(neighbors.items(), key=lambda x:x[1], reverse=True)      # Sort neighbors by descending value (similarity)
        if len(neighbors) < k:                                                      # Determine which of k and len(neighbors) is greater to avoid trying to access values out of bounds
            upper_limit = len(neighbors)
        else:
            upper_limit = k
        for n in range (0, upper_limit):                                            # Copy the key (id) of the top neighbors to the user's neighbors list
            n_id = neighbors[n][0]
            n_sim = neighbors[n][1]
            if (similarity_metric==pearson_similarity and n_sim > 0):               # If similarity metric is pearson similarity, only assign neighbor if similarity is positive
                user.neighbors.append(n_id)
            elif (similarity_metric is not pearson_similarity):
                user.neighbors.append(n_id)
    time_end = time.time()
    print("\tTime taken to create neighborhoods:", time_end - time_start, "seconds")
    return


def populate_user_similarity(similarity_metric, min_corated, users):
    print("Finding similarity between users...")
    time_start = time.time()
    similarity = []
    user_similarity = {}
    for user_1 in users.keys():                                                                                  # For each user, loop through all other users
        for user_2 in users.keys():
            if user_1 != user_2:
                if user_1 < user_2:                                                                              # Determine which id is lower to store key as lowest user_id of the two
                    if user_1 not in user_similarity.keys():
                        user_similarity[user_1] = {}
                    sim_calc =  similarity_metric(users, user_1, user_2, min_corated)                            # Calculate similarity with argument method
                    user_similarity[user_1][user_2] = sim_calc                                                   # Save calculated similarity in user_similarity{} (nested dict of {user_1:{user_2:similarity}})
                else:
                    if user_2 not in user_similarity.keys():
                        user_similarity[user_2] = {}
                    sim_calc = similarity_metric(users, user_1, user_2, min_corated)
                    user_similarity[user_2][user_1] = sim_calc
                similarity.append(sim_calc)
    time_end = time.time()
    print("Total time to find similarity between users: ", time_end-time_start, "seconds")
    user_similarity_mean = statistics.mean(similarity)
    user_similarity_stdev = statistics.stdev(similarity)
    return user_similarity, user_similarity_mean, user_similarity_stdev


def cosine_similarity(users, user_id_1, user_id_2, min_corated):    # Find cosine similarity between two users
    try:                                                                                # Find given users in users dictionary
        user_1 = users[user_id_1]
        user_2 = users[user_id_2]
    except KeyError:
        return 0

    corated_items = set(user_1.ratings.keys()).intersection(user_2.ratings.keys())      # Find items co-rated by both given users

    if len(corated_items) < min_corated:                                                # If users have not co-rated enough items, return similarity o 0
        return 0
    else:                                                                               # Calculate cosine similarity between the two
        numerator_1 = []
        numerator_2 = []
        denominator_1 = 0
        denominator_2 = 0
        for item in corated_items:
            numerator_1.append(user_1.ratings[item])
            numerator_2.append(user_2.ratings[item])
            denominator_1 += pow(user_1.ratings[item], 2)
            denominator_2 += pow(user_2.ratings[item], 2)

        numerator = sum(user_1_stats * user_2_stats for user_1_stats, user_2_stats in zip(numerator_1, numerator_2))
        denominator_1 = math.sqrt(denominator_1)
        denominator_2 = math.sqrt(denominator_2)
        denominator = denominator_1 * denominator_2
        similarity = numerator/denominator

    return similarity                                                                    # Return calculated cosine similarity


def pearson_similarity(users, user_id_1, user_id_2, min_corated):   # Find pearson similarity between two users
    try:                                                                            # Find given users in users dictionary
        user_1 = users[user_id_1]
        user_2 = users[user_id_2]
    except KeyError:
        return 0

    numerator_sum = 0
    denominator_1 = 0
    denominator_2 = 0

    corated_items = set(user_1.ratings.keys()).intersection(user_2.ratings.keys())  # Find items co-rated by both given users

    if len(corated_items) < min_corated:                                            # If users have not co-rated enough items, return similarity of 0
        return 0
    else:                                                                           # Calculate pearson similarity between users
        i=0
        for item in corated_items:
            numerator_1 = user_1.ratings[item] - user_1.rating_mean
            numerator_2 = user_2.ratings[item] - user_2.rating_mean
            numerator_sum += (numerator_1 * numerator_2)
            denominator_1 += pow((user_1.ratings[item] - user_1.rating_mean), 2)
            denominator_2 += pow((user_2.ratings[item] - user_2.rating_mean), 2)
            i+=1
        denominator_final = math.sqrt(denominator_1) * math.sqrt(denominator_2)

    if denominator_final == 0:
        return 0
    correlation_factor = numerator_sum/denominator_final                            # Return pearson similarity correlation factor
    return correlation_factor


def mean_item_rating_neighbors(users, user_id, item_id, item_ratings):      # Given (user_id, item_id) returns the average rating for the item across all ratings for it except rating by given user
    user_target = users[user_id]
    ratings_found = [rating for user, rating in item_ratings[item_id].items() if user in user_target.neighbors]     # Find ratings of user neighbors for the specified item
    if len(ratings_found) > 0:                                    # If ratings were found, calculate mean and return value
        return statistics.mean(ratings_found)
    return None


def mean_item_rating(users, user_id, item_id, item_ratings):                # Given (user_id, item_id) returns the average rating for the item across all ratings for it except rating by given user if it exists
    ratings_found = [rating for user, rating in item_ratings[item_id].items() if user!=user_id]     # Finds ratings for given item for all users except given user
    if len(ratings_found) > 0:                  # If ratings were found, calculate mean and return value
        return statistics.mean(ratings_found)
    else:                                       # Could not find ratings
        return None


def resnicks_pearson_prediction(users, user_id, item_id, user_similarity):
    user = users[user_id]                                                   # Find user
    numerator = 0
    denominator = 0
    if user.neighbors == []:                                                # If user has no neighbors, return None (prediction cannot be made)
        return None

    for neighbor in user.neighbors:                                         # Loop through neighbors of user
        if item_id in users[neighbor].ratings.keys():                       # If neighbor has rated item, consider neighbor for prediction calculations
            if user.id < neighbor:
                numerator += ((users[neighbor].ratings[item_id] - users[neighbor].rating_mean) * user_similarity[user.id][neighbor])
                denominator += abs(user_similarity[user.id][neighbor])
            else:
                numerator += ((users[neighbor].ratings[item_id] - users[neighbor].rating_mean) * user_similarity[neighbor][user.id])
                denominator += abs(user_similarity[neighbor][user.id])

    if denominator == 0:                                                    # Return none for predictions that can't be made
        return None

    prediction = user.rating_mean + numerator/float(denominator)            # Calculate prediction and return
    return prediction


def resnicks_cosine_prediction(users, user_id, item_id, user_similarity):
    user = users[user_id]                                                   # Find user
    numerator = 0
    denominator = 0
    if user.neighbors == []:                                                # If user has no neighbors, return None (prediction cannot be made)
        return None

    for neighbor in user.neighbors:                                         # Loop through neighbors of user
        if item_id in users[neighbor].ratings.keys():                       # If neighbor has rated item, consider neighbor for prediction calculations
            if user.id < neighbor:
                numerator += ((users[neighbor].ratings[item_id] - users[neighbor].rating_mean) * cos_range_to_pearson_range(user_similarity[user.id][neighbor]))
                denominator += abs(cos_range_to_pearson_range(user_similarity[user.id][neighbor]))
            else:
                numerator += ((users[neighbor].ratings[item_id] - users[neighbor].rating_mean) * cos_range_to_pearson_range(user_similarity[neighbor][user.id]))
                denominator += abs(cos_range_to_pearson_range(user_similarity[neighbor][user.id]))

    if denominator == 0:                                                    # Return none for predictions that can't be made
        return None

    prediction = user.rating_mean + numerator/float(denominator)            # Calculate prediction and return
    return prediction


def simple_l10(users, item_ratings, item_count, user_count):
    make_predictions(mean_item_rating, "simple_l10_results.csv", users, item_ratings, item_count, user_count)


def make_predictions(prediction_method, file_name, users, item_ratings, item_count, user_count):
    print("   Making predictions...")
    all_err = []
    predictions_made = 0
    time_start = time.time()                                                # Saves time of start to calculate procedure runtime

    with open(file_name, 'w') as csvfile:                                   # Opens csv file to save results
        results_writer = csv.writer(csvfile, delimiter=',')
        for user, user_ratings in users.items():                            # Loops through all users and all items to make predictions
            for item in item_ratings.keys():
                predicted_rating =  prediction_method(users, user, item, item_ratings)      # Generate prediction with argument prediction method
                                                                                            # *Note: In calculating prediction with Resnick's formula, the last parameter is actually the user_similarity dictionary
                if predicted_rating is not None:                                            # Count prediction if it was made
                    predictions_made += 1                                                   # If actual rating exists, analyze prediction for error calculations
                    if item in user_ratings.ratings.keys():
                        actual_rating = user_ratings.ratings[item]
                        err = predicted_rating - float(actual_rating)
                        all_err.append(err)
                        results_writer.writerow([user, item, actual_rating, predicted_rating, abs(err)])    # Write findings to csv file
        squared_error = 0
        for i in range(0, len(all_err)):                                    # Calculate error in predictions
            squared_error += pow(all_err[i], 2)
        overall_rmse = math.sqrt(squared_error/len(all_err))
        print ("\tOverall RMSE:\t\t", overall_rmse)
        time_end = time.time()
        total_time = time_end-time_start
        print ("\tTotal calculation time:\t", total_time, "seconds")
        coverage = coverage_calc(predictions_made, item_count, user_count)
        print ("\tCoverage:\t\t", str(coverage))
        results_writer.writerow([overall_rmse, total_time, coverage_calc(predictions_made, item_count, user_count)])
        csvfile.close()
    return overall_rmse, total_time, coverage


def general_stats(item_ratings, users, ratings_count):
    user_count = len(users)
    item_count = len(item_ratings)
    density = ratings_count / float(len(users) * len(item_ratings))
    return user_count, item_count, density


def user_stats(users):
    for user, user_dict in users.items():                                       # Loop through all users and generate general user statistics and save findings in corresponding user attributes
        user_ratings_all = user_dict.ratings.values()
        user_dict.rating_mean = statistics.mean(user_ratings_all)
        user_dict.rating_median = statistics.median(user_ratings_all)
        user_dict.rating_min = min(user_ratings_all)
        user_dict.rating_max = max(user_ratings_all)
        if len(user_ratings_all) > 1:
            user_dict.rating_std_dev = statistics.stdev(user_ratings_all)
        user_dict.neighbors = []
    return users


def item_stats(item_ratings):
    print("\n\n--- Item statistics: ---")
    for item, user_ratings in item_ratings.items():                                     # Loop through items and generate general item statistics
        print ("\nItem: ", item)
        item_ratings_all = user_ratings.values()
        print("Number of ratings: ", len(item_ratings_all))
        print("Mean rating: ", statistics.mean(item_ratings_all))
        print ("Median rating: ", statistics.median(item_ratings_all))
        if len(item_ratings_all) > 1:
            print ("Standard deviation: ", statistics.stdev(item_ratings_all))
        print ("Min rating: ", min(item_ratings_all))
        print ("Max rating: ", max(item_ratings_all))
    print ("\nDistribution of ratings (based on mean rating):")
    five_star = len([item for item, rating_dict in item_ratings.items() if statistics.median(rating_dict.values()) == 5])
    four_star = len([item for item, rating_dict in item_ratings.items() if statistics.median(rating_dict.values()) == 4])
    three_star = len([item for item, rating_dict in item_ratings.items() if statistics.median(rating_dict.values()) == 3])
    two_star = len([item for item, rating_dict in item_ratings.items() if statistics.median(rating_dict.values()) == 2])
    one_star = len([item for item, rating_dict in item_ratings.items() if statistics.median(rating_dict.values()) == 1])
    print ("Five stars:", five_star)
    print ("Four stars:", four_star)
    print ("Three stars:", three_star)
    print ("Two stars:", two_star)
    print ("One star:", one_star)
    return


def coverage_calc(predictions_made, item_count, user_count):
    return predictions_made/float(user_count*item_count)            # Given number of predictions made, calculate coverage


def read_data():
    ratings_count = 0
    users = {}
    item_ratings = {}
    user_ratings = {}                                               # Temporary dictionary that holds rating information for each user; key = user, value = {item, rating} dictionary
    with open('ratings.csv', 'r') as csvfile:
        read = csv.reader(csvfile, delimiter=',')
        for line in read:                                           # Line has user_id, item_id, rating, timestamp
            user_id = int(line[0])
            item_id = int(line[1])
            rating_val = int(line[2])
            if user_id not in user_ratings.keys():                  # If user is not in dictionary, create entry with user as key and dictionary as value
                user_ratings[user_id] = {}
            if item_id not in item_ratings.keys():                  # If item is not in dictionary, create entry with item as key and dictionary as value
                item_ratings[item_id] = {}
            user_ratings[user_id].update({item_id: rating_val})
            item_ratings[item_id].update({user_id: rating_val})     # Add newly found (user, rating) in item's dictionary
            ratings_count += 1
    for user_id in user_ratings:                                    # Loop through all users in user_ratings{}
        new_user = User()                                           # Create instance of User class for each user
        new_user.id = user_id                                       # Save id and ratings information of that user in its attributes
        new_user.ratings = user_ratings[user_id]
        users[user_id] = new_user                                   # Add user object to users{}
    csvfile.close()
    return item_ratings, users, ratings_count
