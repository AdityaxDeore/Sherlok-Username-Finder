#!/usr/bin/env python3
"""
Social Media Username Finder - Web Interface
=============================================

Flask web application for the Social Media Username Finder tool.
This provides a user-friendly web interface for the command-line tool.

Author: Aditya Deore
Date: September 2025
Repository: sherlok-finds
"""

from flask import Flask, render_template, request, jsonify, send_file, Response
import json
import os
import requests
import threading
import time
from datetime import datetime

app = Flask(__name__)

# Import the sherlock functions
def write_to_file(url, filename):
    """Write found URL to file"""
    with open(filename, "a") as f:
        f.write(url + "\n")

def print_error(err, errstr, var, debug=False):
    """Print error messages"""
    if debug:
        print(f"ERROR: {errstr} {err}")
    else:
        print(f"ERROR: {errstr} {var}")

def make_request(url, headers, error_type, social_network):
    """Make HTTP request to check if username exists"""
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code:
            return r, error_type
    except requests.exceptions.HTTPError as errh:
        print_error(errh, "HTTP Error:", social_network, False)
    except requests.exceptions.ConnectionError as errc:
        print_error(errc, "Error Connecting:", social_network, False)
    except requests.exceptions.Timeout as errt:
        print_error(errt, "Timeout Error:", social_network, False)
    except requests.exceptions.RequestException as err:
        print_error(err, "Unknown error:", social_network, False)
    
    return None, ""

def sherlock_streaming(username):
    """Streaming version of sherlock function that yields results one by one"""
    
    # Load data.json
    try:
        with open("data.json", "r", encoding="utf-8") as raw:
            data = json.load(raw)
    except FileNotFoundError:
        yield json.dumps({"error": "data.json file not found"}) + "\n"
        return
    
    # User agent for requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
    }
    
    found_count = 0
    total_count = len(data)
    processed = 0
    
    # Send initial status
    yield json.dumps({
        "type": "start",
        "username": username,
        "total_platforms": total_count,
        "timestamp": datetime.now().isoformat()
    }) + "\n"
    
    for social_network in data:
        try:
            processed += 1
            
            # Send progress update
            yield json.dumps({
                "type": "progress",
                "current_platform": social_network,
                "processed": processed,
                "total": total_count,
                "percentage": int((processed / total_count) * 100)
            }) + "\n"
            
            url = data.get(social_network).get("url").format(username)
            error_type = data.get(social_network).get("errorType")
            cant_have_period = data.get(social_network).get("noPeriod")
            
            # Check if username contains period and platform doesn't allow it
            if ("." in username) and (cant_have_period == "True"):
                result = {
                    "type": "result",
                    "platform": social_network,
                    "status": "not_allowed",
                    "url": "",
                    "message": "Username not allowed (contains period)"
                }
                yield json.dumps(result) + "\n"
                continue
            
            # Make request
            r, error_type = make_request(url=url, headers=headers, error_type=error_type, social_network=social_network)
            
            # Skip if request failed
            if r is None:
                result = {
                    "type": "result",
                    "platform": social_network,
                    "status": "error",
                    "url": url,
                    "message": "Connection error"
                }
                yield json.dumps(result) + "\n"
                continue
            
            # Check based on error type
            found = False
            
            if error_type == "message":
                error = data.get(social_network).get("errorMsg")
                if not error in r.text:
                    found = True
            elif error_type == "status_code":
                if not r.status_code == 404:
                    found = True
            elif error_type == "response_url":
                error = data.get(social_network).get("errorUrl")
                if not error in r.url:
                    found = True
            
            if found:
                found_count += 1
                result = {
                    "type": "result",
                    "platform": social_network,
                    "status": "found",
                    "url": url,
                    "message": "Profile found"
                }
            else:
                result = {
                    "type": "result",
                    "platform": social_network,
                    "status": "not_found",
                    "url": url,
                    "message": "Profile not found"
                }
            
            yield json.dumps(result) + "\n"
                
        except Exception as e:
            result = {
                "type": "result",
                "platform": social_network,
                "status": "error",
                "url": "",
                "message": f"Error: {str(e)}"
            }
            yield json.dumps(result) + "\n"
    
    # Send completion status
    yield json.dumps({
        "type": "complete",
        "username": username,
        "total_platforms": total_count,
        "found_count": found_count,
        "timestamp": datetime.now().isoformat()
    }) + "\n"

