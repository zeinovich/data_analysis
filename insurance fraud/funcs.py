# PLOT METRICS
from sklearn.metrics import roc_curve, precision_recall_curve, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from tensorflow import keras
import datetime
import pickle 

def plot_metrics(y_pred: np.array, y_test: np.array, threshold_proba=0.5) -> None:
    '''Plots the confusion matrix, ROC curve and the precision-recall curve.
    
        ### Parameters:
            y_pred: The predicted values (proba)
            y_test: The true values
        ### Returns: 
            None'''

    y_pred_hard = y_pred > threshold_proba
    print(classification_report(y_test, y_pred_hard))
    cm = confusion_matrix(y_test, y_pred_hard)
    sns.heatmap(cm, annot=True, fmt='d', cmap='coolwarm', cbar=True)
    plt.show()

    fpr, tpr, thresholds = roc_curve(y_test, y_pred)
    line_threshold = [thresholds for thresholds in thresholds if thresholds >= threshold_proba][-1]
    idx = np.argwhere(thresholds == line_threshold)[0][0]
    plt.plot(fpr, tpr, linewidth=2, label=None)
    plt.plot(fpr[idx], tpr[idx], "rx")
    plt.plot([0, 1], [0, 1], 'k--')
    plt.axis([0, 1, 0, 1])
    plt.xlabel('False Positive Rate', fontsize=16)
    plt.ylabel('True Positive Rate', fontsize=16)
    plt.show()

    precision, recall, thresholds = precision_recall_curve(y_test, y_pred)
    line_threshold = [thresholds for thresholds in thresholds if thresholds >= threshold_proba][0]
    idx = np.argwhere(thresholds == line_threshold)[0][0]
    plt.plot(recall, precision, linewidth=2, label=None)
    plt.plot(recall[idx], precision[idx], "rx")
    plt.axis([0, 1, 0, 1])
    plt.xlabel('Recall', fontsize=10)
    plt.ylabel('Precision', fontsize=10)
    plt.show()

    

    def plot_aux_lines():
        plt.plot([line_threshold, line_threshold], [0., precision[idx]], "r:")
        plt.plot([line_threshold, line_threshold], [0., recall[idx]], "r:")
        plt.plot([0.0, line_threshold], [recall[idx], recall[idx]], "r:")

        plt.plot([line_threshold], [recall[idx]], "gx")
        plt.plot([line_threshold], [precision[idx]], "bx")
        
        plt.text(line_threshold + 0.03, precision[idx], f'{precision[idx]:.2f}', fontsize=10, color="b")
        plt.text(line_threshold + 0.03, recall[idx], f'{recall[idx]:.2f}', fontsize=10, color="g")
    
    plt.plot(thresholds, precision[:-1], "b-", label="Precision")
    plt.plot(thresholds, recall[:-1], "g-", label="Recall")

    plot_aux_lines()
    
    plt.xlabel("Threshold", fontsize=10)
    plt.legend(loc="upper right", fontsize=10)
    plt.ylim([0, 1])
    plt.xlim([0, 1])
    plt.show()

def get_tb_callback():
    '''Returns a TensorBoard callback.'''
    logdir = "logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    return keras.callbacks.TensorBoard(log_dir=logdir)

METRICS = [
    keras.metrics.Recall(name='recall'),
        keras.metrics.Precision(name='precision'),
        keras.metrics.AUC(name='auc')]

def dump_model(model, name):
    '''Dumps the model to a file.'''
    with open(f'{name}_{datetime.date.today()}', 'wb') as f:
        pickle.dump(model, f)
