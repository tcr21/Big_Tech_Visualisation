#starts the virtualenv you need
. /home/njf21/project/venv/bin/activate

#Get to the project root directory
cd  /home/njf21/project/

#runs required Python file
python3 /home/njf21/project/graph_db_generator/generate_graph.py

#kills virtualenv
deactivate
