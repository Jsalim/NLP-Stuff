import sys, os
import pickle
import networkx as nx

OUT = 'test_graph_output_prune.dot'
prune = 1       # simple method to keep edges above prune weight

'''Load pickled dictionary'''
print "loading pickled dictionary..."
NLP_direc = '/Users/sinn/NLP-Stuff/'
with open(os.path.join(NLP_direc, 'WordNets/def_mapping02.pkl'), 'rb') as f1:
    data = pickle.load(f1)

'''Create directed graph'''
print "Creating graph from dict..."
G = nx.DiGraph()
for key in data.keys():
    G.add_node(key)
  #  G.node[key]['label'] = key
'''Add weighted edges in bunches'''
print "Adding edges..."
for key in data.keys():
    values = data[key]
    we = [(key,n,w) for n,w in values if w > prune]
    G.add_weighted_edges_from(we)

    
##'''Get undirected graph, get connected components'''
##UG = G.to_undirected()
##CC = nx.connected_components(UG)


print "Attempting to create output .dot file..."
try:
    nx.drawing.write_dot(G,os.path.join(NLP_direc, OUT))
except ImportError, e:
    print e
    print 'Shit sucks, using the "windows" file version...'
    # Help for Windows users (or OSX on old intel users...)
    # Not a general purpose method, but representative of
    # the same output write_dot would provide for this graph
    # if installed and easy to implement
    dot = []
    for (n1, n2) in G.edges():
        #dot.append('"%s" [label="%s"]' % (n2, G.node[n2]['label']))
        dot.append('"%s" -> "%s" [weight="%s"]' % (n1, n2, G[n1][n2]['weight']))

    f = open(os.path.join(NLP_direc, 'WordNets', OUT), 'w')
    f.write('''strict digraph {
    %s
    }''' % (';\n'.join(dot), ))
    f.close()
