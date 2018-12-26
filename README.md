# Easy JSON to CSV

Let's face it. NoSQL-style nested data structures offer a lot of wonderful perks, but easy access to the contents within for high level analysis and visualization is not one of them. Have you ever come across data in a nested, noSQL-style JSON format and wished you could just force it into relational form for analysis in Pandas or R? I certainly have, and so I created this project with the intention of practicing my Python and sharing a simple, reusable toolkit for flattening nested data. The Pandas library comes with a similar function, 'read_json,' but I wanted a simpler and more flexible function that could be run on a .json file or on a directory of .json files. My function will output a .csv file containing the results, allowing users to abstract away any work directly within a python environment.

The JSON object that this function was written for was collected via an API and resembles the following structure: A list of objects, with each object representing a desired row in the new dataframe. Each object is a dictionary of nested values that range from strings, to lists of strings, to other dictionaries. **You may need to tweak this code if your initial JSON organization is different**, with the bulk of the code being easily generalizable once you find a way to obtain something of this structure.

Here is an example of a highly simplified JSON file that this code will work immediately for:

    [{customer_name: {"first" : "Eric",
			"last" : "Loreaux"},
      customer_age: "23"},
      {customer_name: {"first" : "Tom",
			"last" : "Burke"},
       customer_age: "23",
       customer_weight: "197"}]

It will return a dataframe of the following structure:

| customer_name.first | customer_name.last | customer_age | customer_weight |
| ------------------- | ------------------ | ------------ | --------------- |
| "Eric"              | "Loreaux"          | "23"         | ""              |
| "Tom"               | "Burke"            | "23"         | "197"           |

Notice the inclusion of a blank value for rows in which there was no value for a particular column. You can tweak this value, it is located at the top of the json_to_csv_utils.py file as the `BLANKVALUE` variable.

The client has a choice for how to handle nested lists. Consider the following example:

    [{customer_name: ["Eric","E-Money"],
      customer_age: "23"},
      {customer_name: "Tom",
       customer_age: "23"}]

1. If the `--stringList` argument is included on the command line, the resulting dataframe will leave these lists as strings:

    | customer_name         | customer_age  |
    | --------------------- | ------------  |
    | "['Eric','E-Money']"  | "23"          |
    | "Tom"                 | "23"          |

2. if the `--stringList` argument is not included, the resulting dataframe will create new columns for each value:

    | customer_name  |  customer_name.2 | customer_age |
    | -------------  | ---------------- | ------------ |
    | "Eric"         | "E-Money"        | "23"         |
    | "Tom"          | ""               | "23"         |

Keep in mind that the first option can be dangerous if you expect there to be lists of values other than strings (e.g. a list of dictionaries turned into a string will be difficult to understand).

If you choose to go with the second option, you can also limit the amount of new columns via the `--repLimit` argument. For example, it might be useful to set repLimit to 3 if you really only care about the first three names for a user.

Here's how you would use this from the terminal:

1. Clone this repository and cd into it.

2. Install dependencies:

```sh
$pip install -r requirements.txt
```

3. Call the json_to_csv.py file with an argument specifying a path to a json file or directory of json files to turn into a single csv file:

```sh
$python json_to_csv.py <json_path>
```

4. Learn more about all the optional arguments by typing in the following:

```sh
$python json_to_csv.py -h
```

All in all, this code may need some tweaking to fit your specific use, but I hope it saves you some time and allows you to more easily explore even the most complicated of nested data structures. If you have any suggestions for added options & functionality, please let me know, I would love to hear your thoughts. Enjoy!