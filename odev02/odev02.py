import sys
s=""
start=""
end=""
if len(sys.argv)-1 == 2:
    start = sys.argv[1]
    end = sys.argv[2]

elif len(sys.argv)-1 == 4:
    start = sys.argv[1]+""+sys.argv[2]
    end = sys.argv[3]+""+sys.argv[2]

#elif len(sys.argv)-1 == 3:
#    print("Which one consists of two words? Please write first or second.")
#    input(s)
#    if s == "first":
#        start = sys.argv[1]+""+sys.argv[2]
#        end = sys.argv[3]
#    if s == "second":
#        start = sys.argv[1]
#        end = sys.argv[2]+""+sys.argv[3]

print(start, end)


class Graph(object):

    def __init__(self, graph_dict=None):

        if graph_dict == None:
            graph_dict = {}
        self.__graph_dict = graph_dict

    def vertices(self):

        return list(self.__graph_dict.keys())

    def edges(self):

        return self.__generate_edges()

    def add_vertex(self, vertex):

        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def add_edge(self, edge):

        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]

    def __generate_edges(self):

        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res


    def find_path(self, start_vertex, end_vertex, path=None):
        if path == None:
            path = []
        graph = self.__graph_dict
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return path
        if start_vertex not in graph:
            return None
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_path = self.find_path(vertex,end_vertex,path)
                if extended_path:
                    return extended_path
        return None



f = open("airlines.txt","r")
#f = open("/Users/basak/Desktop/airlines.txt","r")
g = {}

for line in f:
    splittedLine=line.strip().split(",")
    g[splittedLine[0]]=splittedLine[1:]

graph = Graph(g)

#print("Vertices of graph:")
#print(graph.vertices())

#print("Edges of graph:")
#print(graph.edges())

print("The path from",start, "to", end , ":")
path = graph.find_path(start, end)
print(path)






f.close()
