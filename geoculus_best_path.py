import cv2
import sys
import math
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

def euclid_dist( x,  y,  x2,  y2):
    return (int)((x2-x)**2 + (y2-y)**2)

path = sys.argv[1]

#grayscale
img = cv2.imread(path)
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#convert non-blacks to be white
(thresh, black_and_white_image) = cv2.threshold(gray_image, 15, 255, cv2.THRESH_BINARY)

height, width = black_and_white_image.shape

#invert it
inverted = ~black_and_white_image

#connected components
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(inverted, 8, cv2.CV_32S)
#tsp
#calculate distance matrix O(n^2)
nodes = len(centroids)
distances = [[0 for x in range(nodes)] for y in range(nodes)]
for row in range(0, nodes):
    for col in range(0, nodes):
        distances[row][col] = euclid_dist(centroids[col][0], centroids[col][1], centroids[row][0], centroids[row][1])

def distance_callback(from_index, to_index):
    """Returns the distance between the two nodes."""
    # Convert from routing variable Index to distance matrix NodeIndex.
    from_node = manager.IndexToNode(from_index)
    to_node = manager.IndexToNode(to_index)
    return distances[from_node][to_node]

#second arg: num vehicles, third arg: starting point
manager = pywrapcp.RoutingIndexManager(len(distances),1, 0)

# Create Routing Model
routing = pywrapcp.RoutingModel(manager)

transit_callback_index = routing.RegisterTransitCallback(distance_callback)

routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

# use guided local search
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy = (
    routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

# let google do all the hard work
solution = routing.SolveWithParameters(search_parameters)

def print_solution(manager, routing, solution):
    """Prints solution on console."""
    print('Objective: {} miles'.format(solution.ObjectiveValue()))
    index = routing.Start(0)
    plan_output = 'Route for vehicle 0:\n'
    route_distance = 0
    while not routing.IsEnd(index):
        plan_output += ' {} ->'.format(manager.IndexToNode(index))
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        #add lines
        from_node = manager.IndexToNode(previous_index)
        to_node = manager.IndexToNode(index)
        cv2.line(img, tuple(centroids[from_node].astype(int)), tuple(centroids[to_node].astype(int)), (0, 0, 255), 3)

        dist = distances[from_node][to_node]
        route_distance += dist
    plan_output += ' {}\n'.format(manager.IndexToNode(index))
    plan_output += 'Route distance: {}miles\n'.format(route_distance)
    cv2.imshow("poggers" , img)
    cv2.imwrite("poggers.jpg", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()  

print_solution(manager, routing, solution)