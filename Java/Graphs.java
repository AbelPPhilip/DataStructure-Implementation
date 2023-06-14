
package implementation;

import java.util.*;

/**
 * Implements a graph. We use two maps: one map for adjacency properties 
 * (adjancencyMap) and one map (dataMap) to keep track of the data associated 
 * with a vertex. 
 * 
 * @author cmsc132
 * 
 * @param <E>
 */
public class Graph<E> {
	/* You must use the following maps in your implementation */
	private HashMap<String, HashMap<String, Integer>> adjacencyMap;
	private HashMap<String, E> dataMap;
    
	public Graph() {
		adjacencyMap = new HashMap<String, HashMap<String, Integer>>();
		dataMap = new HashMap<String, E>();
	}
	
	public void addVertex(String vertexName, E data) {
		if (!(adjacencyMap.containsKey(vertexName))) {
			adjacencyMap.put(vertexName, new HashMap<String, Integer>());
		}
		dataMap.put(vertexName, data);
	}
	
	public void doBreadthFirstSearch(String startVertexName, CallBack<E> callback) {
		if(dataMap.containsKey(startVertexName)) {
			HashSet<String> visited = new HashSet<String>();
			Queue<String> discovered = new PriorityQueue<String>();
			discovered.offer(startVertexName);
			while(!(discovered.isEmpty())) {
				String x = discovered.remove();
				if(!(visited.contains(x))){
					visited.add(x);
					callback.processVertex(x, getData(x));
					for(String successor : adjacencyMap.get(x).keySet()) {
						if(!(visited.contains(successor))) {
							discovered.add(successor);
						}
					}
				}
			}
		}else {
			throw new IllegalArgumentException("Vertex not found");
		}
	}
	
	public void doDepthFirstSearch(String startVertexName, CallBack<E> callback) {
		if (dataMap.containsKey(startVertexName)) {
			HashSet<String> visited = new HashSet<String>();
			Stack<String> discovered = new Stack<String>();
			discovered.push(startVertexName);
			while(!(discovered.isEmpty())) {
				String x = discovered.pop();
				if(!(visited.contains(x))){
					visited.add(x);
					callback.processVertex(x, getData(x));
					for(String successor : adjacencyMap.get(x).keySet()) {
						if(!(visited.contains(successor))) {
							discovered.add(successor);
						}
					}
				}
			}
		}
		else {
			throw new IllegalArgumentException("Vertex not found");
		}
		
	}
	
	public int doDijkstras(String startVertexName, String endVertexName, ArrayList<String>shortestPath) {
		if (startVertexName == null || endVertexName== null) {
			throw new IllegalArgumentException("Invalid Parameters");
		}
		/*
		if (!(dataMap.containsKey(startVertexName)) || !(dataMap.containsKey(endVertexName))) {
			throw new IllegalArgumentException("Vertices not found");
		}*/
		
		TreeMap<String, Integer> explored = new TreeMap<String, Integer>();
		TreeMap<String, Integer> unExplored = new TreeMap<String, Integer>();
		for (String s : dataMap.keySet()) {
			if (!s.equals(startVertexName)) {
				unExplored.put(s, Integer.MAX_VALUE);
				System.out.println(s);
			}
		}
		explored.put(startVertexName, 0);
		TreeMap<String, String> predecessor = new TreeMap<String, String>();
		
		String currentVertex = startVertexName;
		while(!(unExplored.isEmpty())) {
			for (String s : unExplored.keySet()) {
				if (adjacencyMap.get(currentVertex).containsKey(s)) {
					if (explored.get(currentVertex)+getCost(currentVertex,s) < unExplored.get(s)) {
						unExplored.put(s,explored.get(currentVertex)+getCost(currentVertex,s));
						predecessor.put(s,currentVertex);
					}
				}
			}
			String minCostVertex = findMin(unExplored);
			explored.put(minCostVertex, unExplored.get(minCostVertex));
			unExplored.remove(minCostVertex);
			currentVertex = minCostVertex;	
		}
		currentVertex = endVertexName;
		while (currentVertex != startVertexName) {
			String currentValue = predecessor.get(currentVertex);
			if (currentValue == null) {
				shortestPath.clear();
				shortestPath.add("None");
				return -1;
			}
			shortestPath.add(0, currentValue);
			currentVertex = currentValue;
		}
		shortestPath.add(endVertexName);
		return explored.get(endVertexName);
		
		
		
	}
	
	private String findMin( TreeMap<String, Integer> map) {
		String min = map.firstKey();
		for (String s : map.keySet()) {
			if (map.get(s)<map.get(min)) {
				min = s;
			}
		}
		return min;
	}
	
	public int getCost(String startVertexName, String endVertexName) {
		return adjacencyMap.get(startVertexName).get(endVertexName);
	}
	
	public int totalVertices() {
		int counter = 0;
		for (String s : dataMap.keySet()) {
			if (adjacencyMap.get(s)!= null) {
				counter++;
			}
		}
		return counter;
	}
	
	public Map<String, Integer> getAdjacentVertices(String vertexName){
		if (adjacencyMap.containsKey(vertexName)) {
			if (adjacencyMap.get(vertexName).isEmpty()) {
				return new HashMap<String, Integer>();
			}
			return adjacencyMap.get(vertexName);
		}
		return null;
		
	}
	
	public E getData(String vertex) {
		if (dataMap.containsKey(vertex)) {
			return dataMap.get(vertex);
		}
		throw new IllegalArgumentException("Vertex not found");
	}
	
	public String toString() {
		String str ="";
		TreeSet<String> orderedDataMap = new TreeSet<String>(dataMap.keySet());
		str+="Vertices: "+orderedDataMap.toString()+"\n";
		str+="Edges: \n";
		for(String s : orderedDataMap) {
			str+="Vertex("+s+")--->"+adjacencyMap.get(s).toString()+"\n";
		}
		return str;
	}

	public void addDirectedEdge(String string, String string2, int i) {
		// TODO Auto-generated method stub
		if (dataMap.containsKey(string) && dataMap.containsKey(string2)) {
			if (adjacencyMap.get(string)==null) {
				HashMap<String, Integer> adjacencies = new HashMap<String, Integer>();
				adjacencies.put(string2, i);
				adjacencyMap.put(string2, adjacencies);
			}else {
				HashMap<String, Integer> adjacencies = adjacencyMap.get(string);
				adjacencies.put(string2,i);
				adjacencyMap.put(string, adjacencies);
			}
			
		}
	}

	public Set<String> getVertices() {
		// TODO Auto-generated method stub
		return dataMap.keySet();
	}
}
