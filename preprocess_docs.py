
def preprocess_docs(holders):
    return list(map(preprocess_doc, holders))

def preprocess_doc(holder):
    # TODO: do better stuff
    return holder["Document"]