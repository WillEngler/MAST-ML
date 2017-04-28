import matplotlib
import matplotlib.pyplot as plt
import data_parser
import numpy as np
from sklearn.kernel_ridge import KernelRidge
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
import data_analysis.printout_tools as ptools
import plot_data.plot_predicted_vs_measured as plotpm
import plot_data.plot_xy as plotxy
import portion_data.get_test_train_data as gttd
import os
import time
class Analysis():
    """Basic analysis class.
        Template for other classes.
        Combine many analysis classes to do meta-analysis
    """
    def __init__(self, 
        training_csv=None,
        testing_csv=None,
        model=None,
        train_index=None,
        test_index=None,
        input_features=None,
        target_feature=None,
        labeling_features=None,
        savepath=None,
        analysis_name=None,
        *args, **kwargs):
        """Initialize class.
            Attributes that can be set through keywords:
                self.training_csv=""
                self.testing_csv=""
                self.model=""
                self.train_index=""
                self.test_index=""
                self.input_features=""
                self.target_feature=""
                self.labeling_features=""
                self.savepath=""
                self.analysis_name=""
            Other attributes:
                self.resultspath=""
                self.training_dataset=""
                self.testing_dataset=""
                self.training_input_data_unfiltered=""
                self.training_target_data_unfiltered=""
                self.testing_input_data_unfiltered=""
                self.testing_target_data_unfiltered=""
                self.training_input_data=""
                self.training_target_data=""
                self.testing_input_data=""
                self.testing_target_data=""
                self.trained_model=""
                self.testing_target_prediction=""
                self.statistics=dict()
        """
        #Attribute initialization and checks
        #training csv
        if training_csv is None:
            raise ValueError("training_csv is not set")
        training_csv = os.path.abspath(training_csv)
        if not(os.path.isfile(training_csv)):
            raise OSError("No file found at %s" % training_csv)
        self.training_csv=training_csv
        #testing csv
        if testing_csv is None:
            raise ValueError("testing_csv is not set")
        testing_csv = os.path.abspath(testing_csv)
        if not(os.path.isfile(testing_csv)):
            raise OSError("No file found at %s" % testing_csv)
        self.testing_csv=testing_csv
        #model
        self.model=model
        #train/test index
        self.train_index=train_index
        self.test_index=test_index
        #features
        if input_features is None:
            raise ValueError("input_features is not set")
        self.input_features=input_features
        if target_feature is None:
            raise ValueError("target_feature is not set")
        self.target_feature=target_feature
        if labeling_features is None:
            self.labeling_features = list(self.input_features)
        else:
            self.labeling_features = labeling_features
        # paths
        if savepath is None:
            savepath = os.getcwd()
        savepath = os.path.abspath(savepath)
        self.savepath = savepath
        if analysis_name is None:
            self.analysis_name = "Results_%s" % time.strftime("%Y%m%d_%H%M%S")
        else:
            self.analysis_name = analysis_name
        #
        self.resultspath=os.path.join(self.savepath, self.analysis_name)
        if not os.path.isdir(self.resultspath):
            os.mkdir(self.resultspath)
        self.training_dataset=None
        self.testing_dataset=None
        self.training_input_data_unfiltered=None
        self.training_target_data_unfiltered=None
        self.testing_input_data_unfiltered=None
        self.testing_target_data_unfiltered=None
        self.training_input_data=None
        self.training_target_data=None
        self.testing_input_data=None
        self.testing_target_data=None
        self.trained_model=None
        self.testing_target_prediction=None
        self.statistics=dict()
        #
        self.do_analysis()
        return

    def do_analysis(self):
        self.get_datasets()
        self.get_unfiltered_data()
        self.get_train_test_indices()
        self.get_data()
        self.get_model()
        self.get_trained_model()
        self.get_prediction()
        self.get_statistics()
        self.print_statistics()
        self.print_output_csv()
        self.plot_results()
        return

    def get_datasets(self):
        """Get datasets. 
            Replace depending on configuration file modifications
        """
        self.training_dataset = data_parser.parse(self.training_csv)
        self.testing_dataset = data_parser.parse(self.testing_csv)
        return
    
    def get_unfiltered_data(self):
        """Replace with pandas dataframes
        """
        self.training_dataset.set_y_feature(self.target_feature)
        self.training_dataset.set_x_features(self.input_features)
        self.training_input_data_unfiltered = np.asarray(self.training_dataset.get_x_data())
        self.training_target_data_unfiltered = np.asarray(self.training_dataset.get_y_data()).ravel()
        hasy = self.testing_dataset.set_y_feature(self.target_feature)
        if hasy:
            self.testing_target_data_unfiltered = np.asarray(self.testing_dataset.get_y_data()).ravel()
        else:
            pass #keep self.testing_target_data as None
        self.testing_dataset.set_x_features(self.input_features)
        self.testing_input_data_unfiltered = np.asarray(self.testing_dataset.get_x_data())
        return
    
    def get_train_test_indices(self):
        if (self.train_index is None):
            train_obs = self.training_input_data_unfiltered.shape[0]
            self.train_index = np.arange(0, train_obs)
        if (self.test_index is None):
            test_obs = self.testing_input_data_unfiltered.shape[0]
            self.test_index = np.arange(0, test_obs)
        return

    def get_data(self):
        self.training_input_data = self.training_input_data_unfiltered[self.train_index]
        self.training_target_data = self.training_target_data_unfiltered[self.train_index]
        self.testing_input_data = self.testing_input_data_unfiltered[self.test_index]
        if not (self.testing_target_data_unfiltered is None):
            self.testing_target_data = self.testing_target_data_unfiltered[self.test_index]
        return


    def get_model(self):
        if (self.model is None):
            raise ValueError("No model.")
        return
    def get_trained_model(self):
        trained_model = self.model.fit(self.training_input_data, self.training_target_data)
        self.trained_model = trained_model
        return

    def get_prediction(self):
        self.testing_target_prediction = self.trained_model.predict(self.testing_input_data)
        return

    def get_rmse(self):
        rmse = np.sqrt(mean_squared_error(self.testing_target_data, self.testing_target_prediction))        
        return rmse
    
    def get_mean_error(self):
        pred_minus_true =self.testing_target_prediction-self.testing_target_data
        mean_error = np.mean(pred_minus_true)
        return mean_error

    def get_mean_absolute_error(self):
        mean_abs_err = mean_absolute_error(self.testing_target_data, self.testing_target_prediction)
        return mean_abs_err

    def get_rsquared(self):
        rsquared = r2_score(self.testing_target_data, self.testing_target_prediction)
        return rsquared

    def get_statistics(self):
        if self.testing_target_data is None:
            print("No testing target data. Statistics will not be collected.")
            return
        self.statistics['rmse'] = self.get_rmse()
        self.statistics['mean_error'] = self.get_mean_error()
        self.statistics['mean_absolute_error'] = self.get_mean_absolute_error()
        self.statistics['rsquared'] = self.get_rsquared()
        return

    def print_statistics(self):
        statname = os.path.join(self.resultspath, "statistics.txt")
        with open(statname, 'w') as statfile:
            statfile.write("Statistics\n")
            statfile.write("%s\n" % time.asctime())
            for skey, svalue in self.statistics.items():
                statfile.write("%s:%3.4f" % (skey, svalue))
        return

    def print_output_csv(self):
        """
            Modify once dataframe is in place
        """
        ocsvname = os.path.join(self.resultspath, "output_data.csv")
        headerline = ""
        printarray = ""
        print_features = self.labeling_features
        print_features.extend(self.input_features)
        if not (self.testing_target_data is None):
            print_features.extend(self.target_feature)
        for feature_name in print_features:
            headerline = headerline + feature_name + ","
            feature_vector = np.asarray(self.testing_dataset.get_data(feature_name)).ravel()[self.test_index]
            print("FEATURE:",feature_name)
            print("SHAPE:",feature_vector.shape)
            if printarray is None:
                printarray = feature_vector
            else:
                printarray = np.vstack((printarray, feature_vector))
        headerline = headerline + "Prediction"
        printarray = np.vstack((printarray, self.testing_target_prediction))
        printarray=printarray.transpose()
        ptools.mixed_array_to_csv(ocsvname, headerline, printarray)
        return

    def plot_results(self):
        if self.testing_target_data is None:
            print("No testing target data. Predicted vs. measured plot will not be plotted.")
            return
        plot_kwargs=dict()
        plot_kwargs['xlabel'] = "Measured"
        plot_kwargs['ylabel'] = "Predicted"
        plot_kwargs['guideline'] = 1
        notelist=list()
        notelist.append("RMSE: %3.3f" % self.statistics['rmse'])
        notelist.append("R-squared: %3.3f" % self.statistics['rsquared'])
        plot_kwargs['notelist'] = notelist
        plot_kwargs['savepath'] = os.path.join(self.resultspath)
        plotxy.single(self.testing_target_data,
                self.testing_target_prediction,
                **plot_kwargs)
        return

def execute(model="", data="", savepath=None, lwr_data="",
        training_csv=None,
        testing_csv=None,
        train_index=None,
        test_index=None,
        input_features=None,
        target_feature=None,
        labeling_features=None,
        analysis_name=None,
        *args, **kwargs):
    """Remove once alltests is updated
    """
    akwargs=dict()
    akwargs['training_csv'] = training_csv
    akwargs['testing_csv'] = testing_csv
    akwargs['model'] = model
    akwargs['train_index'] = train_index
    akwargs['test_index'] = test_index
    akwargs['input_features'] = list(input_features.split(",")) #LIST
    akwargs['target_feature'] = target_feature
    akwargs['labeling_features'] = labeling_features
    akwargs['savepath'] = savepath
    akwargs['analysis_name'] = analysis_name
    print(akwargs)
    mya = Analysis(**akwargs)
    return
        

