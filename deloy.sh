# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install dependencies from requirements.txt
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run the application (example)
# echo "Running the application..."
# python main.py

# # Deactivate the virtual environment
# echo "Deactivating virtual environment..."
# deactivate

echo "Deployment completed successfully."