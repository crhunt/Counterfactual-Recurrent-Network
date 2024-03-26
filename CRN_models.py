
import os
import logging

# This is trivial for compat but will be used for supporting a TF 2 / Keras 3 version of CRN.

if 'CRN_VERSION' not in os.environ:
    logging.info("No env variable CRN_VERSION found. Defaulting to v1.")
    os.environ['CRN_VERSION'] = 'v1'

if "compat" == os.environ['CRN_VERSION']:
    from CRN_model import CRN_Model
elif "v2" == os.environ['CRN_VERSION']:
    from CRN_model_v2 import CRN_Model
else:
    if "v1" != os.environ['CRN_VERSION']:
        logging.info("CRN_VERSION not valid. Defaulting to v1.")
        os.environ['CRN_VERSION'] = 'v1'
    from CRN_model import CRN_Model
