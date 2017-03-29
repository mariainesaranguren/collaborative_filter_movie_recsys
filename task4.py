import recsyscollfilter as rec
from matplotlib import pyplot as plt
import sys
from optparse import OptionParser

def cos_range_to_pearson_range(x):
    cos_min = 0
    cos_max = 1
    cos_range = cos_max - cos_min
    pearson_min = -1
    pearson_max = 1
    pearson_range = pearson_max - pearson_min
    return (((x-cos_min)*pearson_range)/cos_range)+pearson_min

def generate_graphs(x_axis, rmse, time, coverage, curve_label, graph_name, x_axis_label):
    metric = [rmse, time, coverage]
    metric_name = ["RMSE", "Time (s)", "Coverage (%)"]
    metric_name_short = ["RMSE", "time", "coverage"]
    for i in range(0, 3):
        x = x_axis
        y1 = metric[i]
        plt.plot(x, y1, label=curve_label)
        title = "Prediction Results: " + metric_name[i] + " vs. "+x_axis_label
        plt.suptitle(title)
        plt.ylabel(metric_name[i])
        xlabel = x_axis_label
        plt.xlabel(xlabel)
        plt.legend(loc='best')
        fig_name = graph_name+"vs_"+metric_name_short[i]+".png"
        plt.savefig(fig_name)
        plt.clf()
        print("The "+metric_name_short[i]+" graph has been saved in "+fig_name)

def similarity_threshold(similarity_method, similarity_method_name, similarity_method_name_short):
    if similarity_method == rec.cosine_similarity:
        prediction_method = rec.resnicks_cosine_prediction
    else:
        prediction_method = rec.resnicks_pearson_prediction
    print("---------------------------------------------------------------------------")
    print("* Please be patient. Generating predictions can take a few minutes.\n")
    print("Generating predictions...")
    print("Neighborhoods created by:\tMinimum similarity threshold")
    print("Similarity metric used: \t", similarity_method_name, "\n")
    min_corated_items = 5
    user_similarity, user_sim_mean, user_sim_stdev = rec.populate_user_similarity(similarity_method, min_corated_items, users)
    similarity_min_cutoffs = [0.95, 0.90, 0.80, 0.70, 0.60, 0.50]
    if similarity_method_name == "Pearson's similarity":
        similarity_min_cutoffs = [cos_range_to_pearson_range(s) for s in similarity_min_cutoffs]
    rmse_all = []
    time_all = []
    coverage_all = []

    print("\nGenerating predictions across different minimum similarity thresholds for purposes of comparison:")
    for min_similarity_req in similarity_min_cutoffs:
        print("- Minimum similarity threshold: ", min_similarity_req)
        # Create neighborhood
        rec.assign_neighbors_threshold(users, user_similarity, min_similarity_req)
        # Make predictions
        output_file_name = "resnicks_"+similarity_method_name_short + str(min_similarity_req) + "_min_results.csv"
        overall_rmse, total_time, coverage = rec.make_predictions(prediction_method, output_file_name, users, user_similarity, item_count, user_count)
        print("\tResults saved in:\t", output_file_name)
        rmse_all.append(overall_rmse)
        time_all.append(total_time)
        coverage_all.append(coverage)
    curve_label = "Resnick's Formula with "+similarity_method_name
    generate_graphs(similarity_min_cutoffs, rmse_all, time_all, coverage_all, curve_label, "resnicks_"+similarity_method_name_short+"min_similarity_", "Minimum Similarity Between Neighbors")
    print("---------------------------------------------------------------------------")
    return

        # # Resnick's formula
        # print("\tB) Generating predictions using Resnick's Formula")
        # output_file_name = "pearson_sim_" + str(min_similarity_req) + "_min_results.csv"
        # rec.make_predictions(resnicks_prediction, output_file_name)
        # rmse_resnicks.append(overall_rmse)
        # time_resnicks.append(total_time)
        # coverage_resnicks.append(coverage)

