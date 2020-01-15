import os 
import corpus_hdf5
import numpy as np
import jnius_config
from jnius import autoclass
import numpy as np
import pytrec_eval
import pandas as np 
import gzip

def format_trec(corpus_path,pathwrite):
    corpus = corpus_hdf5.CorpusHDF5('jeopardy_corpus.hdf5') 
    # f_out = gzip.open("msa_corpus_trec.gz","wb")
    with gzip.open("jeopardy_corpus_trec.gz", 'wb') as fd:
        doc_id=0
        for title,txt in zip(corpus.get_title_iter(),corpus.get_text_iter()):
            str_out=""
            str_out+= '<DOC>\n' 
            str_out+= '<DOCNO>'
            str_out+= str(doc_id)
            str_out+= '</DOCNO>\n'
            str_out+='<HEAD>\n'
            str_out+=('<TITLE>')
            str_out+=str(title)
            str_out+='</TITLE>\n'
            str_out+='</HEAD>\n'
            str_out+='<BODY>\n'
            str_out+=str(txt)
            str_out+='\n'
            str_out+='</BODY>\n'
            str_out+='</DOC>'
    #         print(str_out)
            fd.write(str_out.encode('utf-8'))
            doc_id+=1
        
    

def t_search():
    os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-1.8.0-openjdk-amd64"

    # another parameter needs to config. 
    jnius_config.set_classpath("terrier-project-5.2-SNAPSHOT-jar-with-dependencies.jar")
    JIR = autoclass('org.terrier.querying.IndexRef')
    JMF = autoclass('org.terrier.querying.ManagerFactory')

    appSetup = autoclass('org.terrier.utility.ApplicationSetup')
    appSetup.setProperty("querying.processes","terrierql:TerrierQLParser,parsecontrols:TerrierQLToControls,parseql:TerrierQLToMatchingQueryTerms,matchopql:MatchingOpQLParser,applypipeline:ApplyTermPipeline,localmatching:LocalManager$ApplyLocalMatching,qe:QueryExpansion,labels:org.terrier.learning.LabelDecorator,filters:LocalManager$PostFilterProcess")
    appSetup.setProperty("querying.postfilters","decorate:SimpleDecorate,site:SiteFilter,scope:Scope")
    appSetup.setProperty("querying.default.controls","wmodel:DPH,parsecontrols:on,parseql:on,applypipeline:on,terrierql:on,localmatching:on,filters:on,decorate:on")

    indexref = JIR.of("/content/data.properties")
    # input the prm.data_properties=./data.properties
    manager = JMF._from_(indexref)


    JIF = autoclass('org.terrier.structures.IndexFactory')
    index = JIF.of(indexref)

    # srq = manager.newSearchRequest("Q0", "university of glasgow")
    #qid= using the dataset_hdf5 to read the query id
    # query= using the dataset_hdf5. 
    srq = manager.newSearchRequest(qid,query)
    srq.setControl("end", "9")
    # srq.addMatchingModel("Matching","BM25")
    srq.setControl("decorate", "on")
    manager.runSearchRequest(srq)
    # get the candidates's id, then choose one of the id using corpus_hdf5.get_article_text(docid) as the candidate terms of D0, 
    # And using corpus_hdf5.get_article_title(docid) as the title 
    # calculate the recall,map, ndcg of the initial retrieval.

    for i, item in enumerate( srq.getResults()):

      print("%d %s %f" % (i, item.getMetadata("docno"),  item.getScore()))
    # return ....

# clear about what the out is

def get_candidates(self, qs, max_cand, max_full_cand=None, save_cache=False, extra_terms=True):
    if not max_full_cand:
        max_full_cand = max_cand

    if prm.docs_path != prm.docs_path_term:
        max_cand2 = 0
    else:
        max_cand2 = max_full_cand
    
    out = self.t_search(qs, max_cand, max_cand2, self.searcher)   

    return out





    


    
    