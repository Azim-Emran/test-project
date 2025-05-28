from sklearn.cluster import KMeans

def cluster_students(data):
    model = KMeans(n_clusters=3)
    clusters = model.fit_predict(data)
    return clusters
