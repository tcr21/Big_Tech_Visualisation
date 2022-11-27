from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from neo4j import GraphDatabase
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json
from bson import json_util

app = Flask(__name__, static_folder="frontend/build", static_url_path="")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"

load_dotenv()
uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(uri, auth=(username, password))
db = driver.session()

# Workaround to access Node properties (which Neo4j made private...)
def bind(instance, func):
    bound_method = func.__get__(instance, instance.__class__)
    setattr(instance, func.__name__, bound_method)
    return bound_method


def get_properties(self):
    return self._properties


def get_all_labels():
    results = db.run("MATCH (n) RETURN DISTINCT labels(n)")
    labels = [record[0] for record in results]
    unique_labels = set([item for sublist in labels for item in sublist])
    return list(unique_labels)


def get_all_relationships():
    results = db.run("MATCH (n)-[r]-(m) RETURN DISTINCT type(r)")
    relationships = [record[0] for record in results]
    return relationships


@app.route("/api/get_article_links")
def get_article_links():
    myclient = MongoClient(os.getenv("MONGODB_SERVER"))
    db = myclient["visualising_news"]
    collection = db["raw_articles"]
    cursor = collection.find({})
    json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]

    return jsonify(json_docs)


@app.route("/api")
def get_nodes_and_links():
    labels = get_all_labels()
    relationships = get_all_relationships()

    nodes = []
    links = []
    i = 0

    for j, label_n in enumerate(labels):
        for label_m in labels[j:]:
            for relationship in relationships:
                if not (label_n == 'News' and label_m == 'News'):
                    results = db.run("MATCH (n:{label_n})-[r:{relationship}]-(m:{label_m}) RETURN n as {label_n}, collect(m) as {label_m}_collection".format(
                        label_n=label_n, relationship=relationship, label_m=label_m))
                    
                    for record in results:
                        bind(record[label_n], get_properties)
                        target_node = {
                            "properties": record[label_n].get_properties(),
                            "label": list(record[label_n].labels)[0],
                        }
                        try:
                            target = nodes.index(target_node)
                        except ValueError:
                            nodes.append(target_node)
                            target = i
                            i += 1

                        for element in record["{}_collection".format(label_m)]:
                            bind(element, get_properties)
                            source_node = {
                                "properties": element.get_properties(),
                                "label": list(element.labels)[0],
                            }
                            try:
                                source = nodes.index(source_node)
                            except ValueError:
                                nodes.append(source_node)
                                source = i
                                i += 1

                            links.append(
                                {
                                    "source": source,
                                    "target": target,
                                    "relationship": relationship,
                                }
                            )

    driver.close()
    return jsonify({"nodes": nodes, "links": links})


@app.route("/")
@cross_origin()
def serve():
    """
    Returns index.html file from frontend/build (app.static_folder)
    """
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    app.run()