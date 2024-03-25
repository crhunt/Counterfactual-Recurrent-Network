import os
import logging

if 'CRN_VERSION' not in os.environ:
    logging.info("No env variable CRN_VERSION found. Defaulting to v1.")
    import tensorflow as tf
    from tensorflow.contrib.rnn import LSTMCell, DropoutWrapper
    from tensorflow.python.ops import rnn
    os.environ['CRN_VERSION'] = 'v1'
else:
    if "v1" == os.environ['CRN_VERSION']:
        import tensorflow as tf
        from tensorflow.contrib.rnn import LSTMCell, DropoutWrapper
        from tensorflow.python.ops import rnn
    elif "compat" == os.environ['CRN_VERSION']:
        import tensorflow.compat.v1 as tf
        tf.disable_v2_behavior()
        from tensorflow.compat.v1.nn.rnn_cell import LSTMCell, DropoutWrapper
        from tensorflow.python.ops import rnn
    elif "v2" == os.environ['CRN_VERSION']:
        import tensorflow as tf
        import keras
    else:
        logging.info("Version CRN_VERSION not valid. Defaulting to v1.")
        import tensorflow as tf
        from tensorflow.contrib.rnn import LSTMCell, DropoutWrapper
        from tensorflow.python.ops import rnn
