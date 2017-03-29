import recsyscollfilter as rec

if __name__ == '__main__':
    users = {}
    item_ratings = {}
    ratings_count = 0

    # Read in data
    item_ratings, users, ratings_count = rec.read_data()
    item_count = len(item_ratings)
    user_count = len(users)

    # 1) Simple leave one out predictions
    print("* Please be patient. Generating predictions can take a few minutes.\n")
    print("Generating simple leave one out predictions:")
    rec.simple_l10(users, item_ratings, item_count, user_count)
    print("\nThe results of this test were saved in simple_l10_results.csv")
    print("In this file, each line represents a user id, an item id, the actual rating, a predicted rating, and error found.")
    print("The last line of the file contains the overall rmse, total time, and coverage of the prediction cycle.")
