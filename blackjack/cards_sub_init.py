class Suit:
	def __init__( self, name, symbol ):
		self.name = name
		self.symbol = symbol		

	def __str__( self ):
		return self.name + ": " + self.symbol

Club, Diamond, Heart, Spade = Suit('Club', '♣'), Suit('Diamond', '♦'), \
Suit('Heart', '♥'), Suit('Spade', '♠')	

class Card:
	pass

class NumberCard( Card ):
	def __init__( self, rank, suit ):
		self.suit = suit
		self.rank = str(rank)
		self.hard = self.soft = rank

class AceCard( Card ):
	def __init__( self, rank, suit ):
		self.suit = suit
		self.rank = "A"
		self.hard, self.soft = 1, 11

class FaceCard( Card ):
	def __init__( self, rank, suit ):
		self.suit = suit
		self.rank = {11: 'J', 12: 'Q', 13: 'K'}[rank]
		self.hard = self.soft = 10


