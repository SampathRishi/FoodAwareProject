import pandas as pd
import sqlite3
from models.hybrid_recommendation import hybrid_recommendation
from sklearn.metrics import precision_score, recall_score, f1_score, average_precision_score

# Database Connection
conn = sqlite3.connect('../database/database.db')
orders_df = pd.read_sql_query("SELECT * FROM orders", conn)
conn.close()

# Configurations
TOP_N = 5

# Ground Truth and Prediction Collector
ground_truth = []
predictions = []

# Evaluate for each user
unique_users = orders_df['user_id'].unique()

print("Evaluating recommendations...")

for user_id in unique_users:
    # Fetch user history
    user_orders = orders_df[orders_df['user_id'] == user_id]
    true_items = user_orders['food_id'].tolist()
    ground_truth.append(true_items)

    # Generate recommendations
    # Using a default mood and weather for simplicity
    recommended_items = hybrid_recommendation(user_id, weather="Sunny", mood="Happy", n=TOP_N)
    predicted_items = [item['food_id'] for item in recommended_items]
    predictions.append(predicted_items)

# Metrics Calculation
def precision_at_k(true_list, pred_list, k=TOP_N):
    pred_set = set(pred_list[:k])
    true_set = set(true_list)
    return len(pred_set & true_set) / float(k)

def recall_at_k(true_list, pred_list, k=TOP_N):
    pred_set = set(pred_list[:k])
    true_set = set(true_list)
    return len(pred_set & true_set) / float(len(true_list)) if len(true_list) > 0 else 0

# Compute Average Scores
precision_scores = [precision_at_k(t, p) for t, p in zip(ground_truth, predictions)]
recall_scores = [recall_at_k(t, p) for t, p in zip(ground_truth, predictions)]

avg_precision = sum(precision_scores) / len(precision_scores)
avg_recall = sum(recall_scores) / len(recall_scores)
f1 = (2 * avg_precision * avg_recall) / (avg_precision + avg_recall) if (avg_precision + avg_recall) > 0 else 0

# Display the Results
print("\nModel Evaluation Results:")
print(f"Precision@{TOP_N}: {avg_precision:.4f}")
print(f"Recall@{TOP_N}: {avg_recall:.4f}")
print(f"F1-Score: {f1:.4f}")
