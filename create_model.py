from deeppavlov.contrib.skills.similarity_matching_skill import SimilarityMatchingSkill
import sys


path = 'quotes_' + str(sys.argv[1]) + '.csv'

faq = SimilarityMatchingSkill(data_path = path,
                              x_col_name = 'Question', 
                              y_col_name = 'Answer',
                              save_load_path = './model',
                              config_type = 'tfidf_autofaq',
                              edit_dict = {},
                              train = True)
