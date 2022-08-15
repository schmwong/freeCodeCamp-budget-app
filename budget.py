from itertools import zip_longest

class Category:


	def __init__(self, catname):
		self.name = catname
		self.ledger = []
		self.balance = 0.0


	def check_funds(self, amount):
		if (abs(amount) > self.balance):
			return False
		else:
			return True

	
	def deposit(self, amount, description=""):
		amount = abs(amount)
		self.ledger.append(
			dict(
				amount=amount,
				description=description
			)
		)
		self.balance += amount

	
	def withdraw(self, amount, description=""):
		if self.check_funds(amount):
			amount = abs(amount) * -1
			self.ledger.append(
				dict(
					amount=amount,
					description=description
				)
			)
			self.balance -= abs(amount)
			return True
		else:
			return False


	def get_balance(self):
		return self.balance


	def transfer(self, amount, targetcat):
		if self.check_funds(amount):
			self.withdraw(amount, f"Transfer to {targetcat.name}")
			targetcat.deposit(amount, f"Transfer from {self.name}")
			return True
		else:
			return False


	def __str__(self):
		title = f"{self.name.center(30, '*')}\n"
		record = ""
		total = 0.0

		for line in self.ledger:
			description = line["description"][:23]
			amount = "%.2f" % line["amount"]
			record += f"{description}{amount.rjust(30 - len(description), ' ')}\n"
			total += round(line["amount"], 2)

		return f"{title}{record}Total: {total}"



def create_spend_chart(categories):
	
	# Get all category expenditure
	expenditure = {}
	for category in categories:
		spent = 0.0
		for line in category.ledger:
			if line["amount"] < 0:
				spent += abs(line["amount"])
		expenditure[category.name] = spent
	# print(expenditure)

	total_spent = sum(expenditure.values())
	# print(total_spent)

	# Rounded to the nearest 10%
	expenditure_percentage = {}
	for category in categories:
		expenditure_percentage[category.name] = int(expenditure[category.name]/total_spent*10)*10

	# print(expenditure_percentage)

	chart_title = "Percentage spent by category"
	
	chart_body = ""
	for y_value in range(100, -1, -10):
		row = ""
		row += f"\n{str(y_value).rjust(3)}|"
		for percentage in expenditure_percentage.values():
			if percentage >= y_value:
				row += " o "
			else:
				row += " " * 3
		row += " "
		chart_body += row

	
	x_axis = f"\n{' ' * 4}{'-' * (3 * len(expenditure) + 1)}\n"
	x_labels = ""

	for x in zip_longest(*expenditure.keys(), fillvalue=f"{' ' * 1}"):
		x_labels += f"{' ' * 4}{('').join([x.center(3) for x in x])} \n"

	x_axis += x_labels
	
	Chart = f"{chart_title}{chart_body}{x_axis}"
		
	return Chart.rstrip("\n") # remove last newline character