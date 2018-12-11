class Suit:
	def __init__( self, name, symbol ):
		self.name = name
		self.symbol = symbol		

	def __str__( self ):
		return self.name + ": " + self.symbol

Club, Diamond, Heart, Spade = Suit('Club', '♣'), Suit('Diamond', '♦'), \
Suit('Heart', '♥'), Suit('Spade', '♠')	

class Card:
	def __init__( self, rank, suit ):
		self.suit = suit
		self.rank = rank
		self.hard, self.soft = self._points()

	def __str__( self ):
		return self.rank + ", " + self.suit.symbol

class NumberCard( Card ):
	def _points( self ):
		return int(self.rank), int(self.rank)

class AceCard( Card ):
	def _points( self ):
		return 1, 11

class FaceCard( Card ):
	def _points( self ):
		return 10, 10

class  CardFactory:
	def rank( self, rank ):
		self.class_, self.rank_str = {
			1: (AceCard, 'A'),
			11: (FaceCard, 'J'),
			12: (FaceCard, 'Q'),
			13: (FaceCard, 'K'),
		}.get(rank, (NumberCard, str(rank)))
		return self

	def suit( self, suit ):
		return self.class_(self.rank_str, suit)

card = CardFactory()

deck = [card.rank(r).suit(s)
	for s in (Club, Diamond, Heart, Spade)
		for r in range(1,14)]

if __name__ == '__main__':
	for card in deck:
		print(card)