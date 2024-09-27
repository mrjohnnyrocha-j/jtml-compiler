import logging

logger = logging.getLogger(__name__)

class DependencyResolver:
    def parse_dependencies(self, root):
        # Parses dependencies listed in the 'depends-on' attribute of the root element
        dependencies = root.attrib.get('depends-on', '')
        return [dep.strip() for dep in dependencies.split(',') if dep.strip()]

    def build_dependency_graph(self, components):
        # Build a dependency graph from component dependencies
        graph = {}
        for component_name, component_data in components.items():
            graph[component_name] = component_data['dependencies']
        return graph

    def topological_sort(self, graph):
        # Perform a topological sort to resolve the dependency order
        visited = set()
        stack = []

        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for neighbor in graph.get(node, []):
                visit(neighbor)
            stack.insert(0, node)

        for node in graph:
            visit(node)
        return stack
