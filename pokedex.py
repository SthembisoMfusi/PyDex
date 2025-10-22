#!/usr/bin/env python3
"""
PyDex: A Command-Line Pokedex
A simple Python script to look up Pokémon information from the PokéAPI.
"""

import sys
import argparse
import requests
import json
import random

def main():
    # creation of an argument parser object to handle CLI arguments
    parser = argparse.ArgumentParser()

    # adding different arguments
    parser.add_argument("name", nargs='?', help="enter the name or ID of the Pokemon")
    parser.add_argument("-r", "--random", action="store_true", help="lists info about a random pokemon")
    parser.add_argument("-a", "--abilities", action="store_true", help="shows the abilities of a pokemon")
    parser.add_argument("-s", "--size", action="store_true", help="shows the weight and height of a pokemon")
    parser.add_argument("-n", "--number", type=int, help="enter the Pokedex ID number of a pokemon")
    args = parser.parse_args()
    
    # if the user adds a --random flag
    if args.random:
        # generate a random number between 1 and 1025 corresponding to a Pokemon ID
        random_id = random.randint(1, 1025)
        pokemon_name = str(random_id)
        api_url = f"https://pokeapi.co/api/v2/pokemon/{random_id}"

    # if the user searches by name
    elif args.name:
        pokemon_name = args.name.lower()
        # API accepts both name and ID, so use input directly
        api_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

    # if the user searches by id number
    elif args.number:
        pokemon_name = args.number
        api_url = f"https://pokeapi.co/api/v2/pokemon/{int(args.number)}"

    # incase of no argument
    else:
        print("Usage: python pokedex.py <pokemon_name_or_id> or python pokedex.py --random")
        print("Example: python pokedex.py pikachu")
        print("Example: python pokedex.py 25")
        sys.exit(1)
    
    try:
        # Make the API request
        response = requests.get(api_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Display basic Pokémon information (always shown)
            print(f"Name: {data['name'].title()}")
            print(f"National Pokédex Number: {data['id']}")
            
            # Display types
            types = [type_info['type']['name'] for type_info in data['types']]
            print(f"Type(s): {', '.join(types).title()}")

            # Display base stats
            print(f"\nBase Stats:")
            for stat in data['stats']:
                # Properly formats the stat name first
                stat_name = stat['stat']['name'].replace('-', ' ').title()
                if stat_name == 'Hp':
                    stat_name = 'HP'
                print(f"  {stat_name}: {stat['base_stat']}")
            
            # if the user wants to check the abilities of a pokemon
            if args.abilities:
                print("\nAbilities:")
                i = 1
                for ability in data['abilities']:
                    ability_name = ability['ability']['name'].replace('-', ' ').title()
                    if ability['is_hidden']:
                        print(f"  Hidden Ability: {ability_name}")
                    else:
                        print(f"  Ability {i}: {ability_name}")
                        i += 1

            # if the user wants the weight and height of a pokemon
            if args.size:
                # PokéAPI returns height in decimeters and weight in hectograms
                # Convert to meters and kilograms
                height_m = data['height'] / 10  # decimeters to meters
                weight_kg = data['weight'] / 10  # hectograms to kilograms
                print(f"\nSize:")
                print(f"  Height: {height_m} m")
                print(f"  Weight: {weight_kg} kg")
                
        else:
            print(f"Error: Pokémon '{pokemon_name}' not found")
            print("Please check the spelling or ID and try again.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to the PokéAPI. {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Could not parse the response from the API. {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
