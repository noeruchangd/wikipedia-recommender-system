from wikirecommender.recommender import WikipediaRecommender

recommender = WikipediaRecommender()
recommender.load_articles(1200)
recommender.save_to_file('test', True)
