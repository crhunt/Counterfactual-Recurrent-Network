# Copyright (c) 2020, Ioana Bica

import os
import argparse
import logging

def init_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chemo_coeff", default=2, type=int)
    parser.add_argument("--radio_coeff", default=2, type=int)
    parser.add_argument("--results_dir", default='results')
    parser.add_argument("--model_name", default="crn_test_2")
    parser.add_argument("--b_encoder_hyperparm_tuning", default=False)
    parser.add_argument("--b_decoder_hyperparm_tuning", default=False)
    parser.add_argument("--version", default="v1")
    parser.add_argument("--load_data", default=True)
    return parser.parse_args()

args = init_arg()
os.environ['CRN_VERSION'] = str(args.version)

'''
if args.version == "v1":
    from CRN_model import CRN_Model
elif args.version == "v2":
    from CRN_model_v2 import CRN_Model
elif args.version == "compat":
    from CRN_model_compat import CRN_Model
else:
    raise ValueError("Invalid CRN_Model version.")
'''

from CRN_encoder_evaluate import test_CRN_encoder
from CRN_decoder_evaluate import test_CRN_decoder
from utils.cancer_simulation import get_cancer_sim_data

if __name__ == '__main__':

    #args = init_arg()

    if not os.path.exists(args.results_dir):
        os.mkdir(args.results_dir)

    save_data = not args.load_data

    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    pickle_map = get_cancer_sim_data(chemo_coeff=args.chemo_coeff, radio_coeff=args.radio_coeff, b_load=args.load_data,
                                          b_save=save_data, model_root=args.results_dir)

    base_model_name = args.model_name + '_CRNversion-' + args.version
    encoder_model_name = 'encoder_' + base_model_name
    encoder_hyperparams_file = '{}/{}_best_hyperparams.txt'.format(args.results_dir, encoder_model_name)

    models_dir = '{}/crn_models'.format(args.results_dir)
    if not os.path.exists(models_dir):
        os.mkdir(models_dir)

    rmse_encoder = test_CRN_encoder(pickle_map=pickle_map, models_dir=models_dir,
                                    encoder_model_name=encoder_model_name,
                                    encoder_hyperparams_file=encoder_hyperparams_file,
                                    b_encoder_hyperparm_tuning=args.b_encoder_hyperparm_tuning)


    decoder_model_name = 'decoder_' + base_model_name
    decoder_hyperparams_file = '{}/{}_best_hyperparams.txt'.format(args.results_dir, decoder_model_name)

    """
    The counterfactual test data for a sequence of treatments in the future was simulated for a 
    projection horizon of 5 timesteps. 
   
    """

    max_projection_horizon = 5
    projection_horizon = 5
    
    rmse_decoder = test_CRN_decoder(pickle_map=pickle_map, max_projection_horizon=max_projection_horizon,
                                    projection_horizon=projection_horizon,
                                    models_dir=models_dir,
                                    encoder_model_name=encoder_model_name,
                                    encoder_hyperparams_file=encoder_hyperparams_file,
                                    decoder_model_name=decoder_model_name,
                                    decoder_hyperparams_file=decoder_hyperparams_file,
                                    b_decoder_hyperparm_tuning=args.b_decoder_hyperparm_tuning)

    logging.info("Chemo coeff {} | Radio coeff {}".format(args.chemo_coeff, args.radio_coeff))
    print("RMSE for one-step-ahead prediction.")
    print(rmse_encoder)

    print("Results for 5-step-ahead prediction.")
    print(rmse_decoder)
