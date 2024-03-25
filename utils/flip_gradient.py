"""
CODE ADAPTED FROM https://github.com/pumpikano/tf-dann/blob/master/flip_gradient.py
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

'''
import os
if 'CRN_VERSION' not in os.environ:
    logging.info("No env variable CRN_VERSION found. Defaulting to v1.")
    import tensorflow as tf
    os.environ['CRN_VERSION'] = 'v1'
elif "v1" == os.environ['CRN_VERSION']:
    import tensorflow as tf
else:
    import tensorflow.compat.v1 as tf
    tf.disable_v2_behavior()
'''
from tensorflow_compat import tf

from tensorflow.python.framework import ops


class FlipGradientBuilder(object):
    def __init__(self):
        self.num_calls = 0

    def __call__(self, x, alpha):
        grad_name = "FlipGradient%d" % self.num_calls

        # Custom gradients in Tensorflow v2: https://stackoverflow.com/questions/55764694/how-to-use-gradient-override-map-in-tensorflow-2-0

        @ops.RegisterGradient(grad_name)
        def _flip_gradients(op, grad):
            return [tf.negative(grad) * alpha]
        """
        # Convert the code above into tensorflow v2 
        @tf.custom_gradient
        def _flip_gradients(x):
            def grad(dy):
                return [-dy * alpha]
            return tf.identity(x), grad
        """

        g = tf.get_default_graph()
        with g.gradient_override_map({"Identity": grad_name}):
            y = tf.identity(x)

        self.num_calls += 1
        return y

flip_gradient = FlipGradientBuilder()

