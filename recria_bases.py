def main():
    from webapp_social_media import db
    from webapp_social_media.models import User, Post, InterestTopic, InterestTopicUser

    topics = ["Algorithm", "AngularJS", "Artificial Intelligence", "Backpropagation", "Bayes' Theorem", "Bayesian Network", "Bias", "Big Data", "Binomial Distribution", "Chi-Square Test", "Classification", "Clustering", "Coefficient", "Computational Linguistics", "Confidence Interval", "Continuous Variable", "Correlation", "Covariance", "Cross-Validation", "D3", "Data Engineer", "Data Mining", "Data Science", "Data Structure", "Data Wrangling", "Decision Trees", "Deep Learning", "Dependent Variable", "Dimension Reduction", "Discrete Variable", "Econometrics", "Feature", "Feature Engineering", "GATE", "Gradient Boosting", "Gradient Descent", "Histogram", "Independent Variable", "JavaScript", "K-means Clustering", "k-nearest Neighbors", "Latent Variable", "Lift", "linear Algebra", "Linear Regression", "Logarithm", "Logistic Regression", "Machine Learning", "Machine Learning Model", "Markov Chain", "MATLAB", "Matrix", "Mean", "Mean Absolute Error", "Mean Squared Error",
              "Median", "Mode", "Model", "Monte Carlo Method", "Moving Average", "N-Gram", "Naive Bayes Classifier", "Neural Network", "Normal Distribution", "NoSQL", "Null Hypothesis", "Objective Function", "Outlier", "Overfitting", "P Value", "PageRank", "Pandas", "Perceptron", "Perl", "Pivot Table", "Poisson Distribution", "Posterior Distribution", "Predictive Analytics", "Predictive Modeling", "Principal Component Analysis", "Pior Distribution", "Python", "Quantile, quartile", "R", "Random Forest", "Regression", "Reinforcement Learning", "Root Mean Squared Error", "Ruby", "S curve", "SAS", "Scalar", "Scripting", "Serial Correlation", "Shell", "Spatiotemporal Data", "SPSS", "SQL", "Standard Deviation", "Standard Normal Distribution", "Standardized Score", "Stata", "Strata, Stratified Sampling", "Supervised Learning", "Support Vector Machine", "T-Distribution", "Tableau", "Time Series Data", "UIMA", "Unsupervised Learning", "Variance", "Vector", "Vector Space", "Weka"]

    db.drop_all()
    db.create_all()

    for x in topics:
        topic = InterestTopic(label=x)
        db.session.add(topic)
    db.session.commit()


if __name__ == '__main__':
    main()
