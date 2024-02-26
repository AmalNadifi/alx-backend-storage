#!/usr/bin/env python3
"""
The following script has a utility function listing all documents
"""
import pymongo


def list_all(mongo_collection):
        """
        This function lists documents in a collection
        """
        if not mongo_collection:
            return []
        return list(mongo_collection.find())
