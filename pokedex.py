#!/usr/bin/env python3
"""
PyDex: A Command-Line Pokedex

This script provides a command-line interface (CLI) tool for looking up Pokémon
information from the PokeAPI (https://pokeapi.co/). Users can search for Pokémon
by name, Pokédex ID, or fetch a random Pokémon. It also supports displaying
additional details like abilities, height, and weight.

Dependencies:
- requests: For making HTTP requests to the PokeAPI.
- colorama: For adding colored output to the terminal (improves readability).

Usage Examples:
    python pokedex.py pikachu
    python pokedex.py 25
    python pokedex.py --random
    python pokedex.py charmander --abilities
    python pokedex.py 1 --size
    python pokedex.py --random --abilities --size
"""

import random
import sys
import argparse
import requests
from colorama import Fore, Style, init

# Initialize colorama once at the beginning for colored output.
# 'autoreset=True' ensures that styling is reset after each print statement,
# preventing subsequent terminal output from retaining the last color.
init(autoreset=True)

def parse_arguments():
    """
    Parses command-line arguments provided by the user.

    This function sets up an ArgumentParser to define the various options
    and positional arguments that the PyDex script accepts. It allows
    users to specify a Pokémon by name or ID, request a random Pokémon,
    and choose to display specific details like abilities or size.

    Returns:
        argparse.Namespace: An object containing the parsed arguments
                            as attributes. For example, `args.name` would
                            hold the Pokémon name, `args.random` would be
                            True if the --random flag was used, etc.
    """
    parser = argparse.ArgumentParser(
        description=(f"{Fore.CYAN}PyDex: A simple CLI Pokémon lookup tool "
                     f"using the PokeAPI.{Style.RESET_ALL}"),
        formatter_class=argparse.RawTextHelpFormatter 
    )

    parser.add_argument(
        "name",
        nargs="?", 
        help=("Enter the name (e.g., 'pikachu') or National Pokédex ID "
              "(e.g., '25') of the Pokémon you want to look up. "
              "This argument is not needed if --random is used.")
    )
    parser.add_argument(
        "-r", "--random",
        action="store_true", # Stores True if the flag is present
        help="Fetch and display information about a random Pokémon."
    )
    parser.add_argument(
        "-a", "--abilities",
        action="store_true",
        help="Show the abilities (including hidden abilities) of the Pokémon."
    )
    parser.add_argument(
        "-s", "--size",
        action="store_true",
        help="Display the height (in meters) and weight (in kilograms) of the Pokémon."
    )
    parser.add_argument(
        "-n", "--number",
        type=int,
        help="Enter the National Pokédex ID number of a Pokémon (e.g., 25 for Pikachu). "
             "Overrides the 'name' argument if both are provided."
    )
    return parser.parse_args()


def get_random_pokemon_id():
    """
    Generates a random valid National Pokédex ID.

    This function produces a random integer within the typical range of
    Pokémon IDs available in the PokeAPI. As of current API data, this
    range is generally considered to be from 1 to 1025 for "main" Pokémon
    entries, excluding forms or specific regional variants that might have
    higher or non-sequential IDs.

    Returns:
        int: A randomly selected integer representing a Pokémon's National Pokédex ID.
    """
    # As of the last update, PokéAPI has ~1025 "main" Pokémon entries for general lookup.
    # This range can be adjusted if the API expands significantly.
    return random.randint(1, 1025)


def fetch_pokemon_data(identifier):
    """
    Fetches Pokémon data from the PokeAPI.

    Constructs a request URL using the provided identifier (Pokémon name or ID)
    and attempts to retrieve the corresponding Pokémon data. It handles network
    errors and HTTP errors (e.g., 404 Not Found) gracefully, printing informative
    messages to the user.

    Args:
        identifier (str or int): The name (e.g., "pikachu") or National Pokédex
                                 ID (e.g., 25) of the Pokémon to fetch.

    Returns:
        dict or None: A dictionary containing the parsed JSON data of the Pokémon
                      if the request is successful (HTTP status 200). Returns
                      None if there's an HTTP error (e.g., Pokémon not found)
                      or a network connectivity issue.
    """
    api_url = f"https://pokeapi.co/api/v2/pokemon/{identifier}"
    try:
        response = requests.get(api_url)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError:
        
        print(f"{Fore.RED}Error: Pokémon '{identifier}' not found.")
        print(f"{Fore.RED}Please check the spelling or ID and try again.{Style.RESET_ALL}")
        return None
    except requests.exceptions.RequestException as e:
     
        print(f"{Fore.RED}Error: Could not connect to the PokéAPI. {e}{Style.RESET_ALL}")
        return None


