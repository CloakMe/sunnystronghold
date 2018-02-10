
def preprocess_docs(holders):
    return list(map(preprocess_doc, holders))

def preprocess_doc(holder):
    return preprocess_doc_assign_weights(holder)

# TODO: list all distinct paragraph keys - maybe we've missed something
def preprocess_doc_assign_weights(holder):
    text = ""
    
    text = append_content(text, holder.get("Title"), 3)
    text = append_content(text, holder.get("Keywords"), 3)
    text = append_content(text, holder.get("Categories"), 3)
    
    text = append_content(text, holder.get("Product"), 1)
    text = append_content(text, holder.get("Symptoms"), 1)
    text = append_content(text, holder.get("Purpose"), 1)
    text = append_content(text, holder.get("Purpose"), 1)
    text = append_content(text, holder.get("Details"), 1)

    return text

def append_content(text, content, count):
    if(content is not None):
        if(type(content) is list):
            content = " ".join(content)
        content_mult = (content + " ")*count
        return text + " " + content_mult
    else:
        return text