def k_nearest(similarity_method, similarity_method_name, similarity_method_name_short):
    if similarity_method == rec.cosine_similarity:
        prediction_method = rec.resnicks_cosine_prediction
    else:
        prediction_method = rec.resnicks_pearson_prediction
    print("---------------------------------------------------------------------------")
    print("* Please be patient. Generating predictions can take a few minutes.\n")
    print("Generating predictions...")
    print("Neighborhoods created by:\tK-nearest users")
    print("Similarity metric used: \t", similarity_method_name, "\n")
    min_corated_items = 5
    k_vals = [5, 10, 20, 30, 40, 50, 60]
    rmse_all = []
    time_all = []
    coverage_all = []

    user_similarity, user_sim_mean, user_sim_stdev = rec.populate_user_similarity(similarity_method, min_corated_items, users)

    print("\nGenerating predictions across different top percents for purposes of comparison:")
    for k in k_vals:
        print(k, "closest users as neighbors")
        # Assign neighborhoods
        rec.assign_neighbors_k_nearest(users, user_similarity, k, similarity_method)
        output_file_name = "resnicks_"+similarity_method_name_short + str(k) + "_closest_results.csv"
        # Make predictions
        overall_rmse, total_time, coverage = rec.make_predictions(prediction_method, output_file_name, users, user_similarity, item_count, user_count)
        print("\tResults saved in:\t", output_file_name)
        rmse_all.append(overall_rmse)
        time_all.append(total_time)
        coverage_all.append(coverage)
    curve_label = "Resnick's Formula with "+similarity_method_name
    generate_graphs(k_vals, rmse_all, time_all, coverage_all, curve_label, "resnicks_"+similarity_method_name_short+"k_nearest_", "K Nearest Neighbors")
    print("---------------------------------------------------------------------------")

def top_percent(similarity_method, similarity_method_name, similarity_method_name_short):
    if similarity_method == rec.cosine_similarity:
        prediction_method = rec.resnicks_cosine_prediction
    else:
        prediction_method = rec.resnicks_pearson_prediction
    print("---------------------------------------------------------------------------")
    print("* Please be patient. Generating predictions can take a few minutes.\n")
    print("Generating predictions...")
    print("Neighborhoods created by:\tTop n percent of closest users")
    print("Similarity metric used: \t", similarity_method_name, "\n")
    min_corated_items = 5
    percent = [0.025, .05, .10, .15, .20, .25]
    rmse_all = []
    time_all = []
    coverage_all = []

    user_similarity, user_sim_mean, user_sim_stdev = rec.populate_user_similarity(similarity_method, min_corated_items, users)

    print("\nGenerating predictions across different top percents for purposes of comparison:")
    for p in percent:
        print("Top", p, "% of closest users as neighbors")
        # Assign neighborhoods
        rec.assign_neighbors_percent(users, user_similarity, p, similarity_method)
        output_file_name = "resnicks_"+similarity_method_name_short + str(p) + "_percent_results.csv"
        overall_rmse, total_time, coverage = rec.make_predictions(prediction_method, output_file_name, users, user_similarity, item_count, user_count)
        print("\tResults saved in:\t", output_file_name)
        rmse_all.append(overall_rmse)
        time_all.append(total_time)
        coverage_all.append(coverage)
    curve_label = "Resnick's Formula with "+similarity_method_name
    generate_graphs(percent, rmse_all, time_all, coverage_all, curve_label, "resnicks_"+similarity_method_name_short+"top_percent_", "Top N% of Neighbors")
    print("---------------------------------------------------------------------------")


if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("--a", action="store_true", dest="a", help="All of the below")
    parser.add_option("--kp", action="store_true", dest="kp", help="K-nearest neighborhoods based on Pearson's similarity")
    parser.add_option("--kc", action="store_true", dest="kc", help="K-nearest neighborhoods based on cosine similarity")
    parser.add_option("--pp", action="store_true", dest="pp", help="Top n percent neighborhoods based on Pearson's similarity")
    parser.add_option("--pc", action="store_true", dest="pc", help="Top n percent neighborhoods based on cosine similarity")
    parser.add_option("--tp", action="store_true", dest="tp", help="Minimum similarity threshold neighborhoods based on Pearson's similarity")
    parser.add_option("--tc", action="store_true", dest="tc", help="Minimum similarity threshold neighborhoods based on cosine similarity")

    (options, args) = parser.parse_args()
    if (len(sys.argv[1:]) == 0):
        parser.print_help()
        sys.exit()

    # Read in data
    users = {}
    item_ratings = {}
    ratings_count = 0
    item_ratings, users, ratings_count = rec.read_data()
    item_count = len(item_ratings)
    user_count = len(users)

    # Key statistics
    rec.general_stats(item_ratings, users, ratings_count)
    users = rec.user_stats(users)

    # Distance-based predictions
    if options.a:
        options.kp = True
        options.kc = True
        options.pp = True
        options.pc = True
        options.tp = True
        options.tc = True
        options.rp = True
        options.rc = True
    if options.kp:
        k_nearest(rec.pearson_similarity, "Pearson's similarity", "pearson_")
    if options.kc:
        k_nearest(rec.cosine_similarity, "Cosine similarity", "cosine_")
    if options.tp:
        similarity_threshold(rec.pearson_similarity, "Pearson's similarity", "pearson_")
    if options.tc:
        similarity_threshold(rec.cosine_similarity, "Cosine similarity", "cosine_")
    if options.pp:
        top_percent(rec.pearson_similarity, "Pearson's similarity", "pearson_")
    if options.pc:
        top_percent(rec.cosine_similarity, "Cosine similarity", "cosine_")
