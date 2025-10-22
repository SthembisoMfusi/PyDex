    #!/usr/bin/env python3
"""
PyDex: A Command-Line Pokedex
A simple Python script to look up Pokémon information from the PokéAPI.
"""
import random
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

    try:
        api_url = f"https://pokeapi.co/api/v2/pokemon/"
        response = requests.get(api_url)
        pokemon_name = sys.argv[1].lower()
        data = response.json()
    
        if pokemon_name.lower() == "--random" or pokemon_name.lower() == "--r":
            random_pokemon = random.choice(data['results'])
            pokemon_name = random_pokemon['name']
        
        # Construct the API URL
        api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            data = response.json()
                
            # Display basic Pokémon information
            print(f"Name: {data['name'].title()}")
            print(f"National Pokédex Number: {data['id']}")
            
            # Display types
            types = [type_info['type']['name'] for type_info in data['types']]
            print(f"Type(s): {', '.join(types).title()}")
            
            # Create dictionary of pokemon types and their colors
            type_colors = {"electric": Fore.YELLOW,
                           "water": Fore.BLUE,
                           "fire": Fore.RED,
                           "flying": Fore.CYAN
                           }
            
            types = [type_info['type']['name'] for type_info in data['types']]
            print(f"Type(s): {', '.join(types).title()}")

            # Display base stats
            print(f"Base Stats: ")
            for stat in data['stats']:
                # Properly formats the stat name first
                stat_name = stat['stat']['name'].replace('-', ' ').title()
                if stat_name == 'Hp':
                    stat_name = 'HP'
                print(f"  {stat_name}: {stat['base_stat']}")
    
        else:
            print(f"Error: Could not find Pokémon '{pokemon_name}'")
            print("Please check the spelling and try again.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to the PokéAPI. {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Could not parse the response from the API. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    

if __name__ == "__main__":
    main()