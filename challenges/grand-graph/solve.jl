using LightGraphs, MetaGraphs, StatsBase


function propagate(graph, node, col)

    # Initialize stack and push root onto it.
    stack = [] 
    push!(stack, node)
    
    # Propagate color to all nodes in component.
    while length(stack) > 0
        node_current = pop!(stack)
        set_prop!(graph, node_current, :col, col)
        for neigh = neighbors(graph, node_current)
            if get_prop(graph, neigh, :col) != col
                push!(stack, neigh)
            end
        end
    end

    # Return graph with propagated values.
    return graph
end


function get_frac_max_cc(num_nodes)
    
    # Initialize empty graph.
    graph = MetaGraph(SimpleGraph{Int64}(num_nodes))
    nodes = collect(vertices(graph))

    # Initialize next color to use.
    col_nxt = 0
    
    # Start timer.
    start = time()

    # Add edges to graph.
    for idx = 1:(num_nodes*log(num_nodes))/8

        # Randomly sample two nodes and add edge.
        a, b = sample(nodes, 2, replace=false)
        add_edge!(graph, a, b)
        
        if length(props(graph, a)) == 0 && length(props(graph, b)) == 0
            # If both nodes do not have color.
            set_prop!(graph, a, :col, col_nxt)
            set_prop!(graph, b, :col, col_nxt)
            col_nxt += 1

        elseif length(props(graph, a)) == 0 && length(props(graph, b)) != 0
            # If first node does not have a color.
            col = get_prop(graph, b, :col)
            set_prop!(graph, a, :col, col)

        elseif length(props(graph, a)) != 0 && length(props(graph, b)) == 0
            # If second node does not have a color.
            col = get_prop(graph, a, :col)
            set_prop!(graph, b, :col, col)

        else
            # If both nodes have a color, merge and propagate.
            col_a = get_prop(graph, a, :col)
            col_b = get_prop(graph, b, :col)
            if col_a != col_b
                graph = propagate(graph, a, col_a)
            end
        end
    end

    # Return fraction of nodes in largest connected component.
    return maximum(values(countmap([get_prop(graph, v, :col) for v in collect(vertices(graph)) if length(props(graph, v)) > 0])))/num_nodes, time() - start

end

# Run test.
for num_nodes = 1000:1000:100000
    frac_max_cc, elapsed = get_frac_max_cc(num_nodes)
    print("n: ")
    print(num_nodes)
    print(", links: ")
    print(Int(ceil((num_nodes*log(num_nodes))/8)))
    print(" proportion of nodes in S: ")
    print(round(frac_max_cc, digits=4))
    print(" time ")
    print(round(elapsed, digits=4))
    println("s")

end