def display_pokemon_info(data, show_abilities=False, show_size=False):
    """
    Prints formatted Pokémon information to the console.

    This function takes a dictionary of Pokémon data (as returned by PokeAPI)
    and optional flags to control which details are displayed. It formats
    the output with colors for better readability and organizes the information
    into sections like basic info, types, base stats, abilities, and size.

    Args:
        data (dict): A dictionary containing the Pokémon's data, typically
                     obtained from `fetch_pokemon_data`.
        show_abilities (bool, optional): If True, the Pokémon's abilities
                                         (including hidden ones) will be printed.
                                         Defaults to False.
        show_size (bool, optional): If True, the Pokémon's height (in meters)
                                    and weight (in kilograms) will be printed.
                                    Defaults to False.
    """
    print(f"\n{Fore.GREEN}--- {data['name'].title()} ---{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}National Pokédex Number: {data['id']}{Style.RESET_ALL}")

    type_colors = {
        "normal": Fore.WHITE, "fire": Fore.RED, "water": Fore.BLUE,
        "grass": Fore.GREEN, "electric": Fore.YELLOW, "ice": Fore.CYAN,
        "fighting": Fore.MAGENTA, "poison": Fore.LIGHTMAGENTA_EX,
        "ground": Fore.LIGHTYELLOW_EX, "flying": Fore.LIGHTCYAN_EX,
        "psychic": Fore.LIGHTRED_EX, "bug": Fore.LIGHTGREEN_EX,
        "rock": Fore.LIGHTWHITE_EX, "ghost": Fore.MAGENTA,
        "dragon": Fore.LIGHTRED_EX, "steel": Fore.LIGHTBLACK_EX,
        "dark": Fore.BLACK, "fairy": Fore.LIGHTBLUE_EX,
    }

 
    types = []
    for type_info in data['types']:
        type_name = type_info['type']['name']
     
        color = type_colors.get(type_name.lower(), Fore.WHITE)
        types.append(f"{color}{type_name.title()}{Style.RESET_ALL}")
    print(f"  Type(s): {', '.join(types)}")

    print(f"\n{Fore.YELLOW}  Base Stats:{Style.RESET_ALL}")
    for stat in data['stats']:
        stat_name = stat['stat']['name'].replace('-', ' ').title()
   
        if stat_name.lower() == 'hp':
            stat_name = 'HP'
        print(f"    {stat_name}: {stat['base_stat']}")

    
    if show_abilities:
        print(f"\n{Fore.MAGENTA}  Abilities:{Style.RESET_ALL}")
        ability_counter = 1
        for ability in data['abilities']:
            ability_name = ability['ability']['name'].replace('-', ' ').title()
            if ability['is_hidden']:
                print(f"    {Fore.LIGHTBLACK_EX}Hidden Ability: {ability_name}{Style.RESET_ALL}")
            else:
                print(f"    Ability {ability_counter}: {ability_name}")
                ability_counter += 1

   
    if show_size:
       
        height_m = data['height'] / 10  # decimeters to meters
        weight_kg = data['weight'] / 10  # hectograms to kilograms
        print(f"\n{Fore.BLUE}  Size:{Style.RESET_ALL}")
        print(f"    Height: {height_m} m")
        print(f"    Weight: {weight_kg} kg")
    print(f"\n{Fore.GREEN}------------------{Style.RESET_ALL}")


def main():
    """
    The main entry point of the PyDex script.

    This function orchestrates the entire program flow:
    1. Parses command-line arguments using `parse_arguments`.
    2. Determines the Pokémon identifier based on user input (random, ID, or name).
    3. Fetches the Pokémon data from PokeAPI using `fetch_pokemon_data`.
    4. Displays the retrieved information using `display_pokemon_info`,
       respecting the user's choices for displaying abilities and size.
    5. Provides clear usage instructions and exits if no valid Pokémon
       identifier or lookup method is provided.
    """
    args = parse_arguments()

    identifier = None
    if args.random:
   
        identifier = get_random_pokemon_id()
    elif args.number:
       
        identifier = args.number
    elif args.name:
      
        identifier = args.name.lower()
    else:
        
        print(f"{Fore.YELLOW}Error: No Pokémon specified. Please provide a name/ID or use --random.{Style.RESET_ALL}")
        
        parse_arguments().print_help()
        sys.exit(1)

    # Fetch Pokémon data using the determined identifier.
    pokemon_data = fetch_pokemon_data(identifier)

    # If data was successfully fetched (i.e., not None), display it.
    if pokemon_data:
        display_pokemon_info(
            pokemon_data,
            show_abilities=args.abilities,
            show_size=args.size
        )


if __name__ == "__main__":
 
    main()