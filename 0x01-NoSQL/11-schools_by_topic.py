#!/usr/bin/env python3
"""
The following script returns the list of school having a specific topic
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
        """
        The function finds a school having a specific topic

        Args:
            mongo_collection: the pymongo collection object
            topics(string): the topic searched
        """
        return mongo_collection.find({"topics": topic})
