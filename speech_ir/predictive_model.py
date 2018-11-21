from sklearn import linear_model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score

from speech_ir.visualizer import read_input_folder


def predictive_logistic_model(train_folder, test_folder):
    train_data = read_input_folder(train_folder)
    train_label = []
    for i in range(len(train_data)):
        train_label.append(1)

    test_data = read_input_folder("2016_test")
    test_label = []
    for i in range(len(test_data)):
        test_label.append(1)

    vec = TfidfVectorizer()
    train_matrix = vec.fit_transform(train_data)
    test_matrix = vec.transform(test_data)
    test_matrix

    logistic_regression_model = linear_model.LogisticRegression()
    logistic_regression_model.fit(train_matrix, train_label)
    prediction_result = logistic_regression_model.predict(test_matrix)

    confidence = logistic_regression_model.predict_proba(test_matrix)
    print("Confidence = " + str(confidence))

    accuracy = accuracy_score(prediction_result, test_label)
    print("Accuracy = " + str(confidence))
