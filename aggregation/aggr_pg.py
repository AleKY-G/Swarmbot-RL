# class of the deep neural network with policy gradient method

# hold data and computation for the neural network and policy gradient method

# input observation, output the action from the neural net
# input a batch of data set(one set includes observation, action, and reward), and training
# the deep neural network

import tensorflow as tf
import numpy as np

class PolicyGradient:
    MULTIPLIER = 4  # control the size of the hidden layers
    def __init__(self, n_div, learning_rate):
        self.n_div = n_div  # number of neurons for both inputs and outputs
            # observation as inputs, action as outputs
        self.n_full = self.n_div * self.MULTIPLIER
            # number of neurons for all hidden layers
        self.lr = learning_rate
        # build the network
        self.ep_obs, self.ep_acts, self.ep_rews = [], [], []  # one episode of data
        self.build_net()
        self.sess = tf.Session()

    def build_net(self):
        with tf.name_scope('inputs'):
            self.obs = tf.placeholder(tf.float32, [None, self.n_div], name='observations')
            self.acts_ = tf.placeholder(tf.float32, [None, ], name='actions')  # labels
            self.rews = tf.placeholder(tf.float32, [None, ], name='rewards')
        # fc1
        dense1 = tf.layers.dense(
            inputs=self.obs,
            units=self.n_full,
            activation=tf.nn.relu,
            kernel_initializer=tf.random_normal_initializer(mean=0, stddev=0.3),
            bias_initializer=tf.constant_initializer(0.1),
            name='dense1')
        # fc2
        dense2 = tf.layers.dense(
            inputs=dense1,
            units=self.n_full,
            activation=tf.nn.relu,
            kernel_initializer=tf.random_normal_initializer(mean=0, stddev=0.3),
            bias_initializer=tf.constant_initializer(0.1),
            name='dense2')
        # fc3
        dense3 = tf.layers.dense(
            inputs=dense2,
            units=self.n_full,
            activation=tf.nn.relu,
            kernel_initializer=tf.random_normal_initializer(mean=0, stddev=0.3),
            bias_initializer=tf.constant_initializer(0.1),
            name='dense3')
        # fc4
        acts = tf.layers.dense(
            inputs=dense3,
            units=self.n_div,
            activation=tf.nn.relu,
            kernel_initializer=tf.random_normal_initializer(mean=0, stddev=0.3),
            bias_initializer=tf.constant_initializer(0.1),
            name='acts')
        # softmax layer
        self.acts_softmax = tf.nn.softmax(acts, name='acts_softmax')
        # loss
        with tf.name_scope('loss'):
            cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
                logits=acts, labels=self.acts_)
            loss = tf.reduce_mean(cross_entropy * self.rews)  # reward guided loss
        # train step
        with tf.name_scope('train'):
            self.train_step = tf.train.AdamOptimizer(self.lr).minimize(loss)

    # randomly choice an action based on action probabilities from nn
    def choose_action(self, observation):
        acts_prob = self.sess.run(
            self.acts_softmax, feed_dict={self.obs: observation[np.newaxis, :]})
        action = np.random.choice(range(self.n_div), p=acts_prob.ravel())
        return action

    # store one data sample including observation, action, and its reward
    def store_transition(self, observation, action, reward):
        self.ep_obs.append(observation)
        self.ep_acts.append(action)
        self.ep_rews.append(reward)

    def learn(self):
        rewards_norm = self.rewards_norm()
        # train on episode
        self.sess.run(self.train_step, feed_dict={
            self.obs: np.vstack(self.ep_obs),
            self.acts_: np.array(self.ep_acts),
            self.rews: rewards_norm,
            })
        # empty episode data after each training
        self.ep_obs, self.ep_acts, self.ep_rews = [], [], []
        return rewards_norm

    # normalize the rewards
    def rewards_norm(self):
        pass


