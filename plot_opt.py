import matplotlib.pyplot as plt
import json

file = 'results/test_ctm/result.json'
results = json.load(open(file))

# plt.xlabel('Iteration')
# plt.ylabel('Coherence score (c_v)')
# plt.title('Median coherence score per iteration')
# plt.plot(results['f_val'])
# plt.show()

print(results['x_iters']['num_topics'][23])
print(results['x_iters']['decay'][23])
print(results['x_iters']['alpha'][23])