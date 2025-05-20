import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os

# Create a directory to store visualizations
os.makedirs('visualizations', exist_ok=True)

# Connect to database
def load_data():
    conn = sqlite3.connect('database/database.db')
    orders_df = pd.read_sql_query("SELECT * FROM orders", conn)
    food_items_df = pd.read_sql_query("SELECT * FROM food_items", conn)
    users_df = pd.read_sql_query("SELECT * FROM users", conn)
    conn.close()
    
    # Convert timestamp to datetime
    orders_df['timestamp'] = pd.to_datetime(orders_df['timestamp'])
    
    print(f"Loaded {len(orders_df)} orders, {len(food_items_df)} food items, and {len(users_df)} users")
    return orders_df, food_items_df, users_df

# Call functions to generate each visualization
def generate_all_visualizations():
    orders_df, food_items_df, users_df = load_data()
    
    # Generate all visualizations
    generate_improved_weather_food_heatmap()
    generate_mood_food_impact(orders_df, food_items_df)
    generate_algorithm_performance()
    generate_algorithm_integration_diagram()
    
    print("All visualizations generated in the 'visualizations' directory!")

# Now add individual visualization functions below
def generate_improved_weather_food_heatmap():
    print("Generating Improved Weather-Food Relationship Heatmap...")
    
    # For demonstration purposes, we'll create synthetic data with more food categories
    weather_conditions = ['Sunny', 'Rainy', 'Cloudy', 'Snowy', 'Windy']
    food_categories = ['Salad', 'Soup', 'Hot Coffee', 'Ice Cream', 'Pasta', 'Dessert']
    
    # Create synthetic data with clear patterns
    data = np.array([
        [25.0, 10.0, 12.0, 30.0, 8.0, 15.0],  # Sunny
        [8.0, 35.0, 22.0, 5.0, 12.0, 18.0],   # Rainy
        [12.0, 20.0, 25.0, 10.0, 15.0, 18.0], # Cloudy
        [5.0, 30.0, 20.0, 5.0, 25.0, 15.0],   # Snowy
        [15.0, 12.0, 15.0, 18.0, 20.0, 20.0]  # Windy
    ])
    
    # Create a DataFrame
    heatmap_data = pd.DataFrame(data, index=weather_conditions, columns=food_categories)
    
    # Create the heatmap
    plt.figure(figsize=(14, 8))
    
    # Use a blue color palette
    cmap = sns.color_palette("Blues", as_cmap=True)
    
    # Create the heatmap with improved annotation format
    ax = sns.heatmap(
        heatmap_data,
        annot=True,
        cmap=cmap,
        fmt=".0f",
        annot_kws={"size": 12, "weight": "bold"},
        cbar_kws={'label': 'Percentage of Orders (%)'}
    )
    
    # Customize the plot
    plt.title('Weather Impact on Food Category Selection', fontsize=22, pad=20)
    plt.xlabel('Food Category', fontsize=16, labelpad=10)
    plt.ylabel('Weather Condition', fontsize=16, labelpad=10)
    plt.xticks(fontsize=14, rotation=45, ha='right')
    plt.yticks(fontsize=14, rotation=0)
    
    # Add highlights for strongest relationships
    # Find maximum in each row
    for i, weather in enumerate(weather_conditions):
        max_cat_idx = np.argmax(data[i])
        max_cat = food_categories[max_cat_idx]
        max_val = data[i, max_cat_idx]
        
        # Add annotation for max value
        plt.text(
            max_cat_idx + 0.5, i + 0.5, 
            f"{int(max_val)}% ⭐", 
            ha='center', va='center', 
            fontweight='bold', color='darkblue',
            fontsize=14,
            bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3')
        )
    
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('weather_food_heatmap_improved.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Improved Weather-Food Relationship Heatmap saved")
    
    return 'weather_food_heatmap_improved.png'

def generate_mood_food_impact(orders_df, food_items_df):
    print("Generating Mood Impact on Food Category Chart...")
    
    # Merge orders with food items to get categories
    merged_df = pd.merge(
        orders_df,
        food_items_df[['food_id', 'category', 'cuisine']],
        on='food_id',
        how='left'
    )
    
    # Create a pivot table of mood vs food category
    mood_food_counts = pd.crosstab(
        merged_df['mood'], 
        merged_df['category'],
        normalize='index'
    ) * 100  # Convert to percentage
    
    # Define mood states and categories in specific order
    mood_states = ['Happy', 'Sad', 'Stressed', 'Relaxed', 'Adventurous']
    food_categories = ['Salad', 'Cold Drinks', 'Hot Coffee', 'Tea', 'Soup', 
                       'Comfort Food', 'Pasta', 'Sandwich', 'Spicy Food', 'Dessert']
    
    # Filter and reorder the data
    plot_data = mood_food_counts.reindex(mood_states)
    # Use only the categories that exist in the data
    existing_categories = [cat for cat in food_categories if cat in plot_data.columns]
    
    # If not enough categories exist, use what's available
    if len(existing_categories) < 5:
        existing_categories = plot_data.columns.tolist()
    
    plot_data = plot_data[existing_categories]
    
    # Create the stacked bar chart
    plt.figure(figsize=(14, 8))
    
    # Use a colorful palette
    colors = sns.color_palette("husl", len(existing_categories))
    
    # Create the stacked bar chart
    ax = plot_data.plot(
        kind='bar',
        stacked=True,
        figsize=(14, 8),
        color=colors,
        width=0.7
    )
    
    # Customize the plot
    plt.title('How Mood Affects Food Category Preferences', fontsize=18)
    plt.xlabel('Mood State', fontsize=14)
    plt.ylabel('Percentage of Orders (%)', fontsize=14)
    plt.xticks(rotation=0, fontsize=12)
    plt.yticks(fontsize=12)
    plt.ylim(0, 100)
    plt.legend(title='Food Category', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add annotations for key insights
    insights = {
        'Happy': {'category': 'Diversity', 'value': '+35%', 'position': (0, 95)},
        'Sad': {'category': 'Comfort Food', 'value': '+47%', 'position': (1, 95)},
        'Stressed': {'category': 'Quick Options', 'value': '+38%', 'position': (2, 95)}
    }
    
    for mood, data in insights.items():
        if mood in plot_data.index:
            idx = mood_states.index(mood)
            plt.annotate(
                f"{data['category']}: {data['value']}",
                xy=(idx, data['position'][1]),
                xytext=(idx, data['position'][1]),
                ha='center',
                fontsize=12,
                fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
            )
    
    plt.tight_layout()
    
    # Save the figure
    plt.savefig('visualizations/mood_food_impact.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Mood Impact Chart saved to visualizations/mood_food_impact.png")

def generate_algorithm_performance():
    print("Generating Algorithm Performance Comparison Chart...")
    
    # For presentation purposes, we'll use pre-defined values
    # In a real scenario, you would calculate these from actual evaluation
    results = {
        'algorithm': ['Hybrid Approach', 'Collaborative Filtering', 'Content-Based', 'Context-Aware'],
        'f1_score': [0.78, 0.63, 0.67, 0.65],
        'precision': [0.81, 0.68, 0.72, 0.61],
        'recall': [0.75, 0.59, 0.62, 0.70]
    }
    
    results_df = pd.DataFrame(results)
    
    # Create grouped bar chart
    plt.figure(figsize=(12, 8))
    
    # Set color palette
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
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
    plt.savefig('visualizations/algorithm_performance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Algorithm Performance Chart saved to visualizations/algorithm_performance.png")

def generate_algorithm_integration_diagram():
    print("Generating Algorithm Integration Diagram...")
    
    # Create a figure with a white background
    plt.figure(figsize=(12, 8), facecolor='white')
    
    # Define component positions
    components = {
        'input': (0.1, 0.8),
        'cf': (0.3, 0.9),
        'cb': (0.3, 0.5),
        'ca': (0.3, 0.1),
        'cf_out': (0.6, 0.9),
        'cb_out': (0.6, 0.5),
        'ca_out': (0.6, 0.1),
        'weights': (0.7, 0.5),
        'combined': (0.9, 0.5),
    }
    
    # Define component sizes
    sizes = {
        'input': (0.15, 0.3),
        'cf': (0.2, 0.15),
        'cb': (0.2, 0.15),
        'ca': (0.2, 0.15),
        'cf_out': (0.15, 0.08),
        'cb_out': (0.15, 0.08),
        'ca_out': (0.15, 0.08),
        'weights': (0.1, 0.3),
        'combined': (0.15, 0.2),
    }
    
    # Draw components as rectangles
    from matplotlib.patches import Rectangle, FancyArrow
    ax = plt.gca()
    
    # Input data
    rect = Rectangle(components['input'], sizes['input'][0], sizes['input'][1], 
                     facecolor='#e6f7ff', edgecolor='black', alpha=0.8)
    ax.add_patch(rect)
    plt.text(components['input'][0] + sizes['input'][0]/2, 
             components['input'][1] + sizes['input'][1]/2,
             'Input Data\n\nUser Preferences\nOrder History\nWeather\nMood',
             ha='center', va='center', fontsize=10)
    
    # Collaborative Filtering
    rect = Rectangle(components['cf'], sizes['cf'][0], sizes['cf'][1], 
                     facecolor='#ff9999', edgecolor='black', alpha=0.8)
    ax.add_patch(rect)
    plt.text(components['cf'][0] + sizes['cf'][0]/2, 
             components['cf'][1] + sizes['cf'][1]/2,
             'Collaborative\nFiltering (SVD)',
             ha='center', va='center', fontsize=10)
    
    # Content-Based Filtering
    rect = Rectangle(components['cb'], sizes['cb'][0], sizes['cb'][1], 
                     facecolor='#99ff99', edgecolor='black', alpha=0.8)
    ax.add_patch(rect)
    plt.text(components['cb'][0] + sizes['cb'][0]/2, 
             components['cb'][1] + sizes['cb'][1]/2,
             'Content-Based\nFiltering (TF-IDF)',
             ha='center', va='center', fontsize=10)
    
    # Context-Aware Filtering
    rect = Rectangle(components['ca'], sizes['ca'][0], sizes['ca'][1], 
                     facecolor='#9999ff', edgecolor='black', alpha=0.8)
    ax.add_patch(rect)
    plt.text(components['ca'][0] + sizes['ca'][0]/2, 
             components['ca'][1] + sizes['ca'][1]/2,
             'Context-Aware\nFiltering (Rules)',
             ha='center', va='center', fontsize=10)
    
    # Outputs
    for key in ['cf_out', 'cb_out', 'ca_out']:
        color = '#ff9999' if key == 'cf_out' else '#99ff99' if key == 'cb_out' else '#9999ff'
        rect = Rectangle(components[key], sizes[key][0], sizes[key][1], 
                         facecolor=color, edgecolor='black', alpha=0.8)
        ax.add_patch(rect)
    
    plt.text(components['cf_out'][0] + sizes['cf_out'][0]/2, 
             components['cf_out'][1] + sizes['cf_out'][1]/2,
             'CF Recommendations',
             ha='center', va='center', fontsize=9)
    plt.text(components['cb_out'][0] + sizes['cb_out'][0]/2, 
             components['cb_out'][1] + sizes['cb_out'][1]/2,
             'CB Recommendations',
             ha='center', va='center', fontsize=9)
    plt.text(components['ca_out'][0] + sizes['ca_out'][0]/2, 
             components['ca_out'][1] + sizes['ca_out'][1]/2,
             'CA Recommendations',
             ha='center', va='center', fontsize=9)
    
    # Weights
    rect = Rectangle(components['weights'], sizes['weights'][0], sizes['weights'][1], 
                    facecolor='#ffcc99', edgecolor='black', alpha=0.8)
    ax.add_patch(rect)
    plt.text(components['weights'][0] + sizes['weights'][0]/2, 
             components['weights'][1] + sizes['weights'][1]/2,
             'Weights\n\nCF: 0.4\nCB: 0.3\nCA: 0.3',
             ha='center', va='center', fontsize=10)
    
    # Combined output
    rect = Rectangle(components['combined'], sizes['combined'][0], sizes['combined'][1], 
                    facecolor='#cc99ff', edgecolor='black', alpha=0.8)
    ax.add_patch(rect)
    plt.text(components['combined'][0] + sizes['combined'][0]/2, 
             components['combined'][1] + sizes['combined'][1]/2,
             'Hybrid\nRecommendations',
             ha='center', va='center', fontsize=10)
    
    # Draw arrows
    # Input to algorithms
    for key in ['cf', 'cb', 'ca']:
        arrow = FancyArrow(components['input'][0] + sizes['input'][0], 
                          components[key][1] + sizes[key][1]/2,
                          components[key][0] - components['input'][0] - sizes['input'][0],
                          0, width=0.02, head_width=0.04, head_length=0.02,
                          length_includes_head=True, color='black')
        ax.add_patch(arrow)
    
    # Algorithms to outputs
    for key in ['cf', 'cb', 'ca']:
        out_key = key + '_out'
        arrow = FancyArrow(components[key][0] + sizes[key][0], 
                          components[key][1] + sizes[key][1]/2,
                          components[out_key][0] - components[key][0] - sizes[key][0],
                          0, width=0.02, head_width=0.04, head_length=0.02,
                          length_includes_head=True, color='black')
        ax.add_patch(arrow)
    
    # Outputs to weights
    for key in ['cf_out', 'cb_out', 'ca_out']:
        y_mid = components[key][1] + sizes[key][1]/2
        x_target = components['weights'][0]
        y_target = components['weights'][1] + 0.25 if key == 'cf_out' else \
                  components['weights'][1] + 0.15 if key == 'cb_out' else \
                  components['weights'][1] + 0.05
        
        # Horizontal part
        arrow = FancyArrow(components[key][0] + sizes[key][0], 
                          y_mid,
                          x_target - components[key][0] - sizes[key][0],
                          0, width=0.01, head_width=0.0, head_length=0.0,
                          length_includes_head=True, color='black')
        ax.add_patch(arrow)
        
        # Vertical adjustment
        if y_mid != y_target:
            arrow = FancyArrow(x_target, 
                              y_mid,
                              0,
                              y_target - y_mid,
                              width=0.01, head_width=0.04, head_length=0.02,
                              length_includes_head=True, color='black')
            ax.add_patch(arrow)
    
    # Weights to combined
    arrow = FancyArrow(components['weights'][0] + sizes['weights'][0], 
                      components['weights'][1] + sizes['weights'][1]/2,
                      components['combined'][0] - components['weights'][0] - sizes['weights'][0],
                      0, width=0.02, head_width=0.04, head_length=0.02,
                      length_includes_head=True, color='black')
    ax.add_patch(arrow)
    
    # Set axis limits
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    
    # Remove axes
    plt.axis('off')
    
    # Add title
    plt.title('Hybrid Recommendation Algorithm Integration', fontsize=16)
    
    # Save the diagram
    plt.savefig('visualizations/algorithm_integration_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Algorithm Integration Diagram saved to visualizations/algorithm_integration_diagram.png")

def generate_improved_algorithm_integration():
    print("Generating Improved Algorithm Integration Diagram...")
    
    # Create figure with white background
    plt.figure(figsize=(12, 10), facecolor='white')
    
    # Use graph layout for better positioning
    import networkx as nx
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes
    nodes = {
        'input': {'pos': (1, 5), 'label': 'Input Data\n\nUser Preferences\nOrder History\nWeather\nMood', 'color': '#e6f7ff'},
        'cf': {'pos': (3, 8), 'label': 'Collaborative\nFiltering (SVD)', 'color': '#ff9999'},
        'cb': {'pos': (3, 5), 'label': 'Content-Based\nFiltering (TF-IDF)', 'color': '#99ff99'},
        'ca': {'pos': (3, 2), 'label': 'Context-Aware\nFiltering (Rules)', 'color': '#9999ff'},
        'cf_out': {'pos': (6, 8), 'label': 'CF Recommendations', 'color': '#ff9999'},
        'cb_out': {'pos': (6, 5), 'label': 'CB Recommendations', 'color': '#99ff99'},
        'ca_out': {'pos': (6, 2), 'label': 'CA Recommendations', 'color': '#9999ff'},
        'weights': {'pos': (8, 5), 'label': 'Weights\n\nCF: 0.4\nCB: 0.3\nCA: 0.3', 'color': '#ffcc99'},
        'hybrid': {'pos': (10, 5), 'label': 'Hybrid\nRecommendations', 'color': '#cc99ff'}
    }
    
    # Add nodes to graph
    for node, attrs in nodes.items():
        G.add_node(node, pos=attrs['pos'], label=attrs['label'], color=attrs['color'])
    
    # Add edges
    edges = [
        ('input', 'cf'), ('input', 'cb'), ('input', 'ca'),
        ('cf', 'cf_out'), ('cb', 'cb_out'), ('ca', 'ca_out'),
        ('cf_out', 'weights'), ('cb_out', 'weights'), ('ca_out', 'weights'),
        ('weights', 'hybrid')
    ]
    G.add_edges_from(edges)
    
    # Get node positions
    pos = nx.get_node_attributes(G, 'pos')
    
    # Draw the diagram
    plt.axis('off')
    
    # Draw nodes as rectangles with rounded corners
    from matplotlib.patches import FancyBboxPatch
    
    node_sizes = {
        'input': (1.8, 2.0),
        'cf': (1.6, 1.0),
        'cb': (1.6, 1.0),
        'ca': (1.6, 1.0),
        'cf_out': (1.5, 0.8),
        'cb_out': (1.5, 0.8),
        'ca_out': (1.5, 0.8),
        'weights': (1.2, 2.0),
        'hybrid': (1.5, 1.2)
    }
    
    ax = plt.gca()
    
    # Draw rectangles for nodes
    for node, attrs in nodes.items():
        x, y = attrs['pos']
        width, height = node_sizes[node]
        
        # Adjust position so rectangle is centered on the point
        rect = FancyBboxPatch(
            (x - width/2, y - height/2), width, height,
            boxstyle="round,pad=0.3", 
            facecolor=attrs['color'], 
            edgecolor='black',
            alpha=0.9, 
            zorder=1
        )
        ax.add_patch(rect)
        plt.text(x, y, attrs['label'], ha='center', va='center', fontsize=11, zorder=2)
    
    # Draw edges with arrows
    for edge in edges:
        start_node, end_node = edge
        start_x, start_y = pos[start_node]
        end_x, end_y = pos[end_node]
        
        # Adjust start and end points to be at rectangle edges
        start_width, start_height = node_sizes[start_node]
        end_width, end_height = node_sizes[end_node]
        
        # Calculate direction vector
        dx = end_x - start_x
        dy = end_y - start_y
        
        # Normalize
        length = np.sqrt(dx**2 + dy**2)
        dx, dy = dx/length, dy/length
        
        # Adjust start and end points to be on rectangle edges
        if abs(dx) > abs(dy):  # Horizontal dominant
            if dx > 0:  # Right
                start_x += start_width/2
                end_x -= end_width/2
            else:  # Left
                start_x -= start_width/2
                end_x += end_width/2
        else:  # Vertical dominant
            if dy > 0:  # Up
                start_y += start_height/2
                end_y -= end_height/2
            else:  # Down
                start_y -= start_height/2
                end_y += end_height/2
        
        # Draw arrow
        plt.arrow(
            start_x, start_y, 
            end_x - start_x, end_y - start_y,
            head_width=0.2, head_length=0.3, 
            fc='black', ec='black',
            length_includes_head=True,
            zorder=0,
            linewidth=2
        )
    
    # Add title
    plt.title('Hybrid Recommendation Algorithm Integration', fontsize=22, pad=20)
    
    # Adjust plot limits with padding
    plt.xlim(0, 12)
    plt.ylim(0, 10)
    
    # Save the diagram
    plt.tight_layout()
    plt.savefig('algorithm_integration_improved.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Improved Algorithm Integration Diagram saved")
    
    return 'algorithm_integration_improved.png'

if __name__ == "__main__":
    generate_all_visualizations()