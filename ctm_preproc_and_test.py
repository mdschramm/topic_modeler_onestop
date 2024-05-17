
from octis.dataset.dataset import Dataset
from octis.evaluation_metrics.coherence_metrics import Coherence
from octis.models.CTM import CTM
from octis.optimization.optimizer import Optimizer
from skopt.space.space import Real, Categorical, Integer
from octis.evaluation_metrics.diversity_metrics import TopicDiversity
from utils import is_duplicate
import csv
import json
import matplotlib.pyplot as plt


text_file = 'preprocessed_onestop/corpus.txt'

# De-duplicate corpus.txt
def de_dupe():
    hashes = set()
    de_duped = []
    for line in open(text_file):
        if not is_duplicate(hashes, line):
            de_duped.append(line)

    with open(text_file, 'w') as f:
        for line in de_duped:
            f.write('{}'.format(line))


# def corpus_txt_to_tsv():
#     tsv_file = 'preprocessed_onestop/corpus.tsv'
#     with open(text_file) as source, open(tsv_file, mode='w', 
#                                          newline='', encoding='utf-8') as dest:
#         d = csv.DictWriter(dest, fieldnames=[0, 1], delimiter='\t',
#                             quoting=csv.QUOTE_NONE,
#                             escapechar='\\')
#         for line in source:
#             d.writerow({0: line.replace('\n', ''), 1: 'train'})

# corpus_txt_to_tsv()

dataset = Dataset()
dataset.load_custom_dataset_from_folder('preprocessed_onestop')

# model = CTM( num_epochs=30, inference_type='combined', 
#             bert_model="bert-base-nli-mean-tokens", bert_path='bert_19_topic',
#             num_layers=2, num_neurons=119, activation='softplus', dropout=.0966)

# coherence = Coherence(texts=dataset.get_corpus(), measure = 'c_v')

# search_space = {"num_topics": Categorical({25, 26, 27, 28, 29, 30, 33, 35, 40, 50})}

# optimization_runs= 10
# model_runs= 2

# optimizer=Optimizer()
# optimization_result = optimizer.optimize(
#     model, dataset, coherence, search_space, number_of_call=optimization_runs, 
#     model_runs=model_runs, save_models=True, 
#     extra_metrics=None, # to keep track of other metrics
#     save_path='results/test_ctm/',
#     plot_model=True)


def score_output_and_graph_coherence_over_num_topics():
    # Insert best parameters here
    model = CTM(num_topics=26, num_epochs=50, inference_type='combined', 
                bert_model="bert-base-nli-mean-tokens", bert_path='bert_19_topic',
                num_layers=2, num_neurons=119, activation='softplus', dropout=.0966)
    
    model_output = model.train_model(dataset)

    for t in model_output['topics']:
        print(' '.join(t))
    
    coherence = Coherence(texts=dataset.get_corpus(), measure = 'c_v')
    topic_diversity = TopicDiversity(topk=10)
    topic_diversity_score = topic_diversity.score(model_output)
    print("Topic diversity: "+str(topic_diversity_score))

    npmi_score = coherence.score(model_output)
    print("Coherence: "+str(npmi_score))

    file = 'results/test_ctm/result.json'
    results = json.load(open(file))
    x_vals = results['x_iters']['num_topics']
    y_vals = results['f_val']

    plt.xlabel('num_topics')
    plt.ylabel('Coherence score (c_v)')
    plt.title('Median coherence score vs num_topics')
    plt.scatter(x_vals, y_vals)
    plt.show()

score_output_and_graph_coherence_over_num_topics()