def sherlock_web(username):
    """Web version of sherlock function that returns results"""
    results = []
    
    # Load data.json
    try:
        with open("data.json", "r", encoding="utf-8") as raw:
            data = json.load(raw)
    except FileNotFoundError:
        return {"error": "data.json file not found"}
    
    # User agent for requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
    }
    
    found_count = 0
    total_count = len(data)
    
    for social_network in data:
        try:
            url = data.get(social_network).get("url").format(username)
            error_type = data.get(social_network).get("errorType")
            cant_have_period = data.get(social_network).get("noPeriod")
            
            # Check if username contains period and platform doesn't allow it
            if ("." in username) and (cant_have_period == "True"):
                results.append({
                    "platform": social_network,
                    "status": "not_allowed",
                    "url": "",
                    "message": "Username not allowed (contains period)"
                })
                continue
            
            # Make request
            r, error_type = make_request(url=url, headers=headers, error_type=error_type, social_network=social_network)
            
            # Skip if request failed
            if r is None:
                results.append({
                    "platform": social_network,
                    "status": "error",
                    "url": url,
                    "message": "Connection error"
                })
                continue
            
            # Check based on error type
            found = False
            
            if error_type == "message":
                error = data.get(social_network).get("errorMsg")
                if not error in r.text:
                    found = True
            elif error_type == "status_code":
                if not r.status_code == 404:
                    found = True
            elif error_type == "response_url":
                error = data.get(social_network).get("errorUrl")
                if not error in r.url:
                    found = True
            
            if found:
                found_count += 1
                results.append({
                    "platform": social_network,
                    "status": "found",
                    "url": url,
                    "message": "Profile found"
                })
            else:
                results.append({
                    "platform": social_network,
                    "status": "not_found",
                    "url": url,
                    "message": "Profile not found"
                })
                
        except Exception as e:
            results.append({
                "platform": social_network,
                "status": "error",
                "url": "",
                "message": f"Error: {str(e)}"
            })
    
    return {
        "username": username,
        "total_platforms": total_count,
        "found_count": found_count,
        "results": results,
        "timestamp": datetime.now().isoformat()
    }
    """Web version of sherlock function that returns results"""
    results = []
    
    # Load data.json
    try:
        with open("data.json", "r", encoding="utf-8") as raw:
            data = json.load(raw)
    except FileNotFoundError:
        return {"error": "data.json file not found"}
    
    # User agent for requests
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'
    }
    
    found_count = 0
    total_count = len(data)
    
    for social_network in data:
        try:
            url = data.get(social_network).get("url").format(username)
            error_type = data.get(social_network).get("errorType")
            cant_have_period = data.get(social_network).get("noPeriod")
            
            # Check if username contains period and platform doesn't allow it
            if ("." in username) and (cant_have_period == "True"):
                results.append({
                    "platform": social_network,
                    "status": "not_allowed",
                    "url": "",
                    "message": "Username not allowed (contains period)"
                })
                continue
            
            # Make request
            r, error_type = make_request(url=url, headers=headers, error_type=error_type, social_network=social_network)
            
            # Skip if request failed
            if r is None:
                results.append({
                    "platform": social_network,
                    "status": "error",
                    "url": url,
                    "message": "Connection error"
                })
                continue
            
            # Check based on error type
            found = False
            
            if error_type == "message":
                error = data.get(social_network).get("errorMsg")
                if not error in r.text:
                    found = True
            elif error_type == "status_code":
                if not r.status_code == 404:
                    found = True
            elif error_type == "response_url":
                error = data.get(social_network).get("errorUrl")
                if not error in r.url:
                    found = True
            
            if found:
                found_count += 1
                results.append({
                    "platform": social_network,
                    "status": "found",
                    "url": url,
                    "message": "Profile found"
                })
            else:
                results.append({
                    "platform": social_network,
                    "status": "not_found",
                    "url": url,
                    "message": "Profile not found"
                })
                
        except Exception as e:
            results.append({
                "platform": social_network,
                "status": "error",
                "url": "",
                "message": f"Error: {str(e)}"
            })
    
    return {
        "username": username,
        "total_platforms": total_count,
        "found_count": found_count,
        "results": results,
        "timestamp": datetime.now().isoformat()
    }

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    """API endpoint for username search"""
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    if len(username) < 2:
        return jsonify({"error": "Username must be at least 2 characters"}), 400
    
    # Run sherlock search
    results = sherlock_web(username)
    
    return jsonify(results)

@app.route('/search-stream/<username>')
def search_stream(username):
    """SSE endpoint for streaming search results"""
    
    if not username or len(username) < 2:
        return jsonify({"error": "Invalid username"}), 400
    
    def generate():
        for data in sherlock_streaming(username):
            yield f"data: {data}\n\n"
    
    return Response(generate(), mimetype='text/event-stream', headers={
        'Cache-Control': 'no-cache',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Cache-Control'
    })

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/api/health')
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)