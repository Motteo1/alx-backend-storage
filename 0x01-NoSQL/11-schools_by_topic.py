#!/usr/bin/env python3
""" Where to learn python """


def schools_by_topic(mongo_collection, topic):
    """schools by topic"""
    return mongo_collection.find({"topics": topic})