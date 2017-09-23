"""
Type descriptions of Twitterverse and Query dictionaries
(for use in docstrings)

Twitterverse dictionary:  dict of {str: dict of {str: object}}
    - each key is a username (a str)
    - each value is a dict of {str: object} with items as follows:
        - key "name", value represents a user's name (a str)
        - key "location", value represents a user's location (a str)
        - key "web", value represents a user's website (a str)
        - key "bio", value represents a user's bio (a str)
        - key "following", value represents all the usernames of users this 
          user is following (a list of str)
       
Query dictionary: dict of {str: dict of {str: object}}
   - key "search", value represents a search specification dictionary
   - key "filter", value represents a filter specification dictionary
   - key "present", value represents a presentation specification dictionary

Search specification dictionary: dict of {str: object}
   - key "username", value represents the username to begin search at (a str)
   - key "operations", value represents the operations to perform (a list of str)

Filter specification dictionary: dict of {str: str}
   - key "following" might exist, value represents a username (a str)
   - key "follower" might exist, value represents a username (a str)
   - key "name-includes" might exist, value represents a str to match (a case-insensitive match)
   - key "location-includes" might exist, value represents a str to match (a case-insensitive match)

Presentation specification dictionary: dict of {str: str}
   - key "sort-by", value represents how to sort results (a str)
   - key "format", value represents how to format results (a str)
   
"""

# Write your Twitterverse functions here

def process_username (data_file, given_username, twitter_dict):
    """ (file open for reading, str, dict of {str: dict of {str: object}}) ->
    NoneType
    
    Format information on the given_username in the data_file onto the 
    twitter_dict.
    """
    
    twitter_dict[given_username] = {}
    twitter_dict[given_username]['name'] = data_file.readline().strip()
    twitter_dict[given_username]['location'] = data_file.readline().strip()
    twitter_dict[given_username]['web'] = data_file.readline().strip()
    bio = ''
    line = data_file.readline().strip()
    while line != 'ENDBIO':
        bio += line + '\n'
        line = data_file.readline().strip()
    twitter_dict[given_username]['bio'] = bio[:-1]
    twitter_dict[given_username]['following'] = []
    line = data_file.readline().strip()
    while line != 'END':
        twitter_dict[given_username]['following'].append(line)
        line = data_file.readline().strip()

def process_data (data_file):
    """ (file open for reading) -> dict of {str: dict of {str: object}}
    
    Return a dictionary of the formatted data_file containing information about
    the twitter users.
    """
    
    twitter_dict = {}
    username = data_file.readline().strip()
    while username != '':
        process_username(data_file, username, twitter_dict)
        username = data_file.readline().strip()
    return twitter_dict

def process_query (data_file):
    """ (file open for reading) -> dict of {str: dict of {str: object}}
    
    Return a dictionary of the formatted data_file containing information about
    certain specifications.
    """
    
    data_file.readline()
    query_dict = {}
    query_dict['search'] = {}
    query_dict['filter'] = {}
    query_dict['present'] = {}
    query_dict['search']['username'] = data_file.readline().strip()
    query_dict['search']['operations'] = []
    line = data_file.readline().strip()
    while line != 'FILTER':
        query_dict['search']['operations'].append(line)
        line = data_file.readline().strip()
    line = data_file.readline().strip()
    filter_strings = []
    while line != 'PRESENT':
        filter_strings = line.split()
        query_dict['filter'][filter_strings[0]] = filter_strings[1]
        line = data_file.readline().strip()
    for count in range(0,2):
        present_strings = data_file.readline().strip().split()
        query_dict['present'][present_strings[0]] = present_strings[1]
    return query_dict

def all_followers (twitter_dict, given_username):
    """ (dict of {str: dict of {str: object}}, str) -> list of str
    
    Return a list of all followers of the given_username based on the 
    twitter_dict.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> all_followers (twitter_data, "b")
    ['a']
    >>> all_followers (twitter_data, "a")
    []
    """
    
    followers = []
    for user in twitter_dict:
        if given_username in twitter_dict[user]['following']:
            followers.append(user)
    return followers
    
def search_usernames (twitter_dict, given_usernames, operation):
    """ (dict of {str: dict of {str: object}}, list of str, str)
    -> list of str
    
    Format the information related to the operation for the given_usernames 
    based on the twitter_dict.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':['c']}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':['c']}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':['b']}}
    >>> search_usernames (twitter_data, ['a', 'b', 'c'], "following")
    ['c', 'c', 'b']
    >>> search_usernames (twitter_data, ['a'], "followers")
    []
    """
    
    modified_list = []
    for user in given_usernames:
        if operation == 'followers':
            modified_list.extend(all_followers(twitter_dict, user))
        elif operation == 'following':
            modified_list.extend(twitter_dict[user]['following'])
    return modified_list    

