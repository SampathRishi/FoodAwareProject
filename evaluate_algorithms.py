import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

def evaluate_algorithm_performance():
    """
    Evaluates and compares the performance of different recommendation algorithms
    using precision, recall, and F1 score metrics.
    """
    # Connect to database
    conn = sqlite3.connect('database/database.db')
    
    # Load data
    orders_df = pd.read_sql_query("SELECT * FROM orders", conn)
    users_df = pd.read_sql_query("SELECT * FROM users", conn)
    food_items_df = pd.read_sql_query("SELECT * FROM food_items", conn)
    conn.close()
    
    print(f"Loaded {len(orders_df)} orders for evaluation")
    
    # Split data into training and testing sets (80/20)
    # We'll use older orders for training and more recent ones for testing
    orders_df['timestamp'] = pd.to_datetime(orders_df['timestamp'])
    orders_df = orders_df.sort_values('timestamp')
    
    train_size = int(len(orders_df) * 0.8)
    train_df = orders_df.iloc[:train_size]
    test_df = orders_df.iloc[train_size:]
    
    print(f"Training on {len(train_df)} orders, testing on {len(test_df)} orders")
    
    # Dictionary to store results
    results = {
        'algorithm': [],
        'precision': [],
        'recall': [],
        'f1_score': []
    }
    
    # Function to evaluate a single recommendation algorithm
    def evaluate_algorithm(name, recommendation_func, **kwargs):
        print(f"Evaluating {name}...")
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        
        # For each user in the test set
        for user_id in test_df['user_id'].unique():
            # Get actual food items ordered by this user in test set
            user_test_orders = test_df[test_df['user_id'] == user_id]
            actual_items = set(user_test_orders['food_id'].tolist())
            
            if len(actual_items) == 0:
                continue
                
            # Get contextual factors (use most recent for testing)
            recent_order = user_test_orders.iloc[-1]
            weather = recent_order['weather']
            mood = recent_order['mood']
            
            # Generate recommendations
            try:
                recommendations = recommendation_func(user_id, weather, mood, **kwargs)
                
                # Handle different return formats
                if isinstance(recommendations, pd.DataFrame):
                    recommended_items = set(recommendations['food_id'].tolist())
                elif isinstance(recommendations, list):
                    if len(recommendations) > 0 and isinstance(recommendations[0], tuple):
                        recommended_items = set([item[0] for item in recommendations])
                    elif len(recommendations) > 0 and isinstance(recommendations[0], dict):
                        recommended_items = set([item['food_id'] for item in recommendations])
                    else:
                        recommended_items = set(recommendations)
                else:
                    recommended_items = set()
                
                # Calculate metrics
                true_positives += len(actual_items.intersection(recommended_items))
                false_positives += len(recommended_items - actual_items)
                false_negatives += len(actual_items - recommended_items)
                
            except Exception as e:
                print(f"Error evaluating {name} for user {user_id}: {e}")
                continue
        
        # Calculate precision, recall, F1
        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        # Store results
        results['algorithm'].append(name)
        results['precision'].append(round(precision, 2))
        results['recall'].append(round(recall, 2))
        results['f1_score'].append(round(f1, 2))
        
        print(f"{name} - Precision: {precision:.2f}, Recall: {recall:.2f}, F1: {f1:.2f}")
        return precision, recall, f1
    
    # Create a function to simulate training on the training set
    # In a real scenario, you would train your models on the training set
    def train_models():
        global train_data
        train_data = train_df
        print("Models trained on training data")
    
    # Train models
    train_models()
    
    # Import our recommendation functions
    from models.collaborative_filtering import recommend_foods as cf_recommend
    from models.content_based_filtering import recommend_content_based as cb_recommend
    from models.context_aware_filtering import recommend_context_aware as ca_recommend
    from models.hybrid_recommendation import hybrid_recommendation
    
    # Evaluate each algorithm (with appropriate parameters)
    evaluate_algorithm('Collaborative Filtering', cf_recommend, n=10)
    evaluate_algorithm('Content-Based', cb_recommend, n=10)
    evaluate_algorithm('Context-Aware', ca_recommend, n=10)
    evaluate_algorithm('Hybrid Approach', hybrid_recommendation, n=10)
    
    # Create results DataFrame
    results_df = pd.DataFrame(results)
    
    # Plot results
    plt.figure(figsize=(12, 6))
    
    # Set color palette
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    
    # Create grouped bar chart
    x = np.arange(len(results_df['algorithm']))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Plot bars
    ax.bar(x - width, results_df['f1_score'], width, label='F1 Score', color=colors[0])
    ax.bar(x, results_df['precision'], width, label='Precision', color=colors[1])
    ax.bar(x + width, results_df['recall'], width, label='Recall', color=colors[2])
    
    # Customize chart
    ax.set_title('Recommendation Algorithm Performance Comparison', fontsize=18)
    ax.set_xlabel('Algorithm', fontsize=14)
    ax.set_ylabel('Score', fontsize=14)
    ax.set_xticks(x)
    ax.set_xticklabels(results_df['algorithm'], fontsize=12)
    ax.set_ylim(0, 1.0)
    ax.legend(fontsize=12)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Add value labels on top of bars
    for i, v in enumerate(results_df['f1_score']):
        ax.text(i - width, v + 0.02, f'{v:.2f}', ha='center', fontsize=11)
    
    for i, v in enumerate(results_df['precision']):
        ax.text(i, v + 0.02, f'{v:.2f}', ha='center', fontsize=11)
    
    for i, v in enumerate(results_df['recall']):
        ax.text(i + width, v + 0.02, f'{v:.2f}', ha='center', fontsize=11)
    
    plt.tight_layout()
    
    # Save figure
    plt.savefig('algorithm_performance.png', dpi=300, bbox_inches='tight')
    
    # Show figure
    plt.show()
    
    return results_df

# Execute the evaluation
if __name__ == "__main__":
    results = evaluate_algorithm_performance()
    print("\nFinal Results:")
    print(results)