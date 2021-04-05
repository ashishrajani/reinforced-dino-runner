import os
import pickle
import pandas as pd
from collections import deque

# stored results path
loss_file_path = "./output/loss_df.csv"
actions_file_path = "./output/actions_df.csv"
q_value_file_path = "./output/q_values_df.csv"
scores_file_path = "./output/scores_df.csv"


class DataLoader:

    def __init__(self, init_cache=False):
        self.init_cache()
        # Initialize log structures from file if exists else create new
        self.loss_df = pd.read_csv(loss_file_path) if os.path.isfile(loss_file_path) else pd.DataFrame(columns=['loss'])
        self.scores_df = pd.read_csv(scores_file_path) if os.path.isfile(loss_file_path) else pd.DataFrame(columns=['scores'])
        self.actions_df = pd.read_csv(actions_file_path) if os.path.isfile(actions_file_path) else pd.DataFrame(columns=['actions'])
        self.q_values_df = pd.read_csv(actions_file_path) if os.path.isfile(q_value_file_path) else pd.DataFrame(columns=['qvalues'])
        return

    def save_obj(self, obj, name):
        # dump files into objects folder
        with open('./output/' + name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def load_obj(self, name):
        # load from file system

        with open('./output/' + name + '.pkl', 'rb') as f:
            return pickle.load(f)

    # training variables saved as checkpoints to filesystem to resume training from the same step
    def init_cache(self, epsilon):
        """initial variable caching, done only once"""

        self.save_obj(epsilon, "epsilon")

        t = 0
        self.save_obj(t, "time")

        D = deque()
        self.save_obj(D, "D")

    def is_loss_file_present(self):
        return os.path.isfile(loss_file_path)

    def store_action(self, action):
        # append action to actions data frame

        self.actions_df.loc[len(self.actions_df)] = action

    def store_scores(self, score):
        # append score to scores data frame

        self.scores_df.loc[len(self.loss_df)] = score

    def store_loss(self, loss):
        # append loss to losses data frame

        self.loss_df.loc[len(self.loss_df)] = loss

    def store_q_value(self, q_value):
        # append q_value to q_values data frame

        self.q_values_df.loc[len(self.q_values_df)] = q_value

    def store_values_to_file(self):
        self.loss_df.to_csv(loss_file_path, index=False)
        self.scores_df.to_csv(scores_file_path, index=False)
        self.actions_df.to_csv(actions_file_path, index=False)
        self.q_values_df.to_csv(q_value_file_path, index=False)
