import os
import string
from octis.dataset.dataset import Dataset
from octis.preprocessing.preprocessing import Preprocessing
from octis.models.LDA import LDA
from octis.evaluation_metrics.diversity_metrics import TopicDiversity
from skopt.space.space import Real, Categorical, Integer
from octis.optimization.optimizer import Optimizer
from octis.evaluation_metrics.coherence_metrics import Coherence
import time

def run_and_test_lda(dataset, data_source):
    # model = LDA()
    # search_space = {
    #     'decay': Real(0.5, 1.0),
    #     'alpha': Categorical({'symmetric', 'asymmetric', 'auto'}),
    #     'num_topics': Integer(5, 25)
    # }

    # coherence = Coherence(texts=dataset.get_corpus(), measure = 'c_v')
    # optimization_runs = 45
    # model_runs = 5

    # optimizer=Optimizer()
    # start = time.time()
    # optimization_result = optimizer.optimize(
    #     model, dataset, coherence, search_space, number_of_call=optimization_runs, 
    #     model_runs=model_runs, save_models=True, 
    #     extra_metrics=None, # to keep track of other metrics
    #     save_path='optimize_result/lda_{}//'.format(data_source))
    # end = time.time()
    # duration = end - start
    # optimization_result.save_to_csv("optimize_result_{}.csv".format(data_source))
    # print('Optimizing model took: ' + str(round(duration)) + ' seconds.')

    model = LDA(num_topics=19,
decay=0.8033352903402347,
alpha='auto')
    model_output = model.train_model(dataset)

    for t in model_output['topics']:
        print(' '.join(t))


    npmi = Coherence(texts=dataset.get_corpus(), measure='c_v')
    topic_diversity = TopicDiversity(topk=10)

    topic_diversity_score = topic_diversity.score(model_output)
    print("Topic diversity: "+str(topic_diversity_score))

    npmi_score = npmi.score(model_output)
    print("Coherence: "+str(npmi_score))


OCTIS_DATA_PATH = 'octis_data'

DATA_SOURCE = 'onestop'
# DATA_SOURCE = 'muse'

CORPUS_PATH = os.path.join(OCTIS_DATA_PATH, DATA_SOURCE)

PREPATH = os.path.join('preprocessed_' + DATA_SOURCE)

if not os.path.exists(PREPATH):
    # Initialize preprocessing
    preprocessor = Preprocessing(vocabulary=None, max_features=None, 
                                remove_punctuation=True, punctuation=string.punctuation,
                                lemmatize=True, stopword_list='english', split=True,
                                min_chars=1, min_words_docs=0)
    # preprocess
    dataset = preprocessor.preprocess_dataset(documents_path=CORPUS_PATH + '/corpus.txt' )
    dataset.save(PREPATH)
    # run_and_test_lda(dataset, DATA_SOURCE)
else:
    dataset = Dataset()
    dataset.load_custom_dataset_from_folder(PREPATH)
    # run_and_test_lda(dataset, DATA_SOURCE)





