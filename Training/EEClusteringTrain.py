from sklearn.cluster import KMeans
from kneed import KneeLocator
import os
from EElogging.EELogger import EELogger
from FileOperations.EEFileOperations import EEFileOperation


class EEClusteringTrain:
    """
    :Class Name: EEClusteringTrain
    :Description: This class is used to cluster the data so that models will be fine
                  tuned for each cluster and higher accuracy is obtained.

    Written By: Jobin Mathew
    Interning at iNeuron Intelligence
    Version: 1.0
    """

    def __init__(self):
        """
        :Method Name: __init__
        :Description: This method is Constructor for class EEFeatureSelectionTrain.
                      Initializes variables for logging
        """
        self.logger = EELogger()
        if not os.path.isdir("EElogging/training/"):
            os.mkdir("EElogging/training/")

        self.log_path = "EElogging/training/EEClusteringTrain.txt"

        self.file_op = EEFileOperation()

    def ee_obtain_optimum_cluster(self, dataframe):
        """
        :Method Name: ee_obtain_optimum_cluster
        :Description: This method calculates the optimum no. of cluster

        :param dataframe: The dataframe representing the data from the client after
                          all the preprocessing has been done
        :return: The optimum cluster value
        :On Failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')

            # within cluster sum of squares: For evaluating the knee point so that no. of clusters can be determined
            wcss = []

            for i in range(1, 11):
                # initializer is k-means++ so that there is some minimum distance between randomly initialized centroid.
                kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
                kmeans.fit(dataframe)
                wcss.append(kmeans.inertia_)

            # KneeLocator mathematically determines the knee point so that the task of selecting the optimum no of
            # cluster can automated.
            opt_cluster_val = KneeLocator(range(1, 11), wcss, curve="convex", direction='decreasing').knee

            message = f"The optimum cluster value obtained is {opt_cluster_val} with wcss={wcss[opt_cluster_val-1]}"
            self.logger.log(log_file, message)
            log_file.close()
            return opt_cluster_val

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was an ERROR while detecting optimum: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e

    def ee_create_cluster(self, dataframe, number_of_clusters):
        """
        :Method Name: ee_create_cluster
        :Description: This method performs the clustering in the dataset after preprocessing.

        :param dataframe: The pandas dataframe which has to be clustered.
        :param number_of_clusters: The number of clusters the data has to be clustered into.
        :return: Dataframe with clusters number added as a new column.
        :return: The sklearn Model used for clustering.
        :On Failure: Exception
        """
        try:
            log_file = open(self.log_path, 'a+')
            k_mean_model = KMeans(n_clusters=number_of_clusters, init='k-means++', random_state=42)

            # Adds a new column to the dataframe which identifies the cluster to which that data point belongs to.
            dataframe['cluster'] = k_mean_model.fit_predict(dataframe)

            message = "Clustering has been done, with cluster column added to dataset"
            self.logger.log(log_file, message)

            return k_mean_model, dataframe

        except Exception as e:
            log_file = open(self.log_path, 'a+')
            message = f"There was an ERROR while creating cluster: {str(e)}"
            self.logger.log(log_file, message)
            log_file.close()
            raise e




