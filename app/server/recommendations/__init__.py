"""
Recommendation systems for the app,
there are multiple because this project aims to compare different recommendation systems
"""

from .method_average import AverageRecommendation
from .method_weighted_average import WeightedAverageRecommendation

supported_methods = ["average", "weighted"]