import recsyscollfilter as rec
import getopt, sys
import random

def usage():
    print("""Usage:
            -u to print user statistics
            -i to print item statistics
            -g to print general statistics
            --help to see usage menu              """)

def general_stats(user_count, item_count, ratings_count, density):
    print("--- General statistics: ---")
    print("Number of users: ", user_count)
    print("Number of items: ", item_count)
    print("Number of ratings: ", ratings_count)
    print("Ratings density metric: ", density)

def user_stats(users):
    users = rec.user_stats(users)
    print("\n\n--- User statistics: ---")
    for user, user_dict in users.items():
        print("User: ", user_dict.id)
        print("Mean rating:", user_dict.rating_mean)
        print("Median rating:", user_dict.rating_median)
        if len(user_dict.ratings.items()) > 1:
            print("Standard deviation rating:", user_dict.rating_mean)
        print("Min rating:", user_dict.rating_min)
        print("Max rating:", user_dict.rating_max, "\n")

def mean_item_rating_func(users, item_ratings, item_count, user_count):
    print ("\n--- Testing mean_item_rating() function: ---")
    exists = 0
    while exists == 0:
        user_rndm = random.randint(1, len(users))
        exists = len([u for u in users.keys() if u == user_rndm])
    exists = 0
    while exists == 0:
        item_rndm = random.randint(1, len(item_ratings))
        exists = len([i for i in item_ratings.keys() if i == item_rndm])
    print ("Randomly chose user ", user_rndm, " and item ", item_rndm)
    rating = rec.mean_item_rating(users, user_rndm, item_rndm, item_ratings)
    if rating is not None:
        print ("Predicted rating for user", user_rndm, "and item", item_rndm, "is: ", rating)
    else:
        print ("Predicted rating for user ", user_rndm, " and item_rndm could not be calculated.")
    items_single = len([item for item, item_dict in item_ratings.items() if len(item_dict)==1])
    mean_item_rating_coverage = rec.coverage_calc(user_count*item_count - items_single, item_count, user_count)
    print ("\nCoverage using simple l10 mean_item_rating() is: ", mean_item_rating_coverage)


if __name__ == '__main__':
    print_user_stats = False
    print_general_stats = False
    print_item_stats = False
    test_mean_item_rating = False

    if (len(sys.argv[1:]) == 0):
        usage()
        sys.exit()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "iugm", ["help"])
    except getopt.GetoptError as err:
        print (str(err))
        usage()
        sys.exit(2)
    for flag, a in opts:
        if flag == "-u":
            print_user_stats = True
        elif flag == "-i":
            print_item_stats = True
        elif flag == "-g":
            print_general_stats = True
        elif flag == "-m":
            test_mean_item_rating = True
        else:
            usage()
            sys.exit()

    # Read in data
    users = {}
    item_ratings = {}
    ratings_count = 0
    item_ratings, users, ratings_count = rec.read_data()
    item_count = len(item_ratings)
    user_count = len(users)

    # Key statistics
    user_count, item_count, density = rec.general_stats(item_ratings, users, ratings_count)
    if print_general_stats:
        general_stats(user_count, item_count, ratings_count, density)
    if print_user_stats:
        user_stats(users)
    if print_item_stats:
        rec.item_stats(item_ratings)

    # Mean item rating
    if test_mean_item_rating:
        mean_item_rating_func(users, item_ratings, item_count, user_count)
