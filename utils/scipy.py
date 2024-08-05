import numpy as np

def euclidean_distance(u, v):
    return np.sqrt(np.sum((u - v) ** 2))

def cdist(XA, XB, metric='euclidean'):
    if metric != 'euclidean':
        raise NotImplementedError("This implementation only supports the Euclidean distance.")
    
    XA = np.asarray(XA)
    XB = np.asarray(XB)
    
    nA = XA.shape[0]
    nB = XB.shape[0]
    
    distances = np.zeros((nA, nB))
    
    for i in range(nA):
        for j in range(nB):
            distances[i, j] = euclidean_distance(XA[i], XB[j])
    
    return distances