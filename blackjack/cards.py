from functools import partial
import random

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
		return self.suit.symbol + ' ' + self.rank

class NumberCard( Card ):
	def _points( self ):
		return int(self.rank), int(self.rank)

class AceCard( Card ):
	def _points( self ):
		return 1, 11

class FaceCard( Card ):
	def _points( self ):
		return 10, 10

def card( rank, suit ):
	if rank == 1: return AceCard('A', suit)
	elif 2 <= rank < 11: return NumberCard( str(rank), suit )
	elif 11 <= rank < 14: 
		name = {11: "J", 12: "Q", 13: "K"}[rank]
		return FaceCard( name, suit )
	else:
		raise Exception( "Rank out of range" )

def card2( rank, suit ):
	if rank == 1: return AceCard('A', suit)
	elif 2 <= rank < 11: return NumberCard( str(rank), suit )
	else:
		name = { 11: 'J', 12: 'Q', 13: 'K' }[rank]
		return FaceCard( name, suit )

def card3( rank, suit ):
	if rank == 1: return AceCard( 'A', suit )
	elif 2 <= rank < 11: return NumberCard( str(rank), suit )
	elif rank == 11:
		return FaceCard( 'J', suit )
	elif rank == 12:
		return FaceCard( 'Q', suit )  
	elif rank == 13:
		return FaceCard( 'K', suit )
	else:
		raise Exception( "Rank out of range" )

def card4( rank, suit ):
	class_ = {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard}.get(rank, NumberCard)
	return class_( rank, suit )

def card4_2( rank, suit ):
	class_ = {1: AceCard, 11: FaceCard, 12: FaceCard, 13: FaceCard}.get(rank, NumberCard)
	rank_str = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}.get(rank, str(rank))
	return class_(rank_str, suit)

def card4_3( rank, suit ):
	class_, rank_str = {
		1: (AceCard, 'A'),
		11: (FaceCard, 'J'),
		12: (FaceCard, 'Q'),
		13: (FaceCard, 'K'),
		}.get(rank, (NumberCard, str(rank)))
	return class_( rank_str, suit )


def card4_4( rank, suit ):
	part_class = {
		1: partial(AceCard, 'A'),
		11: partial(FaceCard, 'J'),
		12: partial(FaceCard, 'Q'),
		13: partial(FaceCard, 'K'),
		}.get(rank, partial(NumberCard, str(rank)))
	return part_class(suit)

deck = [card(rank, suit)
	for suit in (Club, Diamond, Heart, Spade)
		for rank in range(1,14)]

class Deck:
	def __init__( self ):
		self._cards = [card4_3(r,s) for s in (Club, Heart, 
				Diamond, Spade) for r in range(13)]
		random.shuffle( self._cards )
	def pop( self ):
		return self._cards.pop()

class Deck2( list ):
	def __init__( self ):
		super().__init__( card4_3(r+1,s) for r in range(13) for s 
		in (Club, Diamond, Heart, Spade) )
		random.shuffle( self )

class Deck3( list ):
	def __init__(self, decks=1):
		super().__init__()
		for i in range(decks):
			self.extend( card4_3(r+1,s) for r in range(13) for s in
			(Club, Diamond, Heart, Spade) )
		random.shuffle( self )
		burn = random.randint(1, 52)
		for i in range(burn) : self.pop()

class Hand:
	def __init__(self, dealer_card):
		self.dealer_card = dealer_card
		self.cards = []
	def hard_total(self):
		return sum(c.hard for c in self.cards)
	def soft_total(self)
		return sum(c.soft for c in self.cards)

class Hand2:
	def __init__( self, dealer_card, *cards ):
		self.dealer_card = dealer_card
		self.cards = list(cards)
	def hard_total( self ):
		return sum(c.hard in self.cards)
	def soft_total( self ):
		return sum(c.soft in self.cards)

class Hand3:
	def __init__(self, *args, **kwargs):
		if len(args) == 1 and isinstance(args[0],Hand3):
			# Clone an existing hand; often a bad idea
			other = args[0]
			self.dealer_card = other.dealer_card
			self.cards = other.cards
		else:
			# Build a fresh, new hand.
			dealer_card, *cards = args
			sel.dealer_card = dealer_card
			self.cards = list(cards)

class GameStrategy:
	def insurance( self, hand ):
		return False
	def split( self, hand ):
		return False
	def double( self, hand ):
		return False
	def hit( self, hand ):
		return sum(c.hard for c in hand.cards) <= 17

class Table:
	def __init__( self ):
		self.deck = Deck()
	def place_bet ( self, amount ):
		print( "Bet", amount )
	def get_hand( self ):
		try:
			self.hand = Hand2( d.pop(), d.pop(), d.pop() )
			self.hole_card = d.pop()
		except IndexError:
			# Out of cards: need to shuffle
			self.deck = Deck()
			return self.get_hand()
		print( "Deal", self.hand )
		return self.hand
	def can_insure( self, hand ):
		return hand.dealer_card.insure 

class BettingStrategy:
	def bet( self ):
		raise NotImplementedError( "No bet method" )
	def record_win( self ):
		pass
	def record_loss( self ):
		pass

class Flat(BettingStrategy):
	def bet( self ):
		return 1 

import abc

class BettingStrategy2(metaclass=abc.ABCMeta):
	@abstractmethod
	def bet( self ):
		return 1
	def record_win( self ):
		pass
	def record_loss( self ):
		pass

if __name__ == '__main__':
	d = Deck()
	h = Hand2( d.pop(), d.pop(), d.pop() )
	dumb = GameStrategy()

	h = Hand( deck.pop(), deck.pop(), deck.pop() )
	memento = Hand( h ) 
