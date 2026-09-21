from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:,1]
    
    return {
        "Recall_Churn": recall_score(y_test, y_pred),
        "Precision_Churn": precision_score(y_test, y_pred),
        "F1_Churn": f1_score(y_test, y_pred),
        "ROC_AUC": roc_auc_score(y_test, y_prob)
    }


