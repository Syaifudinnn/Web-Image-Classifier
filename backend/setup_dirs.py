import os
import shutil

def setup_directories():
    """
    Create necessary directories and ensure files are in correct locations
    """
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create app directory if it doesn't exist
    app_dir = os.path.join(current_dir, 'app')
    os.makedirs(app_dir, exist_ok=True)
    
    # Create models directory if it doesn't exist
    models_dir = os.path.join(app_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    
    # Create api directory if it doesn't exist
    api_dir = os.path.join(app_dir, 'api')
    os.makedirs(api_dir, exist_ok=True)
    
    # Create __init__.py files if they don't exist
    open(os.path.join(app_dir, '__init__.py'), 'a').close()
    open(os.path.join(models_dir, '__init__.py'), 'a').close()
    open(os.path.join(api_dir, '__init__.py'), 'a').close()
    
    # Check if imagenet_classes.json exists in both places and copy if needed
    source_json = os.path.join(models_dir, 'imagenet_classes.json')
    alt_json = os.path.join(current_dir, 'app', 'models', 'imagenet_classes.json')
    
    # Create a simple classes file if none exists
    if not os.path.exists(source_json) and not os.path.exists(alt_json):
        print("Creating a simple imagenet_classes.json file...")
        simple_classes = {}
        for i in range(1000):
            simple_classes[str(i)] = f"class_{i}"
        
        import json
        with open(source_json, 'w') as f:
            json.dump(simple_classes, f)
        
        # Also copy to the alternative location
        os.makedirs(os.path.dirname(alt_json), exist_ok=True)
        shutil.copy(source_json, alt_json)

if __name__ == "__main__":
    setup_directories()
    print("Directory setup complete!")