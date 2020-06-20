# drinks.py
# Roughly 30-37mL in a shot (choosing 34mL)
# 355mL in a can of soda

# Drink Options: Contains each avalable liquid and their pump number
drink_options = [
	{"group": "Alcoholic", "name": "Gin", "value": "gin", "pump": 1},
	{"group": "Alcoholic", "name": "Rum", "value": "rum", "pump": 2},
	{"group": "Alcoholic", "name": "Vodka", "value": "vodka", "pump": 3},
	{"group": "Alcoholic", "name": "Tequila", "value": "tequila", "pump": 4},
	{"group": "Non-Alcoholic", "name": "Tonic Water", "value": "tonic", "pump": 5},
	{"group": "Non-Alcoholic", "name": "Coke", "value": "coke", "pump": 6},
	{"group": "Non-Alcoholic", "name": "Orange Juice", "value": "oj", "pump": 7},
	{"group": "Non-Alcoholic", "name": "Margarita Mix", "value": "mix", "pump": 8},
	{"group": "Non-Alcoholic", "name": "Water", "value": "water", "pump": 9}
]

drinks_list = {
	"mixed_drinks_list": [
		{
			"name": "Vodka Sprite",
			"ingredients": {
				"Vodka": 44,
				"Sprite": 148
			},
			"details": "44mL (1.5oz) Vodka, 148mL (5oz) Sprite"
		}, {
			"name": "Gin and Tonic",
			"ingredients": {
				"Gin": 44,
				"Tonic": 148
			},
			"details": "44mL (1.5oz) Gin, 148mL (5oz) Tonic"
		}, {
			"name": "Long Island",
			"ingredients": {
				"Gin": 15,
				"Rum": 15,
				"Vodka": 15,
				"Tequila": 15,
				"Coke": 30,
				"Oj": 30
			},
			"details": "15mL (0.5oz) Gin, 15mL (0.5oz) Rum, 15mL (0.5oz) Vodka, 15mL (0.5oz) Tequila, 30mL (1oz) Coke, 30mL (1oz) Oj"
		}, {
			"name": "Screwdriver",
			"ingredients": {
				"Vodka": 44,
				"Oj": 148
			},
			"details": "44mL (1.5oz) Vodka, 148mL (5oz) Oj"
		}, {
			"name": "Margarita",
			"ingredients": {
				"Tequila": 44,
				"Mix": 148
			},
			"details": "44mL (1.5oz) Tequila, 148mL (5oz) Margarita Mix"
		}, {
			"name": "Gin and Juice",
			"ingredients": {
				"Gin": 44,
				"Oj": 148
			},
			"details":"44mL (1.5oz) Gin, 148mL (5oz) Oj"
		}, {
			"name": "Tequila Sunrise",
			"ingredients": {
				"Tequila": 44,
				"Oj": 148
			},
			"details": "44mL (1.5oz) Tequila, 148mL (5oz) Oj"
		}
	],
	"shots_list": [
		{
			"name": "Vodka",
			"ingredients": {"Vodka": 34},
			"details": "34mL (1.15oz) of Vodka"
		}, {
			"name": "Rum",
			"ingredients": {"Rum": 34},
			"details": "34mL (1.15oz) of Rum"
		}, {
			"name": "Whiskey",
			"ingredients": {"Whiskey": 34},
			"details": "34mL (1.15oz) of Whiskey"
		}
	],
	"soda_list": [
		{
			"name": "Sprite",
			"ingredients": {"Sprite": 355},
			"details": "355mL (12oz) of Sprite"
		}, {
			"name": "Coke",
			"ingredients": {"Coke": 355},
			"details": "355mL (12oz) of Coke"
		}, {
			"name": "Orange Juice",
			"ingredients": {"Oj": 355},
			"details": "355mL (12oz) of Oj"
		}
	]
}
