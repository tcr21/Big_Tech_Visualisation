"""
File:           wiki_data_retriever.py
Author:         Ted Jenks
Creation Date:  27/01/2022
Last Edit Date: 03/02/2022
Last Edit By:   Ted Jenks

Class:          WikiDataRetriever()
Functions:      get_name(self), get_description(self), get_location(self), 
                get_property_values(self, property_code)

Summary of File:

    Contains class to get data from WikiData.
"""
from urllib.error import URLError
import urllib.request
import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

class WikiDataRetriever:
    def __init__(self, code) -> None:
        self.head_company_code = code
        self.head_company_filename = "head_company"
        # try:
        self.__download_entity_json(self.head_company_code, self.head_company_filename)
        self.head_company_data = self.__read_json(self.head_company_filename)
        self.head_company_name = self.__retrieve_name(
            self.head_company_code, self.head_company_data
        )
        self.head_company_description = self.__retrieve_description(
            self.head_company_code, self.head_company_data
        )
        self.head_company_location = self.__retrieve_location(
            self.head_company_code, self.head_company_data
        )
        os.remove("graph_db_generator/head_company.json")
        # except:
        #     raise TypeError(
        #         'Failed to retrive company data. Check company code is valid: ',
        #         self.head_company_code)
        self.error_log = []
        print("WikiDataRetriever setup complete")

    def get_name(self):
        return self.head_company_name

    def get_description(self):
        return self.head_company_description

    def get_location(self):
        return self.head_company_location

    def get_property_values(self, property_code):
        print("Retrieving properties...")

        entity_codes = self.__retrieve_property_entities(
            self.head_company_code, property_code, self.head_company_data
        )
        names = [""] * len(entity_codes)
        descriptions = [""] * len(entity_codes)
        humans = [False] * len(entity_codes)
        locations = [""] * len(entity_codes)
        for (i, code) in enumerate(entity_codes):
            try:
                self.__download_entity_json(code, "temp")
                temp = self.__read_json("temp")
            except URLError:
                self.error_log.append("Invalid entity code in sub-entity retrieval")
                continue
            except:
                self.error_log.append("Error in file handling at entity name retrieval")
                continue

            try:
                names[i] = self.__retrieve_name(code, temp)
                descriptions[i] = self.__retrieve_description(code, temp)
                humans[i] = self.__is_human(code, temp)
                locations[i] = self.__retrieve_location(code, temp)
            except KeyError:
                self.error_log.append(
                    "Warning: Invalid dict lookup in entity's name and description retrieval"
                )
                continue
        try:
            os.remove("graph_db_generator/temp.json")
        except Exception as error:
            self.error_log.append("Error removing temp files")
        self.__check_errors()
        return names, entity_codes, descriptions, humans, locations

    def __download_entity_json(self, code, filename):
        urllib.request.urlretrieve(
            "https://www.wikidata.org/wiki/Special:EntityData/" + code + ".json",
            "graph_db_generator/" + filename + ".json",
        )
        return

    def __read_json(self, filename):
        with open("graph_db_generator/" + filename + ".json") as data_file:
            return json.load(data_file)

    def __retrieve_name(self, code, data):
        try:
            res = data["entities"][str(code)]["labels"]["en-gb"]["value"]
        except:
            res = data["entities"][str(code)]["labels"]["en"]["value"]
        return res

    def __retrieve_description(self, code, data):
        try:
            res = data["entities"][str(code)]["descriptions"]["en-gb"]["value"]
        except:
            res = data["entities"][str(code)]["descriptions"]["en"]["value"]
        return res

    def __retrieve_location(self, code, data):
        try:
            locID = data["entities"][str(code)]["claims"]["P159"][0]["mainsnak"][
                "datavalue"
            ]["value"]["id"]
            self.__download_entity_json(locID, "loc")
            locationData = self.__read_json("loc")
            os.remove("graph_db_manager/loc.json")
            return self.__retrieve_name(locID, locationData)
        except:
            return ""

    def __is_human(self, code, data):
        try:
            if (
                data["entities"][str(code)]["claims"]["P31"][0]["mainsnak"][
                    "datavalue"
                ]["value"]["id"]
                == "Q5"
            ):
                return True
            return False
        except:
            return False

    def __is_holding(self, code, data):
        try:
            if (
                data["entities"][str(code)]["claims"]["P31"][0]["mainsnak"][
                    "datavalue"
                ]["value"]["id"]
                == "Q219577"
            ):
                return True
            return False
        except:
            return False

    def __retrieve_property_entities(self, code, property_code, data):
        try:
            entities = data["entities"][str(code)]["claims"][property_code]
        except KeyError:
            self.error_log.append("Entity does not have property: " + property_code)
            return []
        vals = []
        for entity in entities:
            try:
                vals.append(entity["mainsnak"]["datavalue"]["value"]["id"])
            except KeyError:
                self.error_log.append("Cannot locate entity ID")
                continue
        return vals

    def __check_errors(self):
        if self.error_log != []:
            print("ERRORS IN READ:")
            for error in self.error_log:
                print(error)
        else:
            print("Properties retrieved without errors.")
        print("\n")
        self.error_log = []
        return
