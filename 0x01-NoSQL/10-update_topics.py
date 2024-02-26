#!/usr/bin/env python3
"""
The following script changes all school topics
"""
import pymongo


def update_topics(mongo_collection, name, topics):
        """
        This function updates many rows in a school document

        Args:
        mongo_collection: the pymongo collection object
        name(string): the school name to update
        topics(list of strings): the list of topics approached in the school
        """
        return mongo_collection.update_many(
                {"name": name},
                {"$set": {"topics": topics}}
        )
