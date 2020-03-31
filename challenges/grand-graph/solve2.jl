using StatsBase

NUM_NODES = 100000

function merge(graph, node1, node2)
    # Get index of component containing first node.
    comp1 = findall(map(x -> node1 in x, graph))[1]

    # Get index of component containing second node.
    comp2 = findall(map(x -> node2 in x, graph))[1]

    # If components not same, merge.
    if comp1 != comp2
        graph[comp1] = vcat(graph[comp1], graph[comp2])
        deleteat!(graph, comp2)
    end
    return graph
end

function compute_frac_lcc(num_nodes)
    nodes = 1:NUM_NODES
    graph = [[el] for el in nodes]

    @time begin
        for idx = 1:(NUM_NODES*log(NUM_NODES))/8
            node1, node2 = sample(nodes, 2, replace=false) 
            graph = merge(graph, node1, node2)
            
            # Get index of component containing first node.
            comp1 = findall(map(x -> node1 in x, graph))[1]

            # Get index of component containing second node.
            comp2 = findall(map(x -> node2 in x, graph))[1]

            # If components not same, merge.
            if comp1 != comp2
                graph[comp1] = vcat(graph[comp1], graph[comp2])
                deleteat!(graph, comp2)
            end
        end
    end
end

compute_frac_lcc(NUM_NODES)

