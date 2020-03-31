using LightGraphs



function component(graph)
    component = []
    stack = []
    vertex_start = vertices(graph)[1]
    push!(stack, (vertex_start, neighbors(graph, vertex_start)))
    rem_vertex!(graph, vertex_start) 

    while length(stack) > 0
        vert_nxt = pop!(stack)
        append!(component, vert_nxt[1])

        for neigh = vert_nxt[2]
            if has_vertex(graph, neigh)
                push!(stack, (neigh, neighbors(graph, neigh)))
                rem_vertex!(graph, neigh)
            end
        end
    end
    return component, graph
end

function components(graph)
    connected_components = []

    while nv(graph) > 0
        # append!(connected_components, component(graph))
        res, graph = component(graph)
    end

    return connected_components
end


NUM_NODES = 100000
NUM_EDGES = (NUM_NODES*log(NUM_NODES))/8
graph = erdos_renyi(NUM_NODES, NUM_EDGES)

@time begin
    # components(graph)
end
