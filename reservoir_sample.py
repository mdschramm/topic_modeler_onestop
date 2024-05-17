import random
from collections import Counter
import csv
from utils import process_description

class ReservoirSampler:
    def __init__(self,k):
        # Size of sample
        self.k = k
        # Current size of inmut data
        self.N = 0

        self.sample_array = []

    def sample(self, word_array):
        for item in word_array:
            self.N += 1
            if len(self.sample_array) < self.k:
                self.sample_array.append(item)
            else:
                s = int(random.random() * self.N)
                if s < self.k:
                    self.sample_array[s] = item

    def getsample(self):
        return self.sample_array
    

rs = ReservoirSampler(k=50)
total_counter = Counter()

def sample_data_file(filename, desc_col, rs, total_counter):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            text, filtered_words = process_description(line[0])

            total_counter += Counter(list(filtered_words))
            rs.sample(list(filtered_words))

sample_data_file('preprocessed_onestop/corpus.tsv', 'description', rs, total_counter)
print(rs.getsample())
print(total_counter.most_common(50))