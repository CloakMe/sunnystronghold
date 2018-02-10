import tfidf

if __name__ == "__main__":
    table = tfidf.TfIdf()
    table.add_document("foo", ["a", "b", "c", "d", "e", "f", "g", "h"])
    table.add_document("bar", ["a", "b", "c", "i", "j", "k"])
    table.add_document("baz", ["a", "l", "m", "n"])
    table.add_document("taz", ["t"])

    print table.similarities(["a", "l", "m", "n"])
    print table.similarities(["t"])
    #[["foo", 0.6875], ["bar", 0.75], ["baz", 0.0]])

