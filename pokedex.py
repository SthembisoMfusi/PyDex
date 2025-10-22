#!/usr/bin/env python3
"""
PyDex: A Command-Line Pokedex
A simple Python script to look up Pokémon information from the PokéAPI.
"""

import random
import sys
import argparse
import requests
from colorama import Fore, Style, init

def main():
    # creation of an argument parser object to handle CLI arguments
    parser = argparse.ArgumentParser()

    # adding different arguments
    parser.add_argument("name", nargs='?', help="enter the name of the Pokemon")
    parser.add_argument("-r", "--random", action="store_true", help="lists info about a random pokemon")
    parser.add_argument("-a", "--abilities", action="store_true", help="shows the abilities of a pokemon")
    parser.add_argument("-n", "--number", type=int, help="enter the Pokedex ID number of a pokemon")
    args = parser.parse_args()
    
    # if the user adds a --random flag
    if args.random:
        # generate a random number between 1 and 1025 corresponding to a Pokemon ID
        random_id = random.randint(1, 1025)
        pokemon_name = str(random_id)
        api_url = f"https://pokeapi.co/api/v2/pokemon/{random_id}"


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="PyDex: A simple CLI Pokémon lookup")
    parser.add_argument("name", nargs="?", help="Enter the name of the Pokémon")
    parser.add_argument("-r", "--random", action="store_true", help="Fetch info about a random Pokémon")
    parser.add_argument("-a", "--abilities", action="store_true", help="Show abilities of the Pokémon")
    parser.add_argument("-s", "--size", action="store_true", help="Show weight and height of the Pokémon")
    parser.add_argument("-n", "--number", type=int, help="Enter the Pokédex ID number of a Pokémon")
    return parser.parse_args()


def fetch_pokemon_data(identifier):
    """Fetch Pokémon data from the PokéAPI using name or ID."""
    api_url = f"https://pokeapi.co/api/v2/pokemon/{identifier}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            
            # Display basic Pokémon information (always shown)
            print(f"Name: {data['name'].title()}")
            print(f"National Pokédex Number: {data['id']}")
            
            # Display types
            types = [type_info['type']['name'] for type_info in data['types']]
            print(f"Type(s): {', '.join(types).title()}")
            
            # Display height and weight (converted to meters and kilograms)
            height_m = data['height'] / 10  # decimeters to meters
            weight_kg = data['weight'] / 10  # hectograms to kilograms
            print(f"Height: {height_m} m")
            print(f"Weight: {weight_kg} kg")

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
                
        else:
            print(f"Error: Pokémon '{identifier}' not found.")
            sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not connect to the PokéAPI. {e}")
        sys.exit(1)


def get_random_pokemon_id():
    """Return a random Pokémon ID between 1 and 1025."""
    return random.randint(1, 1025)


def display_pokemon_info(data, show_abilities=False, show_size=False):
    """Print Pokémon info including types, stats, abilities, and size."""
    print(f"\nName: {data['name'].title()}")
    print(f"National Pokédex Number: {data['id']}")

    # Type colors (extend as needed)
    type_colors = {
        "electric": Fore.YELLOW,
        "water": Fore.BLUE,
        "fire": Fore.RED,
        "flying": Fore.CYAN
    }

    types = [type_info['type']['name'] for type_info in data['types']]
    print(f"Type(s): {', '.join(types).title()}")

    # Base stats
    print("\nBase Stats:")
    for stat in data['stats']:
        stat_name = stat['stat']['name'].replace('-', ' ').title()
        if stat_name.lower() == 'hp':
            stat_name = 'HP'
        print(f"  {stat_name}: {stat['base_stat']}")

    # Abilities
    if show_abilities:
        print("\nAbilities:")
        i = 1
        for ability in data['abilities']:
            ability_name = ability['ability']['name'].replace('-', ' ').title()
            if ability['is_hidden']:
                print(f"  Hidden Ability: {ability_name}")
            else:
                print(f"  Ability {i}: {ability_name}")
                i += 1

    # Size
    if show_size:
        height_m = data['height'] / 10
        weight_kg = data['weight'] / 10
        print("\nSize:")
        print(f"  Height: {height_m} m")
        print(f"  Weight: {weight_kg} kg")


def main():
    args = parse_arguments()

    # Determine Pokémon identifier
    if args.random:
        identifier = get_random_pokemon_id()
    elif args.number:
        identifier = args.number
    elif args.name:
        identifier = args.name.lower()
    else:
        print("Usage: python pokedex.py <pokemon_name> or python pokedex.py --random")
        print("Example: python pokedex.py pikachu")
        sys.exit(1)

    data = fetch_pokemon_data(identifier)
    display_pokemon_info(data, show_abilities=args.abilities, show_size=args.size)


if __name__ == "__main__":
    main()
