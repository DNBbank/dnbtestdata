#!/usr/bin/env python3
import argparse

from models.person.person import Person
from utils.file_util import FileUtil


def create_list_of_people_json(number_of_people):
    people = list()
    for i in range(number_of_people):
        random_person = Person.generate_random()
        people.append(random_person.to_json())
    return people


parser = argparse.ArgumentParser(description="Quick hack to generate fake people and some data.")
parser.add_argument('-n', type=int, default=10, help='The number of people to create')
args = parser.parse_args()

FileUtil.json_to_json_file(create_list_of_people_json(args.n), 'generated-people')