def remove_dupes (given_list):
    """ (list of str) -> list of str
    
    Format the given_list so that there are only a single instance of all 
    element.)
    
    >>> remove_dupes (['a', 'b', 'c'])
    ['a', 'b', 'c']
    >>> remove_dupes (['a', 'b', 'b'])
    ['a', 'b']
    """
    
    modified_list = []
    for user in given_list:
        if user not in modified_list:
            modified_list.append(user)
    return modified_list
    
def get_search_results (twitter_dict, search_spec_dict):
    """ (dict of {str: dict of {str: object}}, dict of {str: object}) ->
    list of str
    
    Return a list of usernames created by going through the operations of the
    search_spec_dict based on the twitter_dict.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':['c']}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':['c']}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':['b']}}
    >>> get_search_results (twitter_data, \
    {"username":"a", "operations":["followers", "following"]})
    []
    >>> get_search_results (twitter_data, {"username":"a", "operations":[]})
    ['a']
    """
    
    search_list = []
    search_list.append(search_spec_dict['username'])
    for operation in search_spec_dict['operations']:
        search_list = search_usernames(twitter_dict, search_list, operation)
        search_list = remove_dupes(search_list)
    return search_list
            
def filter_usernames (twitter_dict, given_usernames, operation, \
                      filter_spec_dict):
    """ (dict of {str: dict of {str: object}}, list of str, str, \
    dict of {str: str}) -> list of str
    
    Format the information related to the operation and the value of the 
    operation in the filter_spec_dict for the given_usernames based on the
    twitter_dict.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> filter_usernames (twitter_data, ['a','b','c'], "name-includes", \
    {"name-includes":"e"})
    ['a', 'b']
    >>> filter_usernames (twitter_data, ['a','b','c'], "following", \
    {"following":"d"})
    []
    """
    
    modified_list = []
    value = filter_spec_dict[operation]
    for user in given_usernames:
        if operation == 'name-includes':
            if value.lower() in twitter_dict[user]['name'].lower():
                modified_list.append(user)
        elif operation == 'location-includes':
            if value.lower() in twitter_dict[user]['location'].lower():
                modified_list.append(user)
        elif operation == 'follower':
            if value in all_followers(twitter_dict, user):
                modified_list.append(user)
        elif operation == 'following':
            if value in twitter_dict[user]['following']:
                modified_list.append(user)
    return modified_list
    
def get_filter_results (twitter_dict, given_usernames, filter_spec_dict):
    """ (dict of {str: dict of {str: object}}, list of str, \
    dict of {str: str}) -> list of str
    
    Return a list of usernames created by going through the restrictions in the
    filter_spec_dict based on the twitter_dict.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':['a']}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':['b']}}
    >>> get_filter_results (twitter_data, ['a','b','c'], \
    {"name-includes":"e", "following":"b"})
    ['a']
    >>> get_filter_results (twitter_data, ['a','b','c'], {})
    ['a', 'b', 'c']
    """
    
    filter_list = given_usernames
    for operation in filter_spec_dict:
        filter_list = filter_usernames(twitter_dict, filter_list, operation,
                                       filter_spec_dict)
    return filter_list
 
def format_long (twitter_dict, given_username):
    """ (dict of {str: dict of {str: object}}, str) -> str
    
    Retern the specific information that is associated with the given usernamne,
    that can be obtained from the twitterverse_dict.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> format_long (twitter_data, 'a')
    '----------\\na\\nname: Zed\\nlocation: \\nwebsite: \\nbio:\\n\\nfollowing: []\\n'
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'Toronto, Ontario', 'web':'www.Zed.com', \
    'bio':'I love to meet new people!', 'following':[]}}
    >>> format_long (twitter_data, 'a')
    '----------\\na\\nname: Zed\\nlocation: Toronto, Ontario\\nwebsite: www.Zed.com\\nbio:\\nI love to meet new people!\\nfollowing: []\\n'
    """
    
    user_info = '----------\n'
    user_info += given_username + '\n'
    user_info += 'name: ' + twitter_dict[given_username]['name'] + '\n'
    user_info += 'location: ' + twitter_dict[given_username]['location'] + '\n'
    user_info += 'website: ' + twitter_dict[given_username]['web'] + '\n'
    user_info += 'bio:\n' + twitter_dict[given_username]['bio'] + '\n'
    user_info += 'following: ' + \
        str(twitter_dict[given_username]['following']) + '\n'
    return user_info

