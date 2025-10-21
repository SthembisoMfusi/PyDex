#!/usr/bin/env python3
"""
PyDex: A Command-Line Pokedex
A simple Python script to look up Pokémon information from the PokéAPI.
"""

import sys
import requests
import json
from colorama import Fore, Style, init
init(autoreset=True)

def main():
    # Check if a Pokémon name was provided
    if len(sys.argv) != 2:
        print("Usage: python pokedex.py <pokemon_name>")
        print("Example: python pokedex.py pikachu")
        sys.exit(1)
    
    pokemon_name = sys.argv[1].lower()
    
    # Construct the API URL
    api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
    
    try:
        # Make the API request
        response = requests.get(api_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Display basic Pokémon information
            print(f"Name: {data['name'].title()}")
            print(f"National Pokédex Number: {data['id']}")
            
            # Create dictionary of pokemon types and their colors
            type_colors = {"electric": Fore.YELLOW,
                           "water": Fore.BLUE,
                           "fire": Fore.RED,
                           "flying": Fore.CYAN
                           }
            
            types = [type_info['type']['name'] for type_info in data['types']]

            #Create new list of types in color
            colored_types = [
                f"{type_colors.get(type_name.lower(), Fore.WHITE)}{type_name.title()}{Style.RESET_ALL}" for type_name in types
            ]

            # Display types
            print(f"Type(s): {', '.join(colored_types)}")
            
        else:
            print(f"Error: Pokémon '{pokemon_name}' not found\nPlease check the spelling and try again.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to the PokéAPI. {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Could not parse the response from the API. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
