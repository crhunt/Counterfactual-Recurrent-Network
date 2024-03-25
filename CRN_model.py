
import logging
import os

if 'CRN_VERSION' not in os.environ:
    logging.info("No env variable CRN_VERSION found. Defaulting to v1.")
    from CRN_model_v1 import CRN_Model
    os.environ['CRN_VERSION'] = 'v1'
elif "v1" == os.environ['CRN_VERSION']:
    from CRN_model_v1 import CRN_Model
elif "v2" == os.environ['CRN_VERSION']:
    from CRN_model_v2 import CRN_Model
elif "compat" == os.environ['CRN_VERSION']:
    from CRN_model_compat import CRN_Model
else:
    logging.info("CRN_VERSION not valid. Defaulting to v1.")
    from CRN_model import CRN_Model
