import os
from pyspark.mllib.recommendation import ALS

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_counts_and_averages(ID_and_ratings_tuple):
    """Given a tuple (gameID, ratings_iterable)
    returns (gameID, (ratings_count, ratings_avg))
    """
    nratings = len(ID_and_ratings_tuple[1])
    return ID_and_ratings_tuple[0], (nratings, float(sum(x for x in ID_and_ratings_tuple[1])) / nratings)


class RecommendationEngine:
    """A game recommendation engine
    """

    def __count_and_average_ratings(self):
        """Updates the games ratings counts from
        the current data self.ratings_RDD
        """
        logger.info("Counting game ratings...")
        game_ID_with_ratings_RDD = self.ratings_RDD.map(lambda x: (x[1], x[2])).groupByKey()
        game_ID_with_avg_ratings_RDD = game_ID_with_ratings_RDD.map(get_counts_and_averages)
        self.game_rating_counts_RDD = game_ID_with_avg_ratings_RDD.map(lambda x: (x[0], x[1][0]))

    def __train_model(self):
        """Train the ALS model with the current dataset
        """
        logger.info("Training the ALS model...")
        self.model = ALS.train(self.ratings_RDD, self.rank, seed=self.seed,
                               iterations=self.iterations, lambda_=self.regularization_parameter)
        logger.info("ALS model built!")

    def __predict_ratings(self, user_and_game_RDD):
        """Gets predictions for a given (userID, gameID) formatted RDD
        Returns: an RDD with format (gameTitle, gameRating, numRatings)
        """
        predicted_RDD = self.model.predictAll(user_and_game_RDD)
        predicted_rating_RDD = predicted_RDD.map(lambda x: (x.product, x.rating))
        predicted_rating_title_and_count_RDD = \
            predicted_rating_RDD.join(self.game_rating_counts_RDD)
        predicted_rating_title_and_count_RDD = \
            predicted_rating_title_and_count_RDD.map(lambda r: (r[0], r[1][0], r[1][1]))

        return predicted_rating_title_and_count_RDD

    def add_ratings(self, ratings):
        """Add additional game ratings in the format (user_id, game_id, rating)
        """
        # Convert ratings to an RDD
        new_ratings_RDD = self.sc.parallelize(ratings)
        # Add new ratings to the existing ones
        self.ratings_RDD = self.ratings_RDD.union(new_ratings_RDD)
        # Re-compute game ratings count
        self.__count_and_average_ratings()
        # Re-train the ALS model with the new ratings
        self.__train_model()

        return ratings

    def get_ratings_for_game_ids(self, user_id, game_ids):
        """Given a user_id and a list of game_ids, predict ratings for them
        """
        requested_games_RDD = self.sc.parallelize(game_ids).map(lambda x: (user_id, x))
        # Get predicted ratings
        ratings = self.__predict_ratings(requested_games_RDD).collect()

        return ratings

    def get_top_ratings(self, user_id, games_count):
        """Recommends up to games_count top unrated games to user_id
        """
        # Get pairs of (userID, gameID) for user_id unrated games
        user_unrated_games_RDD = self.ratings_RDD.filter(lambda rating: not rating[0] == user_id) \
            .map(lambda x: (user_id, x[1])).distinct()
        # Get predicted ratings
        ratings = self.__predict_ratings(user_unrated_games_RDD).filter(lambda r: r[2] >= 25).takeOrdered(games_count,
                                                                                                           key=lambda
                                                                                                               x: -x[1])

        return ratings

    def __init__(self, sc, dataset_path):
        """Init the recommendation engine given a Spark context and a dataset path
        """

        logger.info("Starting up the Recommendation Engine: ")

        self.sc = sc

        # Load ratings data for later use
        logger.info("Loading Ratings data...")
        ratings_file_path = os.path.join(dataset_path, 'game_ratings.csv')
        ratings_raw_RDD = self.sc.textFile(ratings_file_path)
        self.ratings_RDD = ratings_raw_RDD.map(lambda line: line.split(","))\
                                          .map(lambda tokens: (int(tokens[0]), int(tokens[1]), float(tokens[2])))\
                                          .cache()
        # Pre-calculate games ratings counts
        self.__count_and_average_ratings()

        # Train the model
        self.rank = 8
        self.seed = 5L
        self.iterations = 3
        self.regularization_parameter = 0.1
        self.__train_model()
