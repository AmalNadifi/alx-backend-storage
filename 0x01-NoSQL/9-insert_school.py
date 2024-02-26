#!/usr/bin/env python3
"""
The following script has a utility function that inserts documents
"""
import pymongo


def insert_school(mongo_collection, **kwargs):
        """
        This function inserts into school
        """
        return mongo_collection.insert_one(kwargs).inserted_id
