#!/usr/bin/env python3
"""
Social Media Username Finder (Sherlock)
========================================

A tool to search for usernames across multiple social media platforms.
This tool checks the availability of a given username across various social networks
and generates a report of found profiles.

Author: Aditya
Date: September 2025


Usage:
    python sherlock.py <username> [--debug]

Example:
    python sherlock.py adityadeore
    python sherlock.py adityadeore --debug
"""

import requests
import json
import os
import sys 
import argparse

DEBUG = False


def write_to_file(url , filename):
    with open(filename , "a") as f:
        f.write(url+"\n")

def print_error(err  , errstr , var , debug = False):
    if debug:
        print (f"\033[37;1m[\033[91;1m-\033[37;1m]\033[91;1m {errstr}\033[93;1m {err}")
    else:
        print (f"\033[37;1m[\033[91;1m-\033[37;1m]\033[91;1m {errstr}\033[93;1m {var}")

def make_request(url, headers, error_type, social_network):
    try:
        r = requests.get(url, headers=headers)
        if r.status_code:
            return r, error_type
    except requests.exceptions.HTTPError as errh:
        print_error(errh, "HTTP Error:", social_network, DEBUG)
    except requests.exceptions.ConnectionError as errc:
        print_error(errc, "Error Connecting:", social_network, DEBUG)
    except requests.exceptions.Timeout as errt:
        print_error(errt, "Timeout Error:", social_network, DEBUG)
    except requests.exceptions.RequestException as err:
        print_error(err, "Unknown error:", social_network, DEBUG)
    
    return None, ""


def sherlock(username):
    """
    Main function to search for username across social media platforms.
    
    Args:
        username (str): The username to search for
        
    Returns:
        None: Creates a text file with found profiles
    """
    print("\033[1;92m[\033[0m\033[1;77m*\033[0m\033[1;92m] Social Media Finder by Aditya\033[0m")
    print()

    fname = username+".txt"

    if os.path.isfile(fname):
        os.remove(fname)
        print("\033[1;92m[\033[0m\033[1;77m*\033[0m\033[1;92m] Removing previous file:\033[1;37m {}\033[0m".format(fname))

    print("\033[1;92m[\033[0m\033[1;77m*\033[0m\033[1;92m] Checking username\033[0m\033[1;37m {}\033[0m\033[1;92m on: \033[0m".format(username))
    raw = open("data.json", "r", encoding="utf-8")
    data = json.load(raw)

    # User agent is needed because some sites does not 
    # return the correct information because it thinks that
    # we are bot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
    }

    for social_network in data:
        url = data.get(social_network).get("url").format(username)
        error_type = data.get(social_network).get("errorType")
        cant_have_period = data.get(social_network).get("noPeriod")

        if ("." in username) and (cant_have_period == "True"):
            print("\033[37;1m[\033[91;1m-\033[37;1m]\033[92;1m {}:\033[93;1m User Name Not Allowed!".format(social_network))
            continue
            
        r, error_type = make_request(url=url, headers=headers, error_type=error_type, social_network=social_network)
        
        # Skip if request failed
        if r is None:
            continue
            
        if error_type == "message":
            error = data.get(social_network).get("errorMsg")
            # Checks if the error message is in the HTML
            if not error in r.text:
                print("\033[37;1m[\033[92;1m+\033[37;1m]\033[92;1m {}:\033[0m".format(social_network), url)
                write_to_file(url, fname)                	
            
            else:
                print("\033[37;1m[\033[91;1m-\033[37;1m]\033[92;1m {}:\033[93;1m Not Found!".format(social_network))
            
        elif error_type == "status_code":
            # Checks if the status code of the repsonse is 404
            if not r.status_code == 404:
                print("\033[37;1m[\033[92;1m+\033[37;1m]\033[92;1m {}:\033[0m".format(social_network), url)
                write_to_file(url, fname)
            
            else:
                print("\033[37;1m[\033[91;1m-\033[37;1m]\033[92;1m {}:\033[93;1m Not Found!".format(social_network))

        elif error_type == "response_url":
            error = data.get(social_network).get("errorUrl")

            if not error in r.url:
                print("\033[37;1m[\033[92;1m+\033[37;1m]\033[92;1m {}:\033[0m".format(social_network), url)
                write_to_file(url, fname)
            else:
                print("\033[37;1m[\033[91;1m-\033[37;1m]\033[92;1m {}:\033[93;1m Not Found!".format(social_network))

        elif error_type == "":
            print("\033[37;1m[\033[91;1m-\033[37;1m]\033[92;1m {}:\033[93;1m Error!".format(social_network))

    print("\033[1;92m[\033[0m\033[1;77m*\033[0m\033[1;92m] Saved: \033[37;1m{}\033[0m".format(username+".txt"))

if __name__ == "__main__":
    """
    Main execution block
    Enhanced by Aditya - September 2025
    """
    parser = argparse.ArgumentParser(
        description='Social Media Username Finder - Search for usernames across multiple platforms',
        epilog='Created by Aditya | Example: python sherlock.py johndoe'
    )
    parser.add_argument('username', help='Username to search across social media platforms')
    parser.add_argument("-d", '--debug', help="Enable debug mode for detailed error messages", action="store_true")

    args = parser.parse_args()
    
    if args.debug:
        DEBUG = True

    if args.username:
        sherlock(args.username)


