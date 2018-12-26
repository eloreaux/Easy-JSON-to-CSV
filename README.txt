# This is a series of functions for forcing a 
JavaScript Object Notation data structure into a pandas dataframe object.

The JSON object that this was written for was collected via an API and
    resembles the following structure:

    A list of objects, with each object representing a desired row in the new dataframe.

    Each object is a dictionary of nested values that range from strings, to lists of strings, to other dictionaries.
        - You may need to tweak this code if your initial JSON organization is different, with the bulk of the code
            being easily generalizable once you find a way to obtain something of this structure.

    Here is an example of a highly simplified JSON file that this code will work immediately for:

    [{customer_name: {"first" : "Eric",
			"last" : "Loreaux"},
      customer_age: "23"},
      
      {customer_name: {"first" : "Tom",
			"last" : "Burke"},
       customer_age: "23",
       customer_weight: "197"}]

    it will return a dataframe of the following structure:

    customer_name.first customer_name.last  customer_age    customer_max_bench
    "Eric"              "Loreaux"           "23"            ""
    "Tom"               "Burke"             "23"            "197"

    Notice the inclusion of a blank value for rows in which there was no value for a particular column. Feel free to tweak this value, it is located at the top of both .py files as the BLANKVALUE variable.

    The client has a choice for how to handle nested lists. Consider the following example:

    [{customer_name: ["Eric","E-Money"],
      customer_age: "23"},
      
      {customer_name: "Tom",
       customer_age: "23"}]

    1. if the stringList argument is set to True, the resulting dataframe will leave these lists as strings:

    customer_name           customer_age    
    "['Eric','E-Money']"    "23"
    "Tom"                   "23"

    2. if the stringList argument is set to False, the resulting dataframe will create new columns for each value:

    customer_name   customer_name.2 customer_age
    "Eric"          "E-Money"       "23"
    "Tom"           ""              "23"

    Keep in mind that the first option can be dangerous if you expect there to be lists of values other than strings.
        e.g. a list of dictionaries turned into a string will be difficult to understand

    If you choose to go with the second option, you can also limit the amount of new columns created by invoking the repLimit argument.
	The default limit is set to 3, and this would be useful if you really only cared about the first three nicknames for a user.
	You can change this limit by tweaking the REPLIMIT value in the json_to_csv_utils.py file.

Here's how you would use this in the terminal:

	1. Place these two files in a directory of your choice	

	2. call the json_to_csv.py file with an argument specifying a path to a json file or directory of json files to turn into a single csv file:

		$python json_to_csv.py <json_path>

	3. There are a number of optional arguments, which you can learn more about by typing in the following:

		$python json_to_csv.py -h



    All in all, this code may need some tweaking to fit your specific use, but I hope it saves you some time.