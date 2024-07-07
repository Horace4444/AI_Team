import subprocess
import sys
import os
import json
import requests
from flask import Flask, render_template, request, redirect, url_for

# Initialize Flask app
app = Flask(__name__)

# Function to load the JSON database
def load_teams():
    with open('teams.json', 'r') as file:
        return json.load(file)

# Function to save the JSON database
def save_teams(data):
    with open('teams.json', 'w') as file:
        json.dump(data, file, indent=4)

# Function to install a package
def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Function to install packages
def install_packages(packages):
    for package in packages:
        try:
            __import__(package)
            print(f"{package} is already installed.")
        except ImportError:
            print(f"{package} is not installed. Installing now...")
            try:
                install_package(package)
            except subprocess.CalledProcessError as e:
                print(f"Error installing {package}: {e}")
                print("Attempting to resolve dependencies...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--use-feature=2020-resolver"])
            except Exception as e:
                print(f"An unexpected error occurred while installing {package}: {e}")

# Function to get packages from LLM
def get_packages_from_llm(project_name, capabilities, objectives, avoidances, loop_breakers, artifacts):
    # Replace with the actual API call to the LLM
    response = requests.post('https://api.example.com/get-packages', json={
        'project_name': project_name,
        'capabilities': capabilities,
        'objectives': objectives,
        'avoidances': avoidances,
        'loop_breakers': loop_breakers,
        'artifacts': artifacts
    })
    response_data = response.json()
    return response_data['packages']

# Endpoint to render the input form
@app.route('/', methods=['GET', 'POST'])
def index():
    teams = load_teams()
    if request.method == 'POST':
        if 'save_project' in request.form:
            project_name = request.form['new_project_name']
            new_team = {
                "name": project_name,
                "capabilities": request.form['capabilities'],
                "objectives": request.form['objectives'],
                "avoidances": request.form['avoidances'],
                "loop_breakers": request.form['loop_breakers'],
                "artifacts": request.form['artifacts']
            }
            teams['teams'].append(new_team)
            save_teams(teams)
            return redirect(url_for('index'))

        else:
            project_name = request.form['project_name']
            team_type = request.form['team']
            if team_type == 'Create A New Team':
                team_type = request.form['new_team_name']
                capabilities = request.form['capabilities']
                objectives = request.form['objectives']
                avoidances = request.form['avoidances']
                loop_breakers = request.form['loop_breakers']
                artifacts = request.form['artifacts']
            else:
                selected_team = next((team for team in teams['teams'] if team['name'] == team_type), {})
                capabilities = selected_team.get('capabilities')
                objectives = selected_team.get('objectives')
                avoidances = selected_team.get('avoidances')
                loop_breakers = selected_team.get('loop_breakers')
                artifacts = selected_team.get('artifacts')

            # Get the required packages from LLM
            packages = get_packages_from_llm(project_name, capabilities, objectives, avoidances, loop_breakers, artifacts)
            install_packages(packages)

            return redirect(url_for('success'))

    return render_template('index.html', teams=teams['teams'])

# Endpoint to render the success page
@app.route('/success')
def success():
    return "All required packages are installed."

# CLI command to run the Flask app
def run_flask_app():
    app.run(debug=True)

if __name__ == '__main__':
    run_flask_app()
