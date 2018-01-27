import tensorflow as tf
from openrec.recommenders import BPR
from openrec.modules.interactions import PairwiseEuDist

class CML(BPR):

    def _build_post_training_ops(self):
        unique_user_id, _ = tf.unique(self._user_id_input)
        unique_item_id, _ = tf.unique(tf.concat([self._p_item_id_input, self._n_item_id_input], axis=0))
        return [self._user_vec.censor_l2_norm_op(censor_id_list=unique_user_id),
                self._p_item_vec.censor_l2_norm_op(censor_id_list=unique_item_id)]

    def _build_interactions(self, train=True):

        if train:
            self._add_module('interaction',
                            PairwiseEuDist(user=self._get_module('user_vec').get_outputs()[0], 
                                    p_item=self._get_module('p_item_vec').get_outputs()[0],
                                    n_item=self._get_module('n_item_vec').get_outputs()[0], 
                                    p_item_bias=self._get_module('p_item_bias').get_outputs()[0],
                                    n_item_bias=self._get_module('n_item_bias').get_outputs()[0], 
                                    scope='PairwiseEuDist', reuse=False, train=True),
                            train=True)
        else:
            self._add_module('interaction',
                            PairwiseEuDist(user=self._get_module('user_vec', train=train).get_outputs()[0], 
                                     item=self._get_module('item_vec', train=train).get_outputs()[0],
                                    item_bias=self._get_module('item_bias', train=train).get_outputs()[0],
                                    scope='PairwiseEuDist', reuse=True, train=False),
                            train=False)
