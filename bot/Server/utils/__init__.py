import pickle


dumps = lambda obj: pickle.dumps(obj, -1)

loads = lambda data: pickle.loads(data)