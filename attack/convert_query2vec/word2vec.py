from gensim.models.keyedvectors import KeyedVectors

# -- coding: utf-8 --

class word2vec(object):
    def __init__(self):
        self.model = KeyedVectors.load_word2vec_format("google.bin.gz", binary=True)


    "不存在建立词典，词典就在当前目录。google.tar.gz"
    def query_to_vector(self,query):
        #model = KeyedVectors.load_word2vec_format("google.bin.gz", binary=True)
        length = 300
        ret = [0] * length
        cnt = 0
        query_word = query.split(" ")
        for word in query_word:
            #print("start processing ")
            try:
                #tmp_vec = model[word]
                tmp_vec = self.model[word]
                for i in range(0, length):
                    ret[i] += tmp_vec[i]
                cnt += 1
            except:
                pass
        if cnt == 0:
            return ret
        for i in range(0, len(ret)):
            ret[i] /= cnt
        #print("end of processing ")
        return ret

if __name__ == "__main__":
    w2v = word2vec()
    result = w2v.query_to_vector('this is a test')
    print(len(result))
    print("=======")
    result = w2v.query_to_vector('I love china')
    print(len(result))
    print("=======")


#result = query_to_vector('this is a test')
#print(result)
