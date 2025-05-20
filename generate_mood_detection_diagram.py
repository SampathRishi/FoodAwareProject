import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import matplotlib.patheffects as PathEffects

def generate_improved_mood_detection_pipeline():
    print("Generating Improved Mood Detection Pipeline Diagram...")
    
    # Create figure with white background - INCREASED SIZE
    plt.figure(figsize=(16, 10), facecolor='white')
    ax = plt.gca()
    plt.axis('off')
    
    # Define component positions and sizes - INCREASED SPACING
    components = {
        'user_input': {'pos': (1.5, 5), 'size': (2.0, 1.5), 'color': '#e6f7ff', 
                       'label': 'User Chat Input'},
        
        'preprocessing': {'pos': (5, 5), 'size': (2.0, 1.5), 'color': '#f9e79f', 
                          'label': 'Text Preprocessing\n- Tokenization\n- Cleaning'},
        
        'api_call': {'pos': (9, 5), 'size': (2.2, 1.8), 'color': '#aed6f1', 
                     'label': 'OpenAI API Call\nSystem Prompt:\n"Detect mood from text"'},
        
        'mapping': {'pos': (13, 5), 'size': (2.0, 1.5), 'color': '#d5f5e3', 
                    'label': 'Mood Mapping\nto 5 Categories'},
        
        'result': {'pos': (16.5, 5), 'size': (2.2, 1.8), 'color': '#fadbd8', 
                   'label': 'Detected Mood\n(Happy, Sad, Stressed,\nRelaxed, Adventurous)'},
        
        'fallback': {'pos': (9, 2), 'size': (2.5, 1.5), 'color': '#d7bde2', 
                     'label': 'Fallback Mechanism\n(Keyword Matching)'},
        
        'error': {'pos': (5.5, 3.5), 'size': (1.5, 1.0), 'color': '#f5b7b1', 
                  'label': 'API Error?'},
    }
    
    # Draw components
    for key, component in components.items():
        x, y = component['pos']
        width, height = component['size']
        
        # Create fancy box with rounded corners
        box = FancyBboxPatch(
            (x - width/2, y - height/2), width, height,
            boxstyle="round,pad=0.4",
            facecolor=component['color'],
            edgecolor='black',
            linewidth=1.5,
            alpha=0.9,
            zorder=1
        )
        ax.add_patch(box)
        
        # Add text with slight shadow effect for better visibility
        text = ax.text(
            x, y, component['label'],
            ha='center', va='center',
            fontsize=13, fontweight='bold',
            zorder=2
        )
        text.set_path_effects([
            PathEffects.withStroke(linewidth=2, foreground='white')
        ])
    
    # Draw arrows with increased spacing
    arrows = [
        ('user_input', 'preprocessing'),
        ('preprocessing', 'api_call'),
        ('api_call', 'mapping'),
        ('mapping', 'result'),
        ('api_call', 'error', {'connectionstyle': 'arc3,rad=-0.2', 'color': 'red', 'linewidth': 1.5}),
        ('error', 'fallback', {'connectionstyle': 'arc3,rad=-0.2', 'color': 'red', 'linewidth': 1.5}),
        ('fallback', 'result', {'connectionstyle': 'arc3,rad=0.3', 'color': 'red', 'linewidth': 1.5})
    ]
    
    for arrow in arrows:
        start = arrow[0]
        end = arrow[1]
        
        # Get positions
        start_x, start_y = components[start]['pos']
        end_x, end_y = components[end]['pos']
        
        # Get component sizes
        start_width, start_height = components[start]['size']
        end_width, end_height = components[end]['size']
        
        # Calculate arrow adjustment based on component positions
        dx = end_x - start_x
        dy = end_y - start_y
        
        # Adjust arrow start and end points based on direction
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
        
        # Default arrow style
        arrow_style = {'color': 'black', 'linewidth': 2, 'arrowstyle': '->', 'connectionstyle': 'arc3,rad=0.0'}
        
        # Custom arrow style if provided
        if len(arrow) > 2:
            arrow_style.update(arrow[2])
        
        # Draw the arrow
        arrow_patch = FancyArrowPatch(
            (start_x, start_y), (end_x, end_y),
            **arrow_style,
            zorder=0
        )
        ax.add_patch(arrow_patch)
    
    # Add text labels for special arrow cases - ADJUSTED POSITIONS
    plt.text(5.8, 3.0, "YES", fontsize=12, ha='center', va='center', color='red', fontweight='bold')
    plt.text(10, 3.0, "Alternative", fontsize=12, ha='center', va='center', color='red')
    
    # Add main path label - ADJUSTED POSITION
    plt.text(9, 6.5, "Main Processing Path", fontsize=14, ha='center', va='center', 
             fontweight='bold', bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.3'))
    
    # Add example text boxes with MORE SPACE
    examples = [
        {'pos': (1.5, 8), 'text': 'Example Input: "I feel so happy today and energetic!"', 'result': 'Detected: Happy'},
        {'pos': (9, 8), 'text': 'Example Input: "I\'m feeling down and tired..."', 'result': 'Detected: Sad'},
        {'pos': (16.5, 8), 'text': 'Example Input: "So nervous about my presentation!"', 'result': 'Detected: Stressed'}
    ]
    
    for i, example in enumerate(examples):
        x, y = example['pos']
        rect = Rectangle(
            (x - 2.5, y - 0.8), 5, 1.6,
            facecolor='#f8f9fa',
            edgecolor='#dddddd',
            linewidth=1,
            alpha=0.7,
            zorder=0
        )
        ax.add_patch(rect)
        plt.text(x, y + 0.2, example['text'], ha='center', va='center', fontsize=11)
        plt.text(x, y - 0.4, example['result'], ha='center', va='center', fontsize=12, color='#2980b9', fontweight='bold')
    
    # Add explanation of fallback mechanism - REPOSITIONED
    fallback_explanation = (
        "Fallback Mechanism:\n"
        "When API is unavailable, uses keyword\n"
        "matching to detect mood.\n\n"
        "Example keywords:\n"
        "- Happy: 'glad', 'joy', 'great'\n"
        "- Sad: 'down', 'blue', 'unhappy'"
    )
    
    plt.text(3, 2, fallback_explanation, ha='left', va='center', fontsize=11,
             bbox=dict(facecolor='#f8f9fa', edgecolor='#dddddd', alpha=0.7, boxstyle='round,pad=0.5'))
    
    # Set proper layout with more padding
    plt.tight_layout(pad=2.0)
    plt.subplots_adjust(top=0.9)
    
    # Set limits with generous padding
    plt.xlim(0, 19)
    plt.ylim(0, 10)
    
    # Add title with more space
    plt.title('FOODAWARE Mood Detection Pipeline', fontsize=24, pad=30)
    
    # Save figure
    plt.savefig('mood_detection_pipeline_improved.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Improved Mood Detection Pipeline Diagram saved to mood_detection_pipeline_improved.png")
    return 'mood_detection_pipeline_improved.png'

# Execute the function if run directly
if __name__ == "__main__":
    generate_improved_mood_detection_pipeline()