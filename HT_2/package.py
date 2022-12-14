import requests
from graphviz import Digraph

def get_edges(main_package, depth):
    edges = []
    try:
        json_str = requests.get("https://registry.npmjs.org/" + main_package + "/latest").json()
        dependencies = json_str["dependencies"]
        for package in dependencies.keys():
            vers = dependencies[package]
            if (main_package + "->" + package) not in edges:
                edges.append(main_package + "->" + package)
                graph.edge(main_package, package + ", version " + vers)
                if (depth < max_depth):
                    get_edges(package, depth + 1)
    except:
        if (depth == 0):
            print("Couldn't find this package")
        return

while (True):
    package_name = input("Input package name: ").lower()
    max_depth = int(input("Input max depth: "))
    graph = Digraph()
    get_edges(package_name, 0)
    print(graph.source)