# -*- coding: utf-8 -*-

from deeppavlov.skills.pattern_matching_skill import PatternMatchingSkill
from deeppavlov.contrib.skills.similarity_matching_skill import SimilarityMatchingSkill
from deeppavlov.agents.default_agent.default_agent import DefaultAgent
from deeppavlov.agents.processors.highest_confidence_selector import HighestConfidenceSelector
from deeppavlov.utils.alice import start_agent_server


hello = PatternMatchingSkill(responses=['Добро пожаловать', 'Приветствую тебя, друг мой'], patterns=['Привет', 'Здравствуйте', 'Здравствуй', 'Здорово', 'Ку'], default_confidence = 0.01)
bye = PatternMatchingSkill(responses=['На этом прощаюсь с тобой', 'Всего доброго'], patterns=['До свидания'])
fallback = PatternMatchingSkill(responses=['Мысль свою изложи подробнее, юный падаван'], default_confidence = 0.01)
faq = SimilarityMatchingSkill(save_load_path = './model', train = False)

agent = DefaultAgent([hello, bye, faq, fallback], skills_selector=HighestConfidenceSelector())


start_agent_server(agent, host='0.0.0.0', port=5000, endpoint='/faq', ssl_key='/etc/letsencrypt/live/serg.ml/privkey.pem', ssl_cert='/etc/letsencrypt/live/serg.ml/fullchain.pem')
