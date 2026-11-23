from wikirecommender.recommender import WikipediaRecommender

recommender = WikipediaRecommender()
recommender.load_articles(1000)
recommender.save_to_file('text_data', True)
recommender.save_to_file('tfidf_data', False)