def sort_by (twitter_dict, given_usernames, present_spec_dict):
    """ (dict of {str: dict of {str: object}}, list of str, dict of {str: str})
    -> NoneType
    
    Sorts the given_usernames according to the conditions in present_spec_dict
    based on the twitter_dict.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> result_list = ['a', 'b', 'c']
    >>> sort_by (twitter_data, result_list, \
    {'sort-by':'username','format':'long'})
    >>> result_list
    ['a', 'b', 'c']
    >>> sort_by (twitter_data, result_list, {'sort-by':'name', 'format':'long'})
    >>> result_list
    ['b', 'a', 'c']
    """
    
    if present_spec_dict['sort-by'] == 'username':
        tweet_sort(twitter_dict, given_usernames, username_first)
    elif present_spec_dict['sort-by'] == 'name':
        tweet_sort(twitter_dict, given_usernames, name_first)
    elif present_spec_dict['sort-by'] == 'popularity':
        tweet_sort(twitter_dict, given_usernames, more_popular)
        
def get_present_string (twitter_dict, given_usernames, present_spec_dict):
    """ (dict of {str: dict of {str: object}}, list of str, dict of {str: str})
    -> str
    
    Return a string of the information of the users in given_usernames formatted
    according to the conditions in present_spec_dict based on the twitter_dict.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> usernames = ['a']
    >>> get_present_string (twitter_data, [], {'sort-by':'username', \
    'format':'long'})
    '----------\\n----------'
    >>> get_present_string (twitter_data, usernames, {'sort-by':'username', \
    'format':'short'})
    "['a']"
    """

    present_string = ''
    usernames = given_usernames
    border = '----------'
    if len(usernames) == 0:
        present_string = border + '\n' + border
    else:
        sort_by(twitter_dict, usernames, present_spec_dict)
        for user in usernames:
            if present_spec_dict['format'] == 'short':
                present_string = str(usernames)
            elif present_spec_dict['format'] == 'long':
                present_string += format_long(twitter_dict, user)
        if present_spec_dict['format'] == 'long':
            present_string += border + '\n'
    return present_string
    
# --- Sorting Helper Functions ---
def tweet_sort(twitter_data, results, cmp):
    """ (Twitterverse dictionary, list of str, function) -> NoneType
    
    Sort the results list using the comparison function cmp and the data in 
    twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> result_list = ['c', 'a', 'b']
    >>> tweet_sort(twitter_data, result_list, username_first)
    >>> result_list
    ['a', 'b', 'c']
    >>> tweet_sort(twitter_data, result_list, name_first)
    >>> result_list
    ['b', 'a', 'c']
    """
    
    # Insertion sort
    for i in range(1, len(results)):
        current = results[i]
        position = i
        while position > 0 and cmp(twitter_data, results[position - 1], current) > 0:
            results[position] = results[position - 1]
            position = position - 1 
        results[position] = current 
            
def more_popular(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
    
    Return -1 if user a has more followers than user b, 1 if fewer followers, 
    and the result of sorting by username if they have the same, based on the 
    data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> more_popular(twitter_data, 'a', 'b')
    1
    >>> more_popular(twitter_data, 'a', 'c')
    -1
    """
    
    a_popularity = len(all_followers(twitter_data, a)) 
    b_popularity = len(all_followers(twitter_data, b))
    if a_popularity > b_popularity:
        return -1
    if a_popularity < b_popularity:
        return 1
    return username_first(twitter_data, a, b)
    
def username_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
    
    Return 1 if user a has a username that comes after user b's username 
    alphabetically, -1 if user a's username comes before user b's username, 
    and 0 if a tie, based on the data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':['b']}, \
    'b':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> username_first(twitter_data, 'c', 'b')
    1
    >>> username_first(twitter_data, 'a', 'b')
    -1
    """
    
    if a < b:
        return -1
    if a > b:
        return 1
    return 0

def name_first(twitter_data, a, b):
    """ (Twitterverse dictionary, str, str) -> int
        
    Return 1 if user a's name comes after user b's name alphabetically, 
    -1 if user a's name comes before user b's name, and the ordering of their
    usernames if there is a tie, based on the data in twitter_data.
    
    >>> twitter_data = {\
    'a':{'name':'Zed', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'b':{'name':'Lee', 'location':'', 'web':'', 'bio':'', 'following':[]}, \
    'c':{'name':'anna', 'location':'', 'web':'', 'bio':'', 'following':[]}}
    >>> name_first(twitter_data, 'c', 'b')
    1
    >>> name_first(twitter_data, 'b', 'a')
    -1
    """
    
    a_name = twitter_data[a]["name"]
    b_name = twitter_data[b]["name"]
    if a_name < b_name:
        return -1
    if a_name > b_name:
        return 1
    return username_first(twitter_data, a, b)       

if __name__ == '__main__':
    import doctest
    doctest.testmod()