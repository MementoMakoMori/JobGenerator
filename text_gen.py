from textgenrnn import textgenrnn

# default params
model_cfg = {
    'rnn_size': 128,  # number of LSTM cells per layer
    'rnn_layers': 4,  # number of LSTM layers
    'rnn_bidirectional': False,
    'max_length': 10,  # number of tokens to consider for prediction the next token
    'max_words': 20000,
    'word_level': True  # neural net could be trained at the word level or character level
}

train_cfg = {
    'line_delimited': True,  # each text is its own line in the .txt file
    'num_epochs': 75,
    'gen_epochs': 15,  # generate example output in the console every x number of epochs
    'batch_size': 2048,
    'train_size': 1,
    'validation': False,
    'dropout': 0.02,  # ignore a proportion of source tokens each epoch
    'max_gen_length': 350,  # the average number of words per job description was 588, I want it a bit smaller
    'is_csv': False
}

file_combo = 'combo_data.txt'
model_name = 'sw_job_combo'
combogen = textgenrnn(name=model_name)

train_function = combogen.train_from_file if train_cfg['line_delimited'] else combogen.train_from_largetext_file

train_function(
    file_path=file_combo,
    new_model=True,
    num_epochs=train_cfg['num_epochs'],
    gen_epochs=train_cfg['gen_epochs'],
    batch_size=train_cfg['batch_size'],
    train_size=train_cfg['train_size'],
    dropout=train_cfg['dropout'],
    validation=train_cfg['validation'],
    is_csv=train_cfg['is_csv'],
    rnn_layers=model_cfg['rnn_layers'],
    rnn_size=model_cfg['rnn_size'],
    rnn_bidirectional=model_cfg['rnn_bidirectional'],
    max_length=model_cfg['max_length'],
    dim_embeddings=100,
    word_level=model_cfg['word_level'])

# with open('results.txt', 'w') as f:
#     textgen.generate_to_file(f, temperature=[1.0, 0.5, 0.2, 0.2], prefix=None, n=100, max_gen_length=200)

# combogen = textgenrnn(weights_path='sw_job_combo_weights.hdf5', vocab_path='sw_job_combo_vocab.json', config_path='sw_job_combo_config.json